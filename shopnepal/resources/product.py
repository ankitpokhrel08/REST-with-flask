from flask import request
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask.views import MethodView
from db import db
import uuid
from schemas import ProductSchemas, ProductUpdateSchema
from models import ProductModel

blueprint = Blueprint('products', __name__, description='Operations on products')

@blueprint.route('/product')
class ProductList(MethodView):
    @blueprint.response(200,ProductSchemas(many=True))
    def get(self):
        return ProductModel.query.all()
    
    @blueprint.arguments(ProductSchemas)
    @blueprint.response(200,ProductSchemas)
    def post(self,new_product):
        product = ProductModel(**new_product)
        try:
            db.session.add(product);
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Invalid data")
        return product  
    

@blueprint.route('/product/<product_id>')
class Product(MethodView):
    @blueprint.response(200,ProductSchemas)
    def get(self, product_id):
        product = ProductModel.query.get_or_404(product_id)
        return product, 200

    def delete(self, product_id):
        product = ProductModel.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return {'message':"Product Deleted"}


        
    @blueprint.arguments(ProductUpdateSchema)
    @blueprint.response(201,ProductSchemas)
    def put(self,product_data, product_id):
        product =  ProductModel.query.get_or_404(product_id)
        if product:
            product.price = product_data['price']
            product.name = product_data['name']
        else:
            product = ProductModel(id = product_id, **product_data)
        try:
            db.session.add(product)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Invalid data")
        return product
        
   
