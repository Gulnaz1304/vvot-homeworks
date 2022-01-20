import argparse
from src.ya_cloud import bucket
import os


CMD_UPLOAD = 'upload'
CMD_DOWNLOAD = 'download'
CMD_LIST = 'list' 
ALLOWED_EXTENTIONS = [
    '.jpg', '.jpeg'
]

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', choices=[CMD_UPLOAD, CMD_DOWNLOAD, CMD_LIST])
    parser.add_argument('-a', '--album')
    parser.add_argument('-p', '--path')
    return parser.parse_args()


def main():
    args = parse_args()
    if args.cmd == CMD_DOWNLOAD:
        download(args.path, args.album)
    elif args.cmd == CMD_UPLOAD:
        upload(args.path, args.album)
    elif args.cmd == CMD_LIST:
        if args.album:
            list_files(args.album)
        else:
            list_albums()
    else:
        print(f'unknow command {args.cmd}')


def upload(path, album):
    files = list(filter(
        lambda file: file.is_file() and os.path.splitext(file.path)[-1] in ALLOWED_EXTENTIONS,
        os.scandir(path),
    ))
    if not files:
        print(f'No files in dir {path}')
    for file in files:
        with open(file.path, 'rb') as f:
            filename = os.path.basename(file.path)
            bucket.upload_fileobj(f, f'{album}/{filename}')
            print(f'{file.path} done')

def _get_all():
    return list(bucket.objects.all())

def _is_dir(f: str) -> bool:
    return '/' in f

def _get_album_name(f: str) -> str:
    album, _ = f.rsplit('/', 2)
    return album

def _get_file_name(f: str) -> str:
    _, filename = f.rsplit('/', 2)
    return filename


def _get_files(album: str):
    files = _get_all()
    files = filter(lambda f: _get_album_name(f.key) == album, files)
    return list(map(lambda f: _get_file_name(f.key), files))
    

def _pprint_objects(objs):
    for i, obj in enumerate(sorted(objs)):
            print(f'#{i + 1}. {obj}')
    
def list_files(album: str):
    filenames = _get_files(album)
    if not filenames:
        print('Album does not exist')
    else:
        _pprint_objects(filenames)


def _get_albums():
    files = _get_all()
    files = filter(lambda f: f.size > 0 and _is_dir(f.key), files)
    albums = map(lambda f: _get_album_name(f.key), files)
    return set(albums) 


def list_albums():
    albums = _get_albums()
    if not albums:
        print('No albums.')
    else:
        _pprint_objects(albums)

def download(path, album):
    files = list(bucket.objects.filter(Prefix=album + '/'))
    if not files:
        print('album does not exist')
    else:
        for file in files:
            filename = f'{path}/{_get_file_name(file.key)}'
            content = file.get()
            print(f'{filename} downloaded')
            with open(filename, 'wb') as f:
                f.write(content['Body'].read())



if __name__ == '__main__':
    main()