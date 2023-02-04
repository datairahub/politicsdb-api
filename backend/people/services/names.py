# -*- coding: utf-8 -*-
def clean_spanish_name(name):
    while "  " in name:
        name = name.replace("  ", " ")
    name = name.replace(" La ", " la ").replace(" El ", " el ")
    name = name.replace(" Las ", " las ").replace(" Los ", " los ")
    name = name.replace(" De ", " de ").replace(" Del ", " del ")
    name = name.replace(" Y ", " ").replace(" y ", " ")
    name = name.replace(" I ", " ").replace(" i ", " ")
    name = name.replace(" E ", " ").replace(" e ", " ")
    name = name.strip()

    fixed_names = {
        "Alvaro": "Álvaro",
        "Andres": "Andrés",
        "Angel": "Ángel",
        "Angela": "Ángela",
        "Angeles": "Ángeles",
        "Anton": "Antón",
        "Iñigo": "Íñigo",
        "Ines": "Inés",
        "Ivan": "Iván",
        "Jesus": "Jesús",
        "Jose": "José",
        "Joaquin": "Joaquín",
        "Lopez": "López",
        "Mª": "María",
        "Maria": "María",
        "Oscar": "Óscar",
        "Perez": "Perez",
        "Sanjuan": "Sanjuán",
        "Victor": "Víctor",
    }
    return " ".join([fixed_names.get(n, n) for n in name.split(" ")])
