import argparse
import subprocess
from pathlib import Path


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir', type=Path)
    parser.add_argument('output_file', type=Path)

    return parser


def store_files(input_dir: Path, output_file: Path):
    output_file.parent.mkdir(exist_ok=True, parents=True)
    cmd = [
        'zip', '-0', '-r',
        str(output_file),
        str(input_dir),
    ]
    subprocess.check_call(cmd)

def main():
    parser = get_parser()
    args = parser.parse_args()

    store_files(args.input_dir, args.output_file)

if __name__ == '__main__':
    main()
