import stripe
import tornado.web
from utils.auth import get_jwt_payload, require_jwt_auth


@require_jwt_auth
class CustomerHandler(tornado.web.RequestHandler):
    def delete(self, customer_id):
        """
        ---
        tags:
        - Customers
        summary: Delete a customer
        description: Delete a customer
        produces:
        - application/json
        parameters:
        -   name: customer_id
            in: path
            description: id of the customer
            required: true
            type: string
        responses:
            204:
                description: Customer deleted
            403:
                description: Forbidden to delete a customer other than yourself
            400:
                description: Error deleting customer
        """
        identity = get_jwt_payload(self.request).get("identity")

        if identity != customer_id:
            self.set_status(403)
            self.write({"message": "Forbidden to delete a customer other than yourself"})
            self.finish()
            return

        try:
            stripe.Customer.delete(customer_id)
        except Exception as e:
            self.set_status(400)
            self.write({"message": e.user_message})
            self.finish()
            return

        self.set_status(204, "Deleted")
