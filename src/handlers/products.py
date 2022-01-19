import stripe
import tornado.web
from schemas import products_get_schema
from utils.auth import require_jwt_auth


@require_jwt_auth
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
        # TODO:
        # see if it possible to fetch products and prices with the same API call
        # (dashboard already does it with 'include' clause, but here doesn't work)
        products = stripe.Product.list().data

        # TODO:
        # handle multiple product pages
        for product in products:
            prices = stripe.Price.list(product=product.id)

            # TODO:
            # handle multiple prices... at the moment only first price is considered
            product.price = prices.data[0]

        self.write({"data": products_get_schema.load(products)})
