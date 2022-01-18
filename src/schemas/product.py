from marshmallow import EXCLUDE, Schema, fields
from tornado_swagger.model import register_swagger_model

from schemas.price import PriceSchema


@register_swagger_model
class ProductSchema(Schema):
    """
    ---
    type: object
    description: Product object
    properties:
        id:
            description:  product id
            type: string
        active:
            description: active flag
            type: boolean
        description:
            description: product description
            type: string
        name:
            description: product name
            type: string
        price:
            description: the product price
            $ref: '#/definitions/PriceSchema'
    """

    id = fields.Str(required=True)
    active = fields.Bool(missing=True)
    description = fields.Str()
    name = fields.Str(required=True)
    price = fields.Nested(PriceSchema, unknown=EXCLUDE)
