from utils.auth import create_jwt_token, get_jwt_payload, require_jwt_auth


class RequestMock:
    def __init__(self, headers={}):
        self.headers = headers


def test_require_jwt_auth_missing_headers():
    # arrange

    @require_jwt_auth
    class HandlerMock:
        request = RequestMock()

        def finish(self):
            pass

        def write(self, value):
            self.write_value = value

        def set_status(self, status):
            self.status = status

        def _execute(self, transforms, *args, **kwargs):
            return "_execute response"

    # act
    handler = HandlerMock()
    result = handler._execute([])

    # assert
    assert handler.status == 401
    assert handler.write_value["message"] == "Missing Authorization"
    assert result == "_execute response"


def test_require_jwt_auth_header_invalid():
    # arrange

    @require_jwt_auth
    class HandlerMock:
        request = RequestMock(headers={"Authorization": "test"})

        def finish(self):
            pass

        def write(self, value):
            self.write_value = value

        def set_status(self, status):
            self.status = status

        def _execute(self, transforms, *args, **kwargs):
            return "_execute response"

    # act
    handler = HandlerMock()
    result = handler._execute([])

    # assert
    assert handler.status == 401
    assert handler.write_value["message"] == "Invalid Header Authorization"
    assert result == "_execute response"


def test_require_jwt_auth_invalid_token():
    # arrange

    @require_jwt_auth
    class HandlerMock:
        request = RequestMock(headers={"Authorization": "Bearer 123"})

        def finish(self):
            pass

        def write(self, value):
            self.write_value = value

        def set_status(self, status):
            self.status = status

        def _execute(self, transforms, *args, **kwargs):
            return "_execute response"

    # act
    handler = HandlerMock()
    result = handler._execute([])

    # assert
    assert handler.status == 401
    assert handler.write_value["message"] == "Invalid Authorization"
    assert result == "_execute response"


def test_require_jwt_auth_raise_exception():
    # arrange

    @require_jwt_auth
    class HandlerMock:
        request = RequestMock(headers={"Authorization": "Bearer 123"})

        def finish(self):
            raise Exception()

        def write(self, value):
            self.write_value = value

        def set_status(self, status):
            self.status = status

        def _execute(self, transforms, *args, **kwargs):
            return "_execute response"

    # act
    handler = HandlerMock()
    result = handler._execute([])

    # assert
    assert result is False


def test_get_jwt_payload():
    # arrange
    request = RequestMock(headers={"jwt_payload": "test_data"})

    # act
    result = get_jwt_payload(request)

    # assert
    assert result == "test_data"


def test_create_jwt_token():
    # arrange
    identity = "test_username"

    # act
    result = create_jwt_token(identity)

    # assert
    assert len(result) > 0
