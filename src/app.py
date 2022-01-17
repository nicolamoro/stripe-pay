import tornado.ioloop
import tornado.web
from tornado_swagger.setup import setup_swagger

from config import Config
from handlers.main import MainHandler


class Application(tornado.web.Application):
    _routes = [
        tornado.web.url(f"{Config.API_BASE_URL}/", MainHandler),
    ]

    def __init__(self):
        setup_swagger(
            self._routes,
            swagger_url=f"{Config.API_BASE_URL}{Config.SWAGGERUI_URL}",
            description=Config.SWAGGERUI_DESCRIPTION,
            api_version=Config.API_VERSION,
            title=Config.SWAGGERUI_TITLE,
            contact=Config.SWAGGERUI_CONTACT,
        )
        super(Application, self).__init__(self._routes)


if __name__ == "__main__":  # pragma: no cover
    app = Application()
    app.listen(Config.PORT)
    tornado.ioloop.IOLoop.current().start()
