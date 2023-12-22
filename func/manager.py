import fileinput
import os
from func.init import make_bucket
from func.delete import delete_photo_in_album, delete_album
from func.download import download_album
from func.list_photos import get_files, get_albums
from func.mksite import mksite_album
from func.upload import upload_album


def get_params(file_path):
    """Retrieve and validate parameters from the configuration file."""

    config = {}
    with open(os.path.expanduser(file_path), 'r') as file:
        for line in file:
            name, value = line.strip().split(' = ', 1)
            config[name] = value

    if any(value.startswith("INPUT_") for value in config.values()):
        raise Exception("Config file is not valid")

    return config['bucket'], config['aws_access_key_id'], config['aws_secret_access_key'], config['endpoint_url'], \
        config['region']


class CloudPhotoManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.bucket, self.aws_access_key_id, self.aws_secret_access_key, self.endpoint_url, self.region = get_params(
            file_path)

    def init(self, bucket_name, aws_access_key, aws_secret_access_key):
        """Initialize the cloud photo manager with the provided credentials."""
        replacements = {
            "INPUT_BUCKET_NAME": bucket_name,
            "INPUT_AWS_ACCESS_KEY_ID": aws_access_key,
            "INPUT_AWS_SECRET_ACCESS_KEY": aws_secret_access_key
        }
        with fileinput.FileInput(os.path.expanduser(self.file_path), inplace=True) as file:
            for line in file:
                for old, new in replacements.items():
                    line = line.replace(old, new)
                print(line, end='')

        make_bucket(bucket_name, aws_access_key, aws_secret_access_key, self.endpoint_url, self.region)

    def upload(self, album, path):
        """Upload an album to the configured S3 bucket."""
        upload_album(self.bucket, self.aws_access_key_id, self.aws_secret_access_key, album, path, self.endpoint_url,
                     self.region)

    def download(self, album, path):
        """Download an album from the configured S3 bucket."""
        download_album(self.bucket, self.aws_access_key_id, self.aws_secret_access_key, album, path, self.endpoint_url,
                       self.region)

    def list(self, album=None):
        """List albums or photos from the configured S3 bucket."""
        if album is None:
            get_albums(self.bucket, self.aws_access_key_id, self.aws_secret_access_key, self.endpoint_url, self.region)
        else:
            get_files(self.bucket, self.aws_access_key_id, self.aws_secret_access_key, album, self.endpoint_url,
                      self.region)

    def delete(self, album, photo=None):
        """Delete an album or a photo on the album from the configured S3 bucket."""
        if photo is None:
            delete_album(self.bucket, self.aws_access_key_id, self.aws_secret_access_key, album, self.endpoint_url,
                         self.region)
        else:
            delete_photo_in_album(self.bucket, self.aws_access_key_id, self.aws_secret_access_key, album, photo,
                                  self.endpoint_url, self.region)

    def mksite(self):
        """Generate a static website from the albums in the configured S3 bucket."""
        mksite_album(self.bucket, self.aws_access_key_id, self.aws_secret_access_key, self.endpoint_url, self.region)
