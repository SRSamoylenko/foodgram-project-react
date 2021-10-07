from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.utils.representation import smart_repr
from rest_framework.validators import qs_filter, qs_exists


class IsCreatedValidator:
    """
    Checks whether object with such fields has been created.

    Should be applied to the serializer class, not to an individual field.
    """
    message = _('The object with values {field_names} does not exist.')
    missing_message = _('This field is required.')
    requires_context = True

    def __init__(self, queryset, fields, message=None):
        self.queryset = queryset
        self.fields = fields
        self.message = message or self.message

    def enforce_required_fields(self, attrs, serializer):
        """
        The `IsCreatedValidator` always forces an implied 'required'
        state on the fields it applies to.
        """
        if serializer.instance is not None:
            return

        missing_items = {
            field_name: self.missing_message
            for field_name in self.fields
            if serializer.fields[field_name].source not in attrs
        }
        if missing_items:
            raise ValidationError(missing_items, code='required')

    def filter_queryset(self, attrs, queryset, serializer):
        """
        Filter the queryset to all instances matching the given attributes.
        """
        sources = [
            serializer.fields[field_name].source
            for field_name in self.fields
        ]

        filter_kwargs = {
            source: attrs[source]
            for source in sources
        }
        return qs_filter(queryset, **filter_kwargs)

    def __call__(self, attrs, serializer):
        self.enforce_required_fields(attrs, serializer)
        queryset = self.queryset
        queryset = self.filter_queryset(attrs, queryset, serializer)

        checked_values = [
            value for field, value in attrs.items() if field in self.fields
        ]
        if None not in checked_values and not qs_exists(queryset):
            field_names = ', '.join(self.fields)
            message = self.message.format(field_names=field_names)
            raise ValidationError(message, code='object_not_exists')

    def __repr__(self):
        return '<%s(queryset=%s, fields=%s)>' % (
            self.__class__.__name__,
            smart_repr(self.queryset),
            smart_repr(self.fields)
        )
