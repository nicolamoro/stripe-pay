from marshmallow import EXCLUDE

from schemas.customer import CustomerSchema
from schemas.login import LoginSchema
from schemas.payment_intent import PaymentIntentSchema
from schemas.product import ProductSchema
from schemas.token import TokenSchema

login_schema = LoginSchema()
token_schema = TokenSchema()
products_schema = ProductSchema(many=True, unknown=EXCLUDE)
product_schema = ProductSchema(unknown=EXCLUDE)
customer_schema = CustomerSchema(unknown=EXCLUDE)
payment_intent_schema = PaymentIntentSchema(unknown=EXCLUDE)
