# -*- coding: utf-8 -*-
from django.db import migrations

DATA = [
    [
        "1976-07-08",
        "1977-07-05",
        "Suárez I",
        "https://en.wikipedia.org/wiki/First_government_of_Adolfo_Su%C3%A1rez",
        0,
        "0",
    ],
    [
        "1977-07-05",
        "1979-04-06",
        "Suárez II",
        "https://en.wikipedia.org/wiki/Second_government_of_Adolfo_Su%C3%A1rez",
        1,
        "I",
    ],
    [
        "1979-04-06",
        "1981-02-27",
        "Suárez III",
        "https://en.wikipedia.org/wiki/Third_government_of_Adolfo_Su%C3%A1rez",
        2,
        "II",
    ],
    [
        "1981-02-27",
        "1982-12-03",
        "Calvo-Sotelo I",
        "https://en.wikipedia.org/wiki/Government_of_Leopoldo_Calvo-Sotelo",
        3,
        "III",
    ],
    [
        "1982-12-03",
        "1986-07-26",
        "González I",
        "https://en.wikipedia.org/wiki/First_government_of_Felipe_Gonz%C3%A1lez",
        4,
        "IV",
    ],
    [
        "1986-07-26",
        "1989-12-07",
        "González II",
        "https://en.wikipedia.org/wiki/Second_government_of_Felipe_Gonz%C3%A1lez",
        5,
        "V",
    ],
    [
        "1989-12-07",
        "1993-07-14",
        "González III",
        "https://en.wikipedia.org/wiki/Third_government_of_Felipe_Gonz%C3%A1lez",
        6,
        "VI",
    ],
    [
        "1993-07-14",
        "1996-05-06",
        "González IV",
        "https://en.wikipedia.org/wiki/Fourth_government_of_Felipe_Gonz%C3%A1lez",
        7,
        "VII",
    ],
    [
        "1996-05-06",
        "2000-04-28",
        "Aznar I",
        "https://en.wikipedia.org/wiki/First_government_of_Jos%C3%A9_Mar%C3%ADa_Aznar",
        8,
        "VIII",
    ],
    [
        "2000-04-28",
        "2004-04-18",
        "Aznar II",
        "https://en.wikipedia.org/wiki/Second_government_of_Jos%C3%A9_Mar%C3%ADa_Aznar",
        9,
        "IX",
    ],
    [
        "2004-04-18",
        "2008-04-14",
        "Zapatero I",
        "https://en.wikipedia.org/wiki/First_government_of_Jos%C3%A9_Luis_Rodr%C3%ADguez_Zapatero",
        10,
        "X",
    ],
    [
        "2008-04-14",
        "2011-12-22",
        "Zapatero II",
        "https://en.wikipedia.org/wiki/Second_government_of_Jos%C3%A9_Luis_Rodr%C3%ADguez_Zapatero",
        11,
        "XI",
    ],
    [
        "2011-12-22",
        "2016-11-04",
        "Rajoy I",
        "https://en.wikipedia.org/wiki/First_government_of_Mariano_Rajoy",
        12,
        "XII",
    ],
    [
        "2016-11-04",
        "2018-06-07",
        "Rajoy II",
        "https://en.wikipedia.org/wiki/Second_government_of_Mariano_Rajoy",
        13,
        "XIII",
    ],
    [
        "2018-06-07",
        "2020-01-13",
        "Sánchez I",
        "https://en.wikipedia.org/wiki/First_government_of_Pedro_S%C3%A1nchez",
        14,
        "XIV",
    ],
    [
        "2020-01-13",
        "2999-12-31",
        "Sánchez II",
        "https://en.wikipedia.org/wiki/Second_government_of_Pedro_S%C3%A1nchez",
        15,
        "XV",
    ],
]


def apply_migration(apps, schema_editor):
    Period = apps.get_model("positions", "Period")
    spain_goverment = apps.get_model("positions", "Institution").objects.get(
        name="Gobierno de España"
    )

    for row in DATA:
        Period(
            name=row[2],
            number=row[4],
            code=row[5],
            institution=spain_goverment,
            start=row[0],
            end=row[1],
            metadata={"en.wikipedia.org": row[3]},
        ).save()


def revert_migration(apps, schema_editor):
    Period = apps.get_model("positions", "Period")
    spain_goverment = apps.get_model("positions", "Institution").objects.get(
        name="Gobierno de España"
    )
    Period.objects.filter(institution=spain_goverment).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("positions", "0004_fill_spain_legislatures"),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration),
    ]
