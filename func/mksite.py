import boto3
import os
import random
import shutil
import string
import pathlib
import jinja2
from pathlib import Path


def get_root_directory():
    return pathlib.Path(__file__).parent.parent


def get_albums_data(session, bucket):
    albums = {}
    try:
        list_objects = session.list_objects(Bucket=bucket)
        for key in list_objects.get("Contents", []):
            album_img = key["Key"].split("/")
            if len(album_img) != 2 or album_img[1] == '':
                continue
            album, img = album_img
            albums.setdefault(album, []).append(img)
    except Exception as e:
        print(f"Error getting album data: {e}")
    return albums


def get_template(name):
    template_path = get_root_directory() / "templates" / name
    try:
        with open(template_path, "r") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading template: {e}")
        return None


def save_temporary_template(template):
    filename = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + ".html"
    temp_dir = get_root_directory() / "temp"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = temp_dir / filename
    try:
        with open(temp_path, "w") as file:
            file.write(template)
    except Exception as e:
        print(f"Error writing to temporary template: {e}")
    return str(temp_path)


def remove_temporary_dir():
    try:
        shutil.rmtree(get_root_directory() / "temp")
    except Exception as e:
        print(f"Error removing temporary directory: {e}")


def mksite_album(bucket, aws_access_key_id, aws_secret_access_key, endpoint_url, region):
    session = boto3.session.Session().client(
        's3', endpoint_url=endpoint_url, aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key, region_name=region
    )
    url = f"https://{bucket}.website.yandexcloud.net"
    albums = get_albums_data(session, bucket)
    if not albums:
        return

    try:
        for i, (album, photos) in enumerate(albums.items(), start=1):
            album_template = get_template("album.html")
            if not album_template:
                continue
            rendered_album = jinja2.Template(album_template).render(album=album, images=photos, url=url)
            album_path = save_temporary_template(rendered_album)
            session.upload_file(album_path, bucket, f"album{i}.html")

        index_template = get_template("index.html")
        album_objects = [{'name': f'album{i}.html', 'album': album} for i, album in enumerate(albums, start=1)]
        rendered_index = jinja2.Template(index_template).render(template_objects=album_objects)
        index_path = save_temporary_template(rendered_index)
        session.upload_file(index_path, bucket, "index.html")

        error_template = get_template("error.html")
        error_path = save_temporary_template(error_template)
        session.upload_file(error_path, bucket, "error.html")

        session.put_bucket_website(Bucket=bucket, WebsiteConfiguration={
            "ErrorDocument": {"Key": "error.html"},
            "IndexDocument": {"Suffix": "index.html"},
        })
    except Exception as e:
        print(f"Error in mksite_album: {e}")

    remove_temporary_dir()
    print(url)
