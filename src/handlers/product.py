import tornado.web
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
        produces:
        - application/json
        parameters:
        -   name: product_id
            in: path
            description: id of the product
            required: true
            type: string
        responses:
            200:
                description: purchase completed successfully
        """
        identity = get_jwt_payload(self.request).get("identity")

        self.set_status(200)
        self.write({"message": "TO DO"})
