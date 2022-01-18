from marshmallow import EXCLUDE

from schemas.customer import CustomerSchema
from schemas.login import LoginSchema
from schemas.product import ProductSchema
from schemas.token import TokenSchema

login_post_schema = LoginSchema()
token_schema = TokenSchema()
products_get_schema = ProductSchema(many=True, unknown=EXCLUDE)
product_get_schema = ProductSchema(unknown=EXCLUDE)
customer_post_schema = CustomerSchema(unknown=EXCLUDE)
