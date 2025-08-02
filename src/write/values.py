def define_command(name: str, argnames: str, *commands) -> dict:
    args = []
    for argname in argnames.split(","):
        for index, command in enumerate(commands):
            for x in command:
                if isinstance(x["value"], str):
                    xname = x["value"]
                    xtype = "u"
                    sep = xname.find(":")
                    if sep != -1:
                        xtype = xname[sep+1:]
                        xname = xname[:sep]
                    if xname == argname.strip():
                        args.append({
                            "index": index,
                            "value": xname,
                            "type": xtype,
                            **{ k: v for k, v in x.items() if k != "value" }
                        })
    return {
        "name": name,
        "cmd": commands[0][0]["value"],
        "size": len(commands),
        "args": args
    }


def bnot(x: int, bits: int) -> int:
    mask = ((1 << bits) - 1)
    return mask - (x & mask)


def get_pointer_and_offset(ptr: str) -> tuple[str, int]:
    if isinstance(ptr, int):
        return "NULL", 0
    if "+" in ptr:
        name, off = [x.strip() for x in ptr.split("+")]
        return name, int(off)
    return ptr.strip(), 0


def get_named_flags(flags: int, flagdict: dict[int, str]) -> str:
    params = []
    for flag, param in flagdict.items():
        if (flags & flag) == flag:
            params.append(param)
            flags &= bnot(flag, 32)
    if flags != 0:
        params.append(f"0x{flags:X}")
    return "|".join(params) if params else "0"


def value_to_str(value: int, shift: int, width: int, argtype: str) -> str:
    limit = (1 << width)
    value = ((value >> shift) & (limit - 1))

    # Signed value
    if argtype == "s":
        half = (limit >> 1)
        value = value if value < half else value - limit

    # (Hexa)decimal
    return ("0x%X" if argtype == "x" else "%d") % (value)

