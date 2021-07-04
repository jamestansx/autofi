import argparse


def arg_cli():
    parser = argparse.ArgumentParser(
        prog="AutoFi-UTeM", description="A bot to automatically authenticate UTeM WiFi"
    )
    parser.add_argument(
        "-d",
        "--debug",
        dest="isDebug",
        action="store_true",
        default=False,
        help="Enable debug mode",
    )
    return parser.parse_args()
