import boto3
from pathlib import Path

IMG_EXTENSIONS = [".jpg", ".jpeg"]


def upload_album(bucket, aws_access_key_id, aws_secret_access_key, album, path, endpoint_url, region):
    s3 = boto3.session.Session().client(
        's3', endpoint_url=endpoint_url, aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key, region_name=region
    )
    path = Path(path)

    validate_album_name(album)
    validate_album_path(path)

    if not is_album_exist(s3, bucket, album):
        create_album(s3, bucket, album)

    upload_photos_from_path(s3, bucket, album, path)


def validate_album_name(album):
    if '/' in album:
        raise ValueError("Album name cannot contain '/'")


def validate_album_path(path):
    if not path.is_dir():
        raise ValueError(f"Album path {str(path)} does not exist")


def is_album_exist(s3, bucket, album):
    response = s3.list_objects_v2(Bucket=bucket, Prefix=f"{album}/", Delimiter='/')
    return 'Contents' in response


def create_album(s3, bucket, album):
    s3.put_object(Bucket=bucket, Key=f"{album}/")
    print(f"Album '{album}' created")


def upload_photos_from_path(s3, bucket, album, path):
    count = 0
    for file in path.iterdir():
        if is_image(file):
            try:
                key = f"{album}/{file.name}"
                s3.upload_file(str(file), bucket, key)
                count += 1
                print(f"Uploaded {file.name} to {album}")
            except Exception as ex:
                print(f"Error uploading {file.name}: {ex}")
    print(f"Total {count} photos uploaded to {album}")


def is_image(file):
    return file.is_file() and file.suffix.lower() in IMG_EXTENSIONS
