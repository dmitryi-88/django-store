from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from .models import Product, ProductImage


def get_file_fields(sender):
    if sender is Product:
        return ("image", "thumbnail")
    return ("image", "thumbnail")


@receiver(pre_save, sender=Product)
@receiver(pre_save, sender=ProductImage)
def remember_old_files(sender, instance, **kwargs):
    instance._old_file_names = {}

    if not instance.pk:
        return

    old_values = (
        sender.objects.filter(pk=instance.pk).values(*get_file_fields(sender)).first()
    )

    if old_values:
        instance._old_file_names = old_values


@receiver(post_save, sender=Product)
@receiver(post_save, sender=ProductImage)
def delete_replaced_files(sender, instance, **kwargs):
    old_names = getattr(instance, "_old_file_names", {})

    for field_name in get_file_fields(sender):
        old_name = old_names.get(field_name)
        current_file = getattr(instance, field_name)
        current_name = current_file.name if current_file else None

        if old_name and old_name != current_name:
            field = sender._meta.get_field(field_name)
            field.storage.delete(old_name)


@receiver(post_delete, sender=Product)
@receiver(post_delete, sender=ProductImage)
def delete_model_files(sender, instance, **kwargs):
    for field_name in get_file_fields(sender):
        file_field = getattr(instance, field_name)

        if file_field and file_field.name:
            file_field.storage.delete(file_field.name)
