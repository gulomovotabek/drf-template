import os
import mimetypes

from PIL import Image
from rest_framework.exceptions import ValidationError


def image_compressor(instance):
    if mimetypes.guess_type(instance.file.path) in ['image/jpeg', 'image/jpeg']:
        with Image.open(instance.file) as photo:
            aspect_ratio = photo.size[0] / photo.size[1]
            new_height = 512 / aspect_ratio
            photo.thumbnail((512, new_height))

            thumb_path = f'media/thumbnails/{os.path.basename(instance.file.name)}'
            photo.save(thumb_path, photo.format)

            instance.thumbnail = thumb_path


def validate_image(file):
    max_size = 1 * 1024 * 1024  # 1MB in bytes

    if file.size > max_size:
        raise ValidationError("Image size should be less than 1MB.")

    try:
        img = Image.open(file)
        if img.format != 'PNG':
            raise ValidationError("Only PNG images are allowed.")
    except Exception:
        raise ValidationError("Invalid image file.")
