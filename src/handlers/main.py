import json

import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        """
        ---
        tags:
        - Test endpoints
        summary: Hello world
        description: Hello world endpoint
        produces:
        - application/json
        responses:
            200:
              description: return message
              schema:
                type: object
                properties:
                    message:
                        description: the return message
                        type: string
        """
        self.write(json.dumps({"message": "Hello, world"}))
