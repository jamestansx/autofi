import argparse


def arg_cli():
    parser = argparse.ArgumentParser(
        prog="AutoFi-UTeM", description="A bot to automatically authenticate UTeM WiFi"
    )
    parser.add_argument(
        "--debug",
        "-d",
        dest="isDebug",
        action="store_true",
        default=False,
        help="Enable debug mode",
    )
    args = parser.parse_args()

    return args
