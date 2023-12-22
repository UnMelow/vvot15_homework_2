import fileinput
import os
from pathlib import Path

from func.init import make_bucket
from func.delete import delete_photo_in_album, delete_album
from func.download import download_album
from func.list_photos import get_files, get_albums
from func.mksite import mksite_album
from func.upload import upload_album


class CloudPhotoManager:
    def __init__(self, config_file):
        self.config_file = Path(os.path.expanduser(config_file))
        self.ensure_config_file_exists()
        self.bucket, self.aws_access_key_id, self.aws_secret_access_key, self.endpoint_url, self.region = self.get_params()

    def ensure_config_file_exists(self):
        """Ensure that the configuration file exists."""
        config_directory = self.config_file.parent
        if not config_directory.exists():
            config_directory.mkdir(parents=True)
        if not self.config_file.exists():
            with self.config_file.open('w') as file:
                file.write('bucket = INPUT_BUCKET_NAME\n')
                file.write('aws_access_key_id = INPUT_AWS_ACCESS_KEY_ID\n')
                file.write('aws_secret_access_key = INPUT_AWS_SECRET_ACCESS_KEY\n')
                file.write('endpoint_url = INPUT_ENDPOINT_URL\n')
                file.write('region = INPUT_REGION\n')

    def get_params(self):
        """Retrieve and validate parameters from the configuration file."""
        config = {}
        with self.config_file.open('r') as file:
            for line in file:
                name, value = line.strip().split(' = ', 1)
                config[name] = value

        return config['bucket'], config['aws_access_key_id'], config['aws_secret_access_key'], config['endpoint_url'], \
            config['region']

    def init(self, bucket_name, aws_access_key, aws_secret_access_key):
        """Initialize the cloud photo manager with the provided credentials."""
        replacements = {
            "INPUT_BUCKET_NAME": bucket_name,
            "INPUT_AWS_ACCESS_KEY_ID": aws_access_key,
            "INPUT_AWS_SECRET_ACCESS_KEY": aws_secret_access_key
        }
        with fileinput.FileInput(self.config_file, inplace=True) as file:
            for line in file:
                for old, new in replacements.items():
                    line = line.replace(old, new)
                print(line, end='')

        make_bucket(bucket_name, aws_access_key, aws_secret_access_key, self.endpoint_url, self.region)

    def upload(self, album, path):
        upload_album(self.bucket, self.aws_access_key_id, self.aws_secret_access_key, album, path, self.endpoint_url,
                     self.region)

    def download(self, album, path):
        download_album(self.bucket, self.aws_access_key_id, self.aws_secret_access_key, album, path, self.endpoint_url,
                       self.region)

    def list(self, album=None):
        if album is None:
            get_albums(self.bucket, self.aws_access_key_id, self.aws_secret_access_key, self.endpoint_url, self.region)
        else:
            get_files(self.bucket, self.aws_access_key_id, self.aws_secret_access_key, album, self.endpoint_url,
                      self.region)

    def delete(self, album, photo=None):
        if photo is None:
            delete_album(self.bucket, self.aws_access_key_id, self.aws_secret_access_key, album, self.endpoint_url,
                         self.region)
        else:
            delete_photo_in_album(self.bucket, self.aws_access_key_id, self.aws_secret_access_key, album, photo,
                                  self.endpoint_url, self.region)

    def mksite(self):
        mksite_album(self.bucket, self.aws_access_key_id, self.aws_secret_access_key, self.endpoint_url, self.region)
