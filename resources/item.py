from flask.views import MethodView
from flask_smorest import Blueprint, abort
# highlight-start
from flask_jwt_extended import jwt_required,get_jwt
# highlight-end
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", "items", description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    # highlight-start
    @jwt_required()
    # highlight-end
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    # highlight-start
    @jwt_required()
    # highlight-end
    def delete(self, item_id):
        jwt=get_jwt()
        if jwt=="is_admin":
            abort(500,"Jwt previlige required")
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get_or_404(item_id)

        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(**item_data)

        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item")
class ItemList(MethodView):
    # highlight-start
    @jwt_required(fresh=True)
    # highlight-end
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    # highlight-start
  
    # highlight-end
    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item