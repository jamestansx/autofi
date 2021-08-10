import argparse


def arg_cli():
    parser = argparse.ArgumentParser(
        prog="autofi-utem", description="A bot to automatically authenticate UTeM WiFi"
    )
    parser.add_argument(
        "-d",
        "--debug",
        dest="isDebug",
        action="store_true",
        default=False,
        help="Enable debug mode",
    )
    try:
        return parser.parse_args()
    except:
        return parser.parse_args([])
