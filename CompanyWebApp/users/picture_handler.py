#users/picture_handler.py
#TO STORE THE UPLOADED FILE
import os
# pip install pillow to import PIL
from PIL import Image

from flask import url_for, current_app

def add_profile_pic(pic_upload,username):
    # Grab the file uploaded
    filename = pic_upload.filename
    # Grab extension type .jpg or .png
    ext_type = filename.split('.')[-1]
    # Create a new filename / your can use the password_hass to name
    storage_filename = str(username) + '.' +ext_type
    # Get the storage filepath
    filepath = os.path.join(current_app.root_path, 'static\profile_pics', storage_filename)
    # Play around with this size.
    output_size = (200, 200)
    # Open the picture and save it to the specific size and filepath
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename