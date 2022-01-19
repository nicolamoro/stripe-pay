from marshmallow import Schema, fields, validate
from tornado_swagger.model import register_swagger_model

from schemas.address import AddressSchema


@register_swagger_model
class CustomerSchema(Schema):
    """
    ---
    type: object
    description: Customer object
    properties:
        id:
            description: Id
            type: string
        password:
            description: Password
            type: string
        address:
            description: Address
            $ref: '#/definitions/AddressSchema'
        description:
            description: Description
            type: string
        email:
            description: Email
            type: string
        name:
            description: Name
            type: string
        phone:
            description: Phone
            type: string
    required:
        - id
        - password
        - email
        - name
    """

    id = fields.Str(required=True)
    password = fields.Str(load_only=True, required=True)
    address = fields.Nested(AddressSchema)
    description = fields.Str()
    email = fields.Str(required=True, validate=validate.Email())
    name = fields.Str(required=True)
    phone = fields.Str()
