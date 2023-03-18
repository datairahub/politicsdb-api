# -*- coding: utf-8 -*-


def person_profile_image_path(instance, filename: str) -> str:
    """
    Generate Person profile image path
    """
    return f"static/images/person/{instance.id}/{filename}"
