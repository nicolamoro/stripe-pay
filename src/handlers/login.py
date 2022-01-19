import json

import stripe
import tornado.web

from schemas import login_schema
from utils.auth import create_jwt_token
from utils.hash import generate_hash


class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        """
        ---
        tags:
        - Authentication
        summary: Authenticate user
        description: |
            If given credentials are correct, this endpoint will return
            a JWT token to be used in all protected routes.
        parameters:
        -   name: customer
            in: body
            description: Authentication data
            schema:
                $ref: '#/definitions/LoginSchema'
        produces:
        - application/json
        responses:
            201:
                description: Successfully authenticated
                schema:
                    $ref: '#/definitions/TokenSchema'
            400:
                description: Invalid data
            401:
                description: Unauthenticated
        """
        try:
            login_data = login_schema.load(json.loads(self.request.body))
        except Exception:
            self.set_status(400)
            self.write({"message": "Invalid data"})
            self.finish()
            return

        try:
            customer = stripe.Customer.retrieve(id=login_data["username"])
        except Exception:
            self.set_status(401)
            self.write({"message": "User not found"})
            self.finish()
            return

        if customer.get("metadata", {}).get("password") != generate_hash(login_data["password"]):
            self.set_status(401)
            self.write({"message": "Invalid password"})
            self.finish()
            return

        response = {"access_token": create_jwt_token(login_data["username"])}
        self.write(response)
