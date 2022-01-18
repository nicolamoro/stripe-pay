import tornado.web


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
        pass
