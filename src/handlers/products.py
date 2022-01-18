import stripe
import tornado.web
from schemas import products_get_schema


class ProductsHandler(tornado.web.RequestHandler):
    def get(self):
        """
        ---
        tags:
        - Products
        summary: List all products with price
        description: List all products with price
        produces:
        - application/json
        responses:
            200:
                description: list of products with associated price
                schema:
                    type: object
                    properties:
                        data:
                            type: array
                            items:
                                $ref: '#/definitions/ProductSchema'

        """
        products = stripe.Product.list().data

        for product in products:
            prices = stripe.Price.list(product=product.id)
            product.price = prices.data[0]

        self.write({"data": products_get_schema.load(products)})
