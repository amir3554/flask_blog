import secrets
from blog import conf
import os


def save_image(image_file) -> str:
    """this function changes the image name for safety reasons.
    and it saves the image to the correct path and return the new name of it"""
    hex_name = secrets.token_hex(8)
    _, file_extension = os.path.splitext(image_file.filename) 
    new_image_name = hex_name + file_extension
    file_path = os.path.join(conf.IMAGES_DIR, new_image_name)
    image_file.save(file_path)
    return new_image_name




