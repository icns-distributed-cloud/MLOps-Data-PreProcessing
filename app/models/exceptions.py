class StatusCode:
    HTTP_404 = 404
    HTTP_406 = 406
    HTTP_500 = 500



class APIException(Exception):
    status_code: int
    message: str

    def __init__(
        self,
        *,
        status_code: int = StatusCode.HTTP_404,
        message: str = None,
        ex: Exception = None,
    ):
        self.status_code = status_code
        self.message = message
        super().__init__(ex)



class NotFoundDataEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_404,
            message='데이터셋을 찾을 수 없습니다.',
            ex=ex
        )


class NotFoundColumnEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_406,
            message='컬럼을 찾을 수 없습니다.',
            ex=ex
        )


async def exception_handler(error: APIException):
    if not isinstance(error, APIException):
        error = APIException(ex=error, message=str(error))
    return error