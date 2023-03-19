# -*- coding: utf-8 -*-
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from core.models import DateSourceAbstractModel


class BirthDateSource(DateSourceAbstractModel):
    """
    Fuente (informativa) para la fecha de nacimiento
    """

    class Meta(DateSourceAbstractModel.Meta):
        db_table = "people_birthdatesource"
        verbose_name = "Fecha de nacimiento"
        verbose_name_plural = "Fechas de nacimiento"


@receiver(post_save, sender=BirthDateSource)
def source_post_save(sender, instance, created, **kwargs):
    """
    Register person birth date data
    """
    other_source = (
        BirthDateSource.objects.filter(
            person=instance.person,
        )
        .exclude(
            id=instance.id,
        )
        .order_by("-accuracy")
        .first()
    )

    if not other_source:
        # person only have this birth date source
        instance.person.birth_date = instance.date
        instance.person.birth_date_accuracy = instance.accuracy
        instance.person.save(update_fields=["birth_date", "birth_date_accuracy"])
        return

    if other_source.accuracy > instance.accuracy:
        # other source has greater accuracy, so use it
        instance.person.birth_date = other_source.date
        instance.person.birth_date_accuracy = other_source.accuracy
        instance.person.save(update_fields=["birth_date", "birth_date_accuracy"])
        return

    if other_source.accuracy <= instance.accuracy:
        # current source has more or equal accuracy, so use it
        instance.person.birth_date = instance.date
        instance.person.birth_date_accuracy = instance.accuracy
        instance.person.save(update_fields=["birth_date", "birth_date_accuracy"])
        return


@receiver(pre_delete, sender=BirthDateSource)
def source_pre_delete(sender, instance, **kwargs):
    """
    Unregister person birth date data
    """
    other_source = (
        BirthDateSource.objects.filter(
            person=instance.person,
        )
        .exclude(
            id=instance.id,
        )
        .order_by("-accuracy")
        .first()
    )

    if other_source:
        instance.person.birth_date = other_source.date
        instance.person.birth_date_accuracy = other_source.accuracy
    else:
        instance.person.birth_date = None
        instance.person.birth_date_accuracy = None

    instance.person.save(update_fields=["birth_date", "birth_date_accuracy"])
