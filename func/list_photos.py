import boto3

IMG_EXTENSIONS = [".jpg", ".jpeg"]


def get_albums(bucket_name, aws_access_key, aws_secret_access_key, endpoint_url, region):
    s3 = boto3.session.Session().client(
        's3', endpoint_url=endpoint_url, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )

    try:
        objects = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' not in objects:
            raise Exception("Bucket is empty or does not exist")

        unique_albums = set()
        for key in objects['Contents']:
            album_name = key['Key'].split('/')[0]
            if key['Key'].endswith("/") and album_name not in unique_albums:
                unique_albums.add(album_name)

        for album in unique_albums:
            print(album)
    except boto3.exceptions.Boto3Error as e:
        print(f"An error occurred: {e}")


def get_files(bucket_name, aws_access_key, aws_secret_access_key, album, endpoint_url, region):
    s3 = boto3.session.Session().resource(
        's3', endpoint_url=endpoint_url, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )
    my_bucket = s3.Bucket(bucket_name)

    count_objects = 0
    count_files = 0

    for obj in my_bucket.objects.filter(Prefix=f'{album}/'):
        count_objects += 1
        if any(obj.key.endswith(ext) for ext in IMG_EXTENSIONS):
            print(obj.key.split(f'{album}/')[1])
            count_files += 1

    if count_objects == 0:
        raise Exception(f"Album '{album}' does not exist")
    if count_files == 0:
        raise Exception(f"Album '{album}' does not have image files")
