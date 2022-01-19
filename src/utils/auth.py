import datetime
import uuid

import jwt

from config import Config

JWT_OPTIONS = {
    "verify_signature": True,
    "verify_exp": True,
    "verify_nbf": False,
    "verify_iat": True,
    "verify_aud": False,
}

JWT_PAYLOAD_REQUEST_KEY = "jwt_payload"


def get_jwt_payload(request):
    return request.headers.get(JWT_PAYLOAD_REQUEST_KEY)


def create_jwt_token(identity):
    return jwt.encode(
        {
            "jti": str(uuid.uuid4()),
            "iat": datetime.datetime.utcnow(),
            "nbf": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=Config.JWT_ACCESS_TOKEN_EXPIRES),
            "identity": identity,
        },
        Config.JWT_SECRET_KEY,
        algorithm="HS256",
    )


def require_jwt_auth(handler_class):
    def wrap_execute(handler_execute):
        def require_auth(handler, kwargs):

            auth = handler.request.headers.get("Authorization")
            if auth:
                parts = auth.split()

                if parts[0].lower() != "bearer" or len(parts) == 1 or len(parts) > 2:
                    handler._transforms = []
                    handler.set_status(401)
                    handler.write({"message": "Invalid Header Authorization"})
                    handler.finish()
                    return

                token = parts[1]
                try:
                    handler.request.headers[JWT_PAYLOAD_REQUEST_KEY] = jwt.decode(
                        token,
                        Config.JWT_SECRET_KEY,
                        options=JWT_OPTIONS,
                        algorithms=["HS256"],
                    )

                except Exception as e:
                    handler._transforms = []
                    handler.set_status(401)
                    handler.write({"message": e.message})
                    handler.finish()
            else:
                handler._transforms = []
                handler.set_status(401)
                handler.write({"message": "Missing authorization"})
                handler.finish()

            return True

        def _execute(self, transforms, *args, **kwargs):
            try:
                require_auth(self, kwargs)
            except Exception:
                return False

            return handler_execute(self, transforms, *args, **kwargs)

        return _execute

    handler_class._execute = wrap_execute(handler_class._execute)
    return handler_class
