from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import request
import uuid

from db import shop, product

blueprint = Blueprint('shops', __name__, description='Operations on shops')

@blueprint.route('/shop/<shop_id>')
class Shop(MethodView):
    def get(self, shop_id):
        try:
            return shop[shop_id], 200
        except KeyError:
            abort(404, message="Shop not found")

    def delete(self, shop_id):
        try:
            del shop[shop_id]
            return {"message": "Shop deleted"}, 200
        except KeyError:
            abort(404, message="Shop not found")


@blueprint.route('/shop')
class ShopsList(MethodView):
    def get(self):
        return {"shops": list(shop.values())}

    def post(self):
        shop_data = request.json  # Get the JSON data from the request

        # Validate the input
        if "name" not in shop_data:
            abort(400, message="Invalid shop data")  # Bad request if name is missing

        # Check if shop already exists
        for existing_shop in shop.values():
            if existing_shop["name"] == shop_data["name"]:
                abort(400, message="Shop already exists")  # Bad request if shop name exists

        # Create a new shop ID and save it
        shop_id = uuid.uuid4().hex  # Generate a unique shop ID
        new_shop = {**shop_data, "id": shop_id}  # Merge the data with the new ID
        shop[shop_id] = new_shop  # Add the shop to the dictionary

        return new_shop, 201  # Return the new shop with a 201 status code
