from argparse import ArgumentParser

from sab import constants


def generate_parser() -> ArgumentParser:
    parser = ArgumentParser(description=constants.PROGRAM_DESCRIPTION)
    optional = parser._action_groups.pop()
    optional.add_argument(
        "--debug", "-d", action="store_true", help="Starts debug mode"
    )
    optional.add_argument(
        "--publishers",
        "-p",
        nargs="+",
        help="Publishers to use. Can be more than 1",
        default=["twitter"],
        choices=constants.PUBLISHER_TYPES,
    )
    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "settings_file_path", type=str, help="Path to the settings file"
    )
    required.add_argument(
        "consumer",
        type=str,
        help="Consumer to use. Must be one",
        choices=constants.CONSUMER_TYPES,
    )
    parser._action_groups.append(optional)
    return parser


def parse_parameters():
    parser = generate_parser()
    return parser.parse_args()
