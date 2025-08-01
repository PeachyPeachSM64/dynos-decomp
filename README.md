```
  ______  ___  _  __  ____
  \   \ \/ / \| |/  \/ __/
   | D \  /| \\ | () \__ \
  /___//_/ |_|\_|\__/____/
        D E C O M P
```

A GUI made in Python to decompile DynOS binary files.

## Installation

- Make sure Python is installed in your system (if not, go to https://www.python.org/downloads/)
- Clone or download this repository
- Launch `dynos-decomp-gui.pyw`

## How to use

<img src="howto.png" alt="drawing" width="500"/>

## Supported file formats

- Actor files (`.bin`, `.bin.raw`)
- Texture files (`.tex`)

## Troubleshooting

If the program doesn't start, you might need to install some Python packages:
- Open a terminal (on Windows: press `[Ctrl] + [R]`, input `cmd` then hit `[Enter]`)
- Run this command: `pip install -U tkinterdnd2 pypng`
- Close the terminal and launch the program again

## Progress

- actors: DONE
- textures: DONE
- behaviors: 1%
- collisions: 0%
- levels: 0%
