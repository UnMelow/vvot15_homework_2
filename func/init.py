import boto3
from botocore.exceptions import ClientError


def make_bucket(bucket_name, aws_access_key, aws_secret_access_key, endpoint_url, region):
    session = boto3.session.Session()
    s3 = session.client(
        's3', endpoint_url=endpoint_url, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )

    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists.")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            try:
                s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region},
                                 ACL='public-read')
                print(f"Bucket '{bucket_name}' created.")
            except ClientError as e:
                print(f"Failed to create bucket: {e}")
        else:
            print(f"Failed to check bucket existence: {e}")
