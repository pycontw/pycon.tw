#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Replace the built-in auto-increment primary key with a time-based bigint.

The main purpose for this is to show a better URL schema than something like
"/proposals/12/". This is not only more secure, but better for the eye.

The default value function is adapted from
http://rob.conery.io/2014/05/29/a-better-id-generator-for-postgresql/
"""
from __future__ import unicode_literals

from django.db import migrations


CREATE_PROPOSAL_SCHEMA = """
    CREATE FUNCTION proposals_proposal_id_generator(OUT result bigint) AS $$
    DECLARE
        -- 2015-08-19T00:00:00Z. This is arbitrarily chosen; anything is fine
        -- as long as it is a not-too-distant past.
        our_epoch bigint := 1449083752000;

        seq_id bigint;
        now_millis bigint;
    BEGIN
        SELECT nextval('proposals_proposal_id_seq') % (1 << 23)
        INTO seq_id;

        SELECT FLOOR(EXTRACT(EPOCH FROM clock_timestamp()) * 1000)
        INTO now_millis;

        result := (now_millis - our_epoch) << 23;
        result := result | seq_id;
    END;
    $$ LANGUAGE PLPGSQL;
"""

DROP_PROPOSAL_SCHEMA = 'DROP FUNCTION proposals_proposal_id_generator();'

SET_ID_FIELD_BIGINT_DEFAULT = """
    ALTER TABLE "proposals_proposal" ALTER COLUMN "id"
        SET DATA TYPE bigint;
    ALTER TABLE "proposals_proposal" ALTER COLUMN "id"
        SET DEFAULT proposals_proposal_id_generator();
"""

DROP_ID_FIELD_BIGINT_DEFAULT = """
    ALTER TABLE "proposals_proposal" ALTER COLUMN "id"
        SET DEFAULT nextval('proposals_proposal_id_seq');
    ALTER TABLE "proposals_proposal" ALTER COLUMN "id"
        SET DATA TYPE integer USING "id" % (1 << 23);
"""


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            CREATE_PROPOSAL_SCHEMA,
            DROP_PROPOSAL_SCHEMA,
        ),
        migrations.RunSQL(
            SET_ID_FIELD_BIGINT_DEFAULT,
            DROP_ID_FIELD_BIGINT_DEFAULT,
        ),
    ]
