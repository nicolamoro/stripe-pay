import stripe
import tornado.ioloop
import tornado.web
from tornado_swagger.setup import setup_swagger

from config import Config
from handlers.customer import CustomerHandler
from handlers.customers import CustomersHandler
from handlers.login import LoginHandler
from handlers.product import ProductPurchaseHandler
from handlers.products import ProductsHandler


class Application(tornado.web.Application):
    _routes = [
        tornado.web.url(fr"{Config.API_BASE_URL}/login", LoginHandler),
        tornado.web.url(fr"{Config.API_BASE_URL}/customers", CustomersHandler),
        tornado.web.url(fr"{Config.API_BASE_URL}/customers/([^/]+)", CustomerHandler),
        tornado.web.url(fr"{Config.API_BASE_URL}/products", ProductsHandler),
        tornado.web.url(fr"{Config.API_BASE_URL}/products/([^/]+)/purchase", ProductPurchaseHandler),
    ]

    def __init__(self):
        stripe.api_key = Config.STRIPE_SECRET_KEY

        setup_swagger(
            self._routes,
            swagger_url=f"{Config.API_BASE_URL}{Config.SWAGGERUI_URL}",
            description=Config.SWAGGERUI_DESCRIPTION,
            api_version=Config.API_VERSION,
            title=Config.SWAGGERUI_TITLE,
            contact=Config.SWAGGERUI_CONTACT,
            security_definitions={"JWT": {"type": "apiKey", "in": "header", "name": "Authorization"}},
        )

        super(Application, self).__init__(self._routes)


if __name__ == "__main__":  # pragma: no cover
    app = Application()
    app.listen(Config.PORT)
    tornado.ioloop.IOLoop.current().start()
