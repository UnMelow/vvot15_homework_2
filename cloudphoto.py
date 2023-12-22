import argparse
import sys
import os
from func.manager import CloudPhotoManager


def execute_command(args, app_manager):
    """Execute the appropriate command based on parsed arguments."""
    command_functions = {
        'init': lambda: app_manager.init(input('bucket_name == '), input('aws_access_key_id == '),
                                         input('aws_secret_access_key == ')),
        'upload': lambda: app_manager.upload(args.album, args.path),
        'download': lambda: app_manager.download(args.album, args.path),
        'list': lambda: app_manager.list(args.album),
        'delete': lambda: app_manager.delete(args.album, args.photo),
        'mksite': app_manager.mksite
    }

    command_function = command_functions.get(args.command)
    if command_function:
        command_function()
        print(f"{args.command} done")
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)


def main():
    """Main function to parse arguments and call command execution."""
    parser = argparse.ArgumentParser(prog='cloudphoto')
    command_parser = parser.add_subparsers(title='command', dest='command')

    # Define parsers for each command
    init_parser = command_parser.add_parser('init', help='Config program')

    upload_parser = command_parser.add_parser('upload', help='Upload photos')
    upload_parser.add_argument('--album', required=True, help='Album name')
    upload_parser.add_argument('--path', default='.', help='Path to photo directory')

    download_parser = command_parser.add_parser('download', help="Download photos")
    download_parser.add_argument('--album', required=True, help='Photo album name')
    download_parser.add_argument('--path', default='.', help='Path to photo directory')

    list_parser = command_parser.add_parser('list', help='List photos and albums')
    list_parser.add_argument('--album', help='Album name')

    delete_parser = command_parser.add_parser('delete', help='Delete album or photo')
    delete_parser.add_argument('--album', required=True, help='Album name')
    delete_parser.add_argument('--photo', help='Photo name')

    mksite_parser = command_parser.add_parser('mksite', help='Make web site')

    args = parser.parse_args()

    app_manager = CloudPhotoManager(f"~{os.sep}.config{os.sep}cloudphoto{os.sep}cloudphotorc")

    try:
        execute_command(args, app_manager)
        sys.exit(os.EX_OK)
    except Exception as err:
        print(f"Error: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
