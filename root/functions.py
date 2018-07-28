import secrets
import os
from root import app
from PIL import Image


def save_picture(image_file):
    s = secrets.token_hex(8)
    _, ext = os.path.splitext(image_file.filename)
    picture_fn = s + ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (200, 200)
    i = Image.open(image_file)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def save_resume(resume_file):
    s = secrets.token_hex(8)
    _, ext = os.path.splitext(resume_file.filename)
    resume_fn = s + ext
    resume_path = os.path.join(app.root_path, 'static/resume', resume_fn)

    resume_file.save(resume_path)
    return resume_fn
