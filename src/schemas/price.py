from marshmallow import Schema, fields, validate
from tornado_swagger.model import register_swagger_model


@register_swagger_model
class PriceSchema(Schema):
    """
    ---
    type: object
    description: Price object
    properties:
        currency:
            description: price currency
            type: string
        unit_amount:
            description: price unit amount
            type: integer
    """

    currency = fields.Str(validate=validate.Length(equal=3))
    unit_amount = fields.Integer()
