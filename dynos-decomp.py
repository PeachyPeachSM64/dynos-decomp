import os, sys
from src import prints
from src.commands import OPTIONS_TO_COMMANDS, is_compressed


def main(argv: list[str]):
    if len(argv) == 1:
        prints.usage(0)

    args = argv[1:]

    options = [arg for arg in args if arg.startswith('-') and arg in OPTIONS_TO_COMMANDS]
    file_args = [arg for arg in args if not arg.startswith('-')]

    if len(options) > 1:
        prints.error(f"Cannot combine multiple options: {options}")

    invalid_options = [arg for arg in args if arg.startswith('-') and arg not in OPTIONS_TO_COMMANDS]
    if invalid_options:
        prints.error(f"Invalid options: {invalid_options}")

    if len(file_args) < 1:
        prints.error("No file provided")

    if len(file_args) > 1:
        prints.error(f"Too many files provided: {file_args[1:]}")

    filepath = file_args[0].replace("\\", "/")
    if not os.path.isfile(filepath):
        prints.error(f"File `{filepath}` doesn't exist")

    with open(filepath, "rb") as f:
        data = f.read()

    option = options[0] if options else ("-d" if is_compressed(data) else "-c")

    OPTIONS_TO_COMMANDS[option](filepath, data)


if __name__ == "__main__":
    main(sys.argv)
