import argparse


def generate_parser():
    # TODO: Add description
    parser = argparse.ArgumentParser()
    optional = parser._action_groups.pop()
    optional.add_argument(
        "--debug",
        "-d",
        action='store_true',
        help="Starts debug mode"
    )
    optional.add_argument(
        "--consumer",
        "-c",
        type=str,
        help="Consumer to use (trovo, twitch)"
    )
    required = parser.add_argument_group('required arguments')
    required.add_argument(
        'settings_file_path',
        type=str,
        help="Path to the settings file"
    )
    parser._action_groups.append(optional)
    return parser


def parse_parameters():
    parser = generate_parser()
    return parser.parse_args()
