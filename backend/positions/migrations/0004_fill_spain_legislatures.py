# -*- coding: utf-8 -*-
from django.db import migrations

DATA = [
    ["0", "Legislatura Constituyente", "1977-07-01", "1979-04-01", "0"],
    ["1", "Legislatura I", "1979-04-01", "1982-12-01", "I"],
    ["2", "Legislatura II", "1982-12-01", "1986-07-01", "II"],
    ["3", "Legislatura III", "1986-07-01", "1989-12-01", "III"],
    ["4", "Legislatura IV", "1989-12-01", "1993-07-01", "IV"],
    ["5", "Legislatura V", "1993-07-01", "1996-05-01", "V"],
    ["6", "Legislatura VI", "1996-05-01", "2000-04-01", "VI"],
    ["7", "Legislatura VII", "2000-04-01", "2004-04-01", "VII"],
    ["8", "Legislatura VIII", "2004-04-01", "2008-04-01", "VIII"],
    ["9", "Legislatura IX", "2008-04-01", "2011-12-01", "IX"],
    ["10", "Legislatura X", "2011-12-01", "2015-12-01", "X"],
    ["11", "Legislatura XI", "2015-12-01", "2016-07-01", "XI"],
    ["12", "Legislatura XII", "2016-07-01", "2019-05-01", "XII"],
    ["13", "Legislatura XIII", "2019-05-01", "2020-01-01", "XIII"],
    ["14", "Legislatura XIV", "2020-01-01", "2022-01-04", "XIV"],
]


def apply_migration(apps, schema_editor):
    Period = apps.get_model("positions", "Period")
    spain_parlament = apps.get_model("positions", "Institution").objects.get(
        name="Parlamento de España"
    )
    spain_senate = apps.get_model("positions", "Institution").objects.get(
        name="Senado de España"
    )

    for row in DATA:
        Period(
            name=row[1],
            number=int(row[0]),
            code=row[4],
            institution=spain_parlament,
            start=row[2],
            end=row[3],
        ).save()
        Period(
            name=row[1],
            number=int(row[0]),
            code=row[4],
            institution=spain_senate,
            start=row[2],
            end=row[3],
        ).save()


def revert_migration(apps, schema_editor):
    Period = apps.get_model("positions", "Period")
    Period.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("positions", "0003_period"),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration),
    ]
