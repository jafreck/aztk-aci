import argparse
import warnings

from aztk_aci import error, version
from aztk_aci_cli import constants
from .logger import log, setup_logging
from .spark import spark


# Makes sure the warnings are displayed nicely in the CLI without a stacktrace
def _show_warn(message, *_args):
    log.warning(str(message))


def main():
    parser = argparse.ArgumentParser(prog=constants.CLI_EXE)

    setup_common_args(parser)

    subparsers = parser.add_subparsers(title="Available Softwares", dest="software", metavar="<software>")
    subparsers.required = True
    spark_parser = subparsers.add_parser("spark", help="Commands to run spark jobs")
    plugins_parser = subparsers.add_parser("plugins", help="Commands to list and view plugins")
    toolkit_parser = subparsers.add_parser("toolkit", help="List current toolkit information and browse available ones")

    spark.setup_parser(spark_parser)
    args = parser.parse_args()

    parse_common_args(args)

    try:
        run_software(args)
    # except batch_error.BatchErrorException as e:
    #     utils.print_batch_exception(e)
    except error.AztkError as e:
        log.error(str(e))


def setup_common_args(parser: argparse.ArgumentParser):
    parser.add_argument('--version', action='version', version=version.__version__)
    parser.add_argument("--verbose", action='store_true', help="Enable verbose logging.")


def parse_common_args(args):
    if args.verbose:
        setup_logging(True)
        log.debug("Verbose logging enabled")
    else:
        warnings.showwarning = _show_warn
        setup_logging(False)


def run_software(args):
    softwares = {}
    softwares["spark"] = spark.execute

    func = softwares[args.software]
    func(args)


if __name__ == '__main__':
    main()
