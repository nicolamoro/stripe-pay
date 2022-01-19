import json

import stripe
import tornado.web

from schemas import customer_schema
from utils.hash import generate_hash


class CustomersHandler(tornado.web.RequestHandler):
    def post(self):
        """
        ---
        tags:
        - Customers
        summary: Create a customer
        description: Create a customer
        parameters:
        -   name: customer
            in: body
            description: Customer to be created
            schema:
                $ref: '#/definitions/CustomerSchema'
        produces:
        - application/json
        responses:
            201:
                description: Customer added
                schema:
                    $ref: '#/definitions/CustomerSchema'
            400:
                description: Error creating customer
        """
        try:
            user_data = customer_schema.load(json.loads(self.request.body))
        except Exception as e:
            self.set_status(400)
            self.write({"message": "Invalid data", "description": e.messages})
            self.finish()
            return

        # User password is saved hashed into customer metadata
        if user_data.get("password"):
            user_data["metadata"] = {"password": generate_hash(user_data["password"])}
            del user_data["password"]

        try:
            stripe.Customer.create(**user_data)
        except Exception as e:
            self.set_status(400)
            self.write({"message": e.user_message})
            self.finish()
            return

        self.write(customer_schema.dump(user_data))
        self.set_status(201, "Created")
