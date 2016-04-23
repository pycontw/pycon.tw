import enum

from django.apps import apps
from django.db import models

from .validators import EAWMaxLengthValidator


class BigForeignKey(models.ForeignKey):
    def db_type(self, connection):
        """ Adds support for foreign keys to big integers as primary keys.

        Django's AutoField is actually an IntegerField (SQL integer field),
        but in some cases we are using bigint on PostgreSQL without Django
        knowing it. So we continue to trick Django here, swapping its field
        type detection, and just tells it to use bigint.

        :seealso: Migrations in the ``postgres`` app.
        """
        presumed_type = super().db_type(connection)
        if apps.is_installed('postgres') and presumed_type == 'integer':
            return 'bigint'
        return presumed_type


class EAWTextField(models.TextField):
    """Derived TextField that checks for its content's EAW lengh.

    This adds an extra validator that counts EAW wide characters as two
    instead of one.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.max_length is not None:
            self.validators.append(EAWMaxLengthValidator(self.max_length))


def make_choices_enum(typename, key_val_des, unique=True):
    """Build a enum.Enum subclass that can be used as Django choices.

    Usage in model::

        Color = make_choices_enum('Color', [
            ('red',   '#ff0000', _('Red')),
            ('blue',  '#00ff00', _('Blue')),
            ('green', '#0000ff', _('Green')),
        ])
        color = models.CharField(choices=Color.choices)
    """
    # Extract keys, values and descriptions.
    key_list, val_list, des_list = zip(*key_val_des)

    class ChoicesEnum(enum.Enum):
        def __new__(cls, val):
            """Get the value from the value list, instead of using the default
            integer schema.
            """
            obj = object.__new__(cls)
            obj._value_ = val_list[len(cls.__members__)]
            return obj

    new_enum_class = ChoicesEnum(typename, key_list)
    if unique:
        new_enum_class = enum.unique(new_enum_class)

    # Django choices (key, description) pairs.
    new_enum_class.choices = tuple(zip(val_list, des_list))
    return new_enum_class
