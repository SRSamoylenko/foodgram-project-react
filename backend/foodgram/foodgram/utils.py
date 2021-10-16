from rest_framework import status
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if is_customization_needed(response):
        response.data = {
            'errors': '\n'.join(response.data)
        }

    return response


def is_customization_needed(response):
    return (
        response is not None
        and response.status_code == status.HTTP_400_BAD_REQUEST
        and isinstance(response.data, list)
    )
