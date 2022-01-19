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
            description: Price currency
            type: string
        unit_amount:
            description: Price unit amount
            type: integer
    """

    currency = fields.Str(validate=validate.Length(equal=3))
    unit_amount = fields.Integer()
