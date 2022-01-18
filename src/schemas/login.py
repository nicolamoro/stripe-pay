from marshmallow import Schema, fields
from tornado_swagger.model import register_swagger_model


@register_swagger_model
class LoginSchema(Schema):
    """
    ---
    type: object
    description: Login object
    properties:
        username:
            description: Username
            type: string
        password:
            description: Password
            type: string
    """

    username = fields.Str(required=True)
    password = fields.Str(required=True)
