import tornado.ioloop
import tornado.web

from config import Config
from handlers.main import MainHandler


def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
        ]
    )


if __name__ == "__main__":  # pragma: no cover
    app = make_app()
    app.listen(Config.PORT)
    tornado.ioloop.IOLoop.current().start()
