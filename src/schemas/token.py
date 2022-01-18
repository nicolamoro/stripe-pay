from marshmallow import Schema, fields
from tornado_swagger.model import register_swagger_model


@register_swagger_model
class TokenSchema(Schema):
    """
    ---
    type: object
    description: Token object
    properties:
        token:
            description: Token
            type: string
    """

    token = fields.Str(required=True)
