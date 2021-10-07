from rest_framework.views import exception_handler as django_exception_handler


def exception_handler(exc, context):
    response = django_exception_handler(exc, context)
    if response is not None and 'non_field_errors' in response.data:
        errors = response.data.pop('non_field_errors')
        response.data['errors'] = ' '.join(errors)
    return response
