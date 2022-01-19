from marshmallow import Schema, fields
from tornado_swagger.model import register_swagger_model


@register_swagger_model
class TokenSchema(Schema):
    """
    ---
    type: object
    description: Access Token object
    properties:
        access_token:
            description: Access Token
            type: string
    required:
        - access_token
    """

    token = fields.Str(required=True)
