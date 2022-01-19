import stripe
import tornado.web

from schemas import customer_schema, payment_intent_schema, product_schema
from utils.auth import get_jwt_payload, require_jwt_auth


@require_jwt_auth
class ProductPurchaseHandler(tornado.web.RequestHandler):
    def post(self, product_id):
        """
        ---
        tags:
        - Products
        summary: Purchase product
        description: Purchase product
        security:
            - JWT: []
        produces:
        - application/json
        parameters:
        -   name: product_id
            in: path
            description: Id of the product
            required: true
            type: string
        responses:
            200:
                description: Purchase completed successfully
                schema:
                    $ref: '#/definitions/PaymentIntentSchema'
            400:
                description: Error processing purchase
        """
        customer_id = get_jwt_payload(self.request).get("identity")

        # Fetch Customer, Product and Prices info
        try:
            customer = customer_schema.dump(
                stripe.Customer.retrieve(customer_id),
            )

            product_obj = stripe.Product.retrieve(product_id)
            prices_obj = stripe.Price.list(product=product_id)
            product_obj["price"] = prices_obj.get("data")[0]
            product = product_schema.dump(product_obj)

        except Exception as e:
            self.set_status(400)
            self.write({"message": e.user_message})
            self.finish()
            return

        # Create PaymentIntent
        # - credit card for customer must be already present
        try:
            # Receipts in test mode will not be sent. See:
            # https://stripe.com/docs/receipts#receipts-in-test-mode
            #
            # It can be sent manually from dashboard.
            payment_intent_result = stripe.PaymentIntent.create(
                amount=product["price"]["unit_amount"],
                currency=product["price"]["currency"],
                customer=customer_id,
                receipt_email=customer.get("email"),
                confirm=True,
            )

        except Exception as e:
            self.set_status(400)
            self.write({"message": e.user_message})
            self.finish()
            return

        self.set_status(200)
        self.write(payment_intent_schema.dump(payment_intent_result))
