from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import request
import uuid
from db import db
from schemas import ShopSchema
from models import ShopModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError



blueprint = Blueprint('shops', __name__, description='Operations on shops')

@blueprint.route('/shop/<shop_id>')
class Shop(MethodView):
    @blueprint.response(200,ShopSchema)
    def get(self, shop_id):
        shop = ShopModel.query.get_or_404(shop_id)
        return shop, 200

    def delete(self, shop_id):
        shop = ShopModel.query.get_or_404(shop_id)
        db.session.delete(shop)
        db.session.commit()
        return {'message':"Shop Deleted"}
        
    
@blueprint.route('/shop')
class ShopsList(MethodView):
    @blueprint.response(200,ShopSchema(many=True))
    def get(self):
        return ShopModel.query.all()
        
    @blueprint.arguments(ShopSchema)
    @blueprint.response(201,ShopSchema)
    
    def post(self,shop_data):
        shop = ShopModel(**shop_data)
        try:
            db.session.add(shop);
            db.session.commit();
        except IntegrityError:
            abort(400, message="Shop already exists")
        except SQLAlchemyError:
            abort(500, message="Invalid data")


