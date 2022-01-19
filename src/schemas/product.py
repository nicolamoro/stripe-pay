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
            description: Product id
            type: string
        active:
            description: Active flag
            type: boolean
        description:
            description: Product description
            type: string
        name:
            description: Product name
            type: string
        price:
            description: The product price
            $ref: '#/definitions/PriceSchema'
    required:
        - id
        - name
    """

    id = fields.Str(required=True)
    active = fields.Bool(load_default=True)
    description = fields.Str()
    name = fields.Str(required=True)
    price = fields.Nested(PriceSchema, unknown=EXCLUDE)
