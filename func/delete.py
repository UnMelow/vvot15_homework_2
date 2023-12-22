import boto3
from botocore.exceptions import ClientError


def delete_album(bucket_name, aws_access_key, aws_secret_access_key, album, endpoint_url, region):
    s3 = boto3.session.Session().resource(
        's3', endpoint_url=endpoint_url, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )
    my_bucket = s3.Bucket(bucket_name)

    try:
        my_bucket.Object(f'{album}/').load()  # Check if album exists
        for obj in my_bucket.objects.filter(Prefix=f'{album}/'):
            obj.delete()
        my_bucket.Object(f'{album}/').delete()  # Delete album directory
        print(f"Album '{album}' deleted.")
    except ClientError as e:
        raise Exception(f"Failed to delete album '{album}': {e}")


def delete_photo_in_album(bucket_name, aws_access_key, aws_secret_access_key, album, photo, endpoint_url, region):
    s3 = boto3.session.Session().resource(
        's3', endpoint_url=endpoint_url, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )
    my_bucket = s3.Bucket(bucket_name)
    photo_path = f'{album}/{photo}'

    try:
        my_bucket.Object(photo_path).load()  # Check if photo exists
        my_bucket.Object(photo_path).delete()
        print(f"Photo '{photo}' in album '{album}' deleted.")
    except ClientError as e:
        raise Exception(f"Failed to delete photo '{photo}' in album '{album}': {e}")
