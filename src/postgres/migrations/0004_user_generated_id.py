#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


CREATE_USER_SCHEMA = """
    CREATE FUNCTION users_user_id_generator(OUT result bigint) AS $$
    DECLARE
        -- 2015-08-19T00:00:00Z. This is arbitrarily chosen; anything is fine
        -- as long as it is a not-too-distant past.
        our_epoch bigint := 1449083752000;

        seq_id bigint;
        now_millis bigint;
    BEGIN
        SELECT nextval('users_user_id_seq') % (1 << 23)
        INTO seq_id;

        SELECT FLOOR(EXTRACT(EPOCH FROM clock_timestamp()) * 1000)
        INTO now_millis;

        result := (now_millis - our_epoch) << 23;
        result := result | seq_id;
    END;
    $$ LANGUAGE PLPGSQL;
"""

DROP_USER_SCHEMA = 'DROP FUNCTION users_user_id_generator();'

SET_ID_FIELD_BIGINT_DEFAULT = """
    ALTER TABLE "users_user" ALTER COLUMN "id"
        SET DATA TYPE bigint;
    ALTER TABLE "users_user" ALTER COLUMN "id"
        SET DEFAULT users_user_id_generator();
"""

DROP_ID_FIELD_BIGINT_DEFAULT = """
    ALTER TABLE "users_user" ALTER COLUMN "id"
        SET DEFAULT nextval('users_user_id_seq');
    ALTER TABLE "users_user" ALTER COLUMN "id"
        SET DATA TYPE integer USING "id" % (1 << 23);
"""


class Migration(migrations.Migration):

    dependencies = [
        ('postgres', '0003_rename_proposal_generated_id'),
        ('users', '0005_auto_20151225_1353'),
    ]

    operations = [
        migrations.RunSQL(
            CREATE_USER_SCHEMA,
            DROP_USER_SCHEMA,
        ),
        migrations.RunSQL(
            SET_ID_FIELD_BIGINT_DEFAULT,
            DROP_ID_FIELD_BIGINT_DEFAULT,
        ),
    ]
