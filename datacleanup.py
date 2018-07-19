import os

import click


@click.command()
@click.argument('directory', type=click.Path(exists=True), required=True)
def cleanup(directory):
    directory = directory.rstrip('/')
    base = os.path.basename(directory)
    files = os.listdir(directory)
    for i, f in enumerate(files):
        root, ext = os.path.splitext(f)
        print(f'renaming {f}')
        os.rename(os.path.join(directory, f), os.path.join(directory, f'{base}.{i}{ext}'))


if __name__ == "__main__":
    cleanup()