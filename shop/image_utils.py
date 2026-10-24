from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile



def process_image(uploaded_image, max_size=(1200, 1200), thumbnail_size=(300, 300)):
    with Image.open(uploaded_image) as image:
        image = image.convert("RGB")

        image.thumbnail(max_size)

        original_buffer = BytesIO()
        image.save(original_buffer, format="JPEG", quality=85)
        original_buffer.seek(0)

        thumbnail = image.copy()
        thumbnail.thumbnail(thumbnail_size)

        thumbnail_buffer = BytesIO()
        thumbnail.save(thumbnail_buffer, format="JPEG", quality=80)
        thumbnail_buffer.seek(0)

    return (
        ContentFile(original_buffer.read(), name="product.jpg"),
        ContentFile(thumbnail_buffer.read(), name="thumbnail.jpg"),
    )
