from marshmallow import Schema, fields, validate
from tornado_swagger.model import register_swagger_model


@register_swagger_model
class AddressSchema(Schema):
    """
    ---
    type: object
    description: Address object
    properties:
        city:
            description: City
            type: string
        country:
            description: Country
            type: string
        line1:
            description: Line1
            type: string
        line2:
            description: Line2
            type: string
        postal_code:
            description: Postal Code
            type: string
        state:
            description: State
            type: string
    """

    city = fields.Str()
    country = fields.Str(validate=validate.Length(equal=2))
    line1 = fields.Str()
    line2 = fields.Str()
    postal_code = fields.Str()
    state = fields.Str()
