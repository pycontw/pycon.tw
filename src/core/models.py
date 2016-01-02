from django.db import models


class BigForeignKey(models.ForeignKey):
    def db_type(self, connection):
        """ Adds support for foreign keys to big integers as primary keys.
        """
        presumed_type = super().db_type(connection)
        if presumed_type == 'integer':
            return 'bigint'
        return presumed_type
