import argparse

def generate_parser():
    # TODO: Add description
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    required.add_argument(
        'settings_file_path',
        type=str,
        help="path to the settings file",
    )

    return parser

def parse_parameters():
    parser = generate_parser()
    return parser.parse_args()
