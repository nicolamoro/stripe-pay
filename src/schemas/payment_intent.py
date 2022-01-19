from marshmallow import Schema, fields, validate
from tornado_swagger.model import register_swagger_model


@register_swagger_model
class PaymentIntentSchema(Schema):
    """
    ---
    type: object
    description: Payment Intent object
    properties:
        id:
            description: Payment intent id
            type: string
        amount:
            description: Payment intent amount
            type: integer
        currency:
            description: Payment intent currency
            type: string
        customer:
            description: Payment intent customer
            type: string
        receipt_email:
            description: Payment intent receipt email
            type: string
        status:
            description: Payment intent status
            type: string
    required:
        - id
        - amount
        - currency
        - customer
        - receipt_email
        - status
    """

    id = fields.Str(required=True)
    amount = fields.Integer(required=True)
    currency = fields.Str(validate=validate.Length(equal=3), required=True)
    customer = fields.Str(required=True)
    receipt_email = fields.Str(validate=validate.Email(), required=True)
    status = fields.Str(dump_only=True, required=True)
