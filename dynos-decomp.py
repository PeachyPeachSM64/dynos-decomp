import os, sys
from src.commands import OPTIONS_TO_COMMANDS, usage, error, is_compressed


def main(argv: list[str]):
    if len(argv) == 1:
        usage(0)

    options = list(filter(lambda x: x in OPTIONS_TO_COMMANDS, argv))

    if len(options) > 1:
        error(f"Cannot combine multiple options: {options}")

    args = list(filter(lambda x: x not in OPTIONS_TO_COMMANDS, argv))
    invalid_options = list(filter(lambda x: x.startswith("-"), args))

    if invalid_options:
        error(f"Invalid options: {invalid_options}")

    if len(args) < 2:
        error(f"No file provided")

    if len(args) > 2:
        error(f"Too much files provided: {args[1:]}")

    filepath = args[1].replace("\\", "/")
    if not os.path.isfile(filepath):
        error(f"File `{filepath}` doesn't exist")

    with open(filepath, "rb") as f:
        data = f.read()
    option = options[0] if options else ("-e" if is_compressed(data) else "-c")

    OPTIONS_TO_COMMANDS[option](filepath, data)


if __name__ == "__main__":
    main(sys.argv)
