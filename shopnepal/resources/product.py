from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import shop, product
import uuid

blueprint = Blueprint('products', __name__, description='Operations on products')

@blueprint.route('/product')
class ProductList(MethodView):
    def get(self):
        # Return the list of products
        return {"products": list(product.values())}

    def post(self):
        new_product = request.json  # Get the product data from the request body
        
        # Ensure the shop exists
        if new_product["shop_id"] not in shop:
            return {"message": "Shop not found"}, 404
        
        # Generate a unique product ID
        product_id = uuid.uuid4().hex
        
        # Create the product entry
        product_data = {**new_product, "id": product_id}
        product[product_id] = product_data
        
        return product_data, 201  # Return the created product with a 201 status code

@blueprint.route('/product/<product_id>')
class Product(MethodView):
    def get(self, product_id):
        # Fetch the product by ID
        try:
            return product[product_id], 200
        except KeyError:
            abort(404, message="Product not found")

    def delete(self, product_id):
        # Delete the product by ID
        try:
            del product[product_id]
            return {"message": "Product deleted"}, 200
        except KeyError:
            abort(404, message="Product not found")

    def put(self, product_id):
        # Update an existing product by ID
        product_data = request.json
        
        # Ensure necessary fields are present
        if "price" not in product_data or "name" not in product_data:
            abort(400, message="Invalid product data")
        
        try:
            # Update the product with the new data
            existing_product = product[product_id]
            existing_product.update(product_data)  # Merge old and new data
            return existing_product, 200
        except KeyError:
            abort(404, message="Product not found")
