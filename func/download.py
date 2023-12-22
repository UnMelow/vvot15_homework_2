import boto3
from pathlib import Path


def download_album(bucket, aws_access_key_id, aws_secret_access_key, album, path, endpoint_url, region):
    s3 = boto3.session.Session().client(
        's3', endpoint_url=endpoint_url, aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key, region_name=region
    )
    path = Path(path)

    if not is_album_exist(s3, bucket, album):
        raise Exception(f"Album '{album}' does not exist in bucket '{bucket}'")

    if not path.is_dir():
        raise Exception(f"Path '{path}' is not a directory")

    download_files(s3, bucket, album, path)


def is_album_exist(s3, bucket, album):
    response = s3.list_objects_v2(Bucket=bucket, Prefix=f"{album}/", Delimiter='/')
    return 'Contents' in response and any(not obj['Key'].endswith('/') for obj in response['Contents'])


def download_files(s3, bucket, album, path):
    response = s3.list_objects_v2(Bucket=bucket, Prefix=f"{album}/")
    if 'Contents' in response:
        for obj in response['Contents']:
            if not obj['Key'].endswith('/'):
                download_file(s3, bucket, obj['Key'], path)
    else:
        print(f"No files found in album '{album}'")


def download_file(s3, bucket, key, path):
    obj = s3.get_object(Bucket=bucket, Key=key)
    filename = Path(key).name
    filepath = path / filename
    with filepath.open("wb") as file:
        file.write(obj["Body"].read())
    print(f"Downloaded {filename} to {path}")
