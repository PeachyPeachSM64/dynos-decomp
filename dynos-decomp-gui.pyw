import os, re, sys
import itertools
import traceback
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import scrolledtext, filedialog, font, messagebox

from dataclasses import dataclass
from src import prints
from src.decomp import DECOMP_TABLE


WINDOW_TITLE = "DynOS Decomp"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

FILE_TYPES = [
    (info["name"], "*"+ext + (" *"+ext+".raw" if info["compressed"] else ""))
    for ext, info in DECOMP_TABLE.items()
]
FILE_TYPES.insert(0,
    ("DynOS compatible files", " ".join([pattern for _, pattern in FILE_TYPES]))
)
FILE_TYPES_PATTERNS = [
    (ext, [".*\\"+ext] + ([".*\\"+ext+"\\.raw"] if info["compressed"] else []))
    for ext, info in DECOMP_TABLE.items()
]
FILE_TYPES_ALL_PATTERNS = list(itertools.chain(*[patterns for _, patterns in FILE_TYPES_PATTERNS]))

COLOR_CODES_TO_TK_COLORS = {
    "\033[0;31m": "red",
    "\033[0;32m": "lime green",
    "\033[0;33m": "orange",
    "\033[0;34m": "blue",
    "\033[0;35m": "magenta",
    "\033[0;36m": "deep sky blue",
    "\033[0m": "reset",
}

BEHAVIOR_ASK_YES_NO_MESSAGE = "There are multiple behavior files (.bhv) queued for decompilation.\nWrite all behaviors in the same `behavior_data.c` file?"


@dataclass
class DynosDecompGUI:
    window: tk.Tk
    button_browse: tk.Button
    button_decomp: tk.Button
    button_clear_files: tk.Button
    button_clear_output: tk.Button
    listbox_files: tk.Listbox
    font_output: font.Font
    text_output: scrolledtext.ScrolledText


    # tkinter dnd drop event.data format is ass, so this is required (no regex can solve this)
    @staticmethod
    def get_files_from_drop_event(event) -> list:
        files_str = event.data
        files = []
        filepath = ""
        filepath_depth = 0
        for c in files_str:
            if c == '{':
                if filepath_depth > 0:
                    filepath_depth += 1
                elif not filepath:
                    filepath_depth = 1
                    continue            
            elif c == '}':
                if filepath_depth > 0:
                    filepath_depth -= 1
                    if filepath_depth == 0:
                        if filepath:
                            files.append(filepath)
                            filepath = ""
                        continue
            elif c == ' ' and filepath_depth == 0:
                if filepath:
                    files.append(filepath)
                    filepath = ""
                continue
            filepath += c
        if filepath:
            files.append(filepath)
        return files


    @staticmethod
    def normalize_filepath(filepath: str) -> str:
        return os.path.normpath(filepath).replace("\\", "/")


    def on_file_drop(self, event):
        files = DynosDecompGUI.get_files_from_drop_event(event)
        for file in files:
            for filepath in [os.path.join(file, f) for f in os.listdir(file)] if os.path.isdir(file) else [file]:
                if os.path.isfile(filepath) and any(re.match(pattern, filepath) for pattern in FILE_TYPES_ALL_PATTERNS):
                    self.listbox_files.insert(tk.END, DynosDecompGUI.normalize_filepath(filepath))


    def open_file_explorer(self):
        files = filedialog.askopenfilenames(filetypes=FILE_TYPES)
        for filepath in files:
            if os.path.isfile(filepath):
                self.listbox_files.insert(tk.END, DynosDecompGUI.normalize_filepath(filepath))


    def print_text(self, message: str, **kwargs):

        # Handle color codes
        tokens = []
        tag_color = None
        while True:
            cc_start = message.find("\033[")
            if cc_start == -1: break
            cc_end = message.find("m", cc_start)
            if cc_end == -1: break
            color_code = message[cc_start:cc_end + 1]
            message = message[:cc_start] + message[cc_end+1:]
            if color_code in COLOR_CODES_TO_TK_COLORS:
                tag = COLOR_CODES_TO_TK_COLORS[color_code]
                if ((tag == "reset" and tag_color is not None) or
                    (tag != "reset" and tag_color is not None and tag != tag_color)):
                    message = message[:cc_start]
                    tokens.append((message, tag_color))
                    message = message[cc_start:]
                    tag_color = None
                if tag != "reset":
                    tag_color = tag
        if message:
            tokens.append((message, None))

        # Print colored text to output and move cursor to the end
        self.text_output.config(state=tk.NORMAL)
        for token, tag_color in tokens:
            if tag_color is not None:
                tag_start = self.text_output.index(tk.END + "-1c")
                self.text_output.insert(tk.END, token)
                tag_end = self.text_output.index(tk.END + "-1c")
                self.text_output.tag_add(tag_color, tag_start, tag_end)
            else:
                self.text_output.insert(tk.END, token)
        self.text_output.insert(tk.END, kwargs["end"] if "end" in kwargs else "\n")
        self.text_output.config(state=tk.DISABLED)
        self.text_output.see(tk.END)


    def get_visible_chars_per_line(self) -> int:
        text_width_px = self.text_output.winfo_width()
        font_width_px = self.font_output.measure("0")
        return (text_width_px // font_width_px) - 1 if text_width_px > 0 else 0


    def lock_buttons(self):
        self.button_browse.config(state=tk.DISABLED)
        self.button_decomp.config(state=tk.DISABLED)
        self.button_clear_files.config(state=tk.DISABLED)
        self.button_clear_output.config(state=tk.DISABLED)
        self.listbox_files.config(state=tk.DISABLED)


    def unlock_buttons(self):
        self.button_browse.config(state=tk.NORMAL)
        self.button_decomp.config(state=tk.NORMAL)
        self.button_clear_files.config(state=tk.NORMAL)
        self.button_clear_output.config(state=tk.NORMAL)
        self.listbox_files.config(state=tk.NORMAL)


    def decomp_files(self):
        self.lock_buttons()
        kwargs = {}

        bhv_files_count = len([True for i in range(self.listbox_files.size()) if self.listbox_files.get(i).endswith(".bhv")])
        if bhv_files_count >= 2 and messagebox.askyesno(WINDOW_TITLE, BEHAVIOR_ASK_YES_NO_MESSAGE):
            behavior_data_filepath = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "behavior_data.c")
            kwargs["behavior_data_filepath"] = behavior_data_filepath
            try: os.remove(behavior_data_filepath)
            except: pass

        while self.listbox_files.size() > 0:
            filepath = self.listbox_files.get(0)
            max_width = self.get_visible_chars_per_line()
            self.print_text(
                "=" * max_width + "\n" +
                f"{filepath}\n" +
                "=" * max_width + "\n"
            )
            for ext, patterns in FILE_TYPES_PATTERNS:
                if any(re.match(pattern, filepath) for pattern in patterns):
                    DECOMP_TABLE[ext]["decomp"](filepath, **kwargs)
                    break
            self.text_output.update_idletasks()
            self.listbox_files.config(state=tk.NORMAL) # Not unlocking the listbox before deleting hangs the program. Oops!
            self.listbox_files.delete(0)
            self.listbox_files.config(state=tk.DISABLED)
            self.listbox_files.update_idletasks()
        self.unlock_buttons()


    def clear_files(self):
        self.listbox_files.delete(0, tk.END)


    def clear_output(self):
        self.text_output.config(state=tk.NORMAL)
        self.text_output.delete("1.0", tk.END)
        self.text_output.config(state=tk.DISABLED)


    def info(self, message: str, **kwargs):
        self.print_text(message, **kwargs)


    def warning(self, message: str, **kwargs):
        self.print_text(f"\033[0;33mWarning: {message}\033[0m", **kwargs)


    def error(self, message: str, **kwargs):
        self.print_text(f"\033[0;31mError: {message}\033[0m", **kwargs)


    def __init__(self):
        self.window = TkinterDnD.Tk()
        self.window.title(WINDOW_TITLE)
        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        icon = tk.PhotoImage(file="ico/icon.png")
        self.window.wm_iconphoto(False, icon)

        # Files browser
        layout_browser = tk.Frame(self.window, bg="lightgray")
        layout_browser.pack(fill=tk.X)

        label_drop = tk.Label(layout_browser, text="Drop files below...", bg="lightgray", height=1)
        label_drop.pack(side=tk.LEFT, padx=10, pady=5)

        self.button_browse = tk.Button(layout_browser, text="Browse file", command=lambda: self.open_file_explorer())
        self.button_browse.pack(side=tk.RIGHT, padx=(5, 10), pady=5)

        label_browse = tk.Label(layout_browser, text="...or browse file:", bg="lightgray", height=1)
        label_browse.pack(side=tk.RIGHT)

        # File list
        layout_files = tk.Frame(self.window)
        layout_files.pack(fill=tk.X)
    
        self.listbox_files = tk.Listbox(layout_files)
        self.listbox_files.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=5)
        self.listbox_files.drop_target_register(DND_FILES)
        self.listbox_files.dnd_bind('<<Drop>>', lambda event: self.on_file_drop(event))

        scrollbar_files = tk.Scrollbar(layout_files)
        scrollbar_files.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(0, 10), pady=5)
        scrollbar_files.config(command=self.listbox_files.yview)
        self.listbox_files.config(yscrollcommand=scrollbar_files.set)

        # Decomp/clear buttons
        layout_buttons = tk.Frame(self.window)
        layout_buttons.grid_columnconfigure(0, weight=1)
        layout_buttons.grid_columnconfigure(1, weight=1)
        layout_buttons.grid_columnconfigure(2, weight=1)
        layout_buttons.pack(fill=tk.X)

        layout_buttons_clear = tk.Frame(layout_buttons)
        layout_buttons_clear.grid_rowconfigure(0, weight=1)
        layout_buttons_clear.grid_rowconfigure(1, weight=1)
        layout_buttons_clear.grid(row=0, column=2, sticky=tk.E)

        font_decomp = font.Font(size=10, weight=font.BOLD)
        self.button_decomp = tk.Button(layout_buttons, text="Decomp files", width=15, height=2, font=font_decomp, command=lambda: self.decomp_files())
        self.button_decomp.grid(row=0, column=1)

        self.button_clear_files = tk.Button(layout_buttons_clear, text="Clear files", command=lambda: self.clear_files())
        self.button_clear_files.grid(row=0, column=0, sticky=tk.E, padx=(0, 10), pady=(5, 5))

        self.button_clear_output = tk.Button(layout_buttons_clear, text="Clear output", command=lambda: self.clear_output())
        self.button_clear_output.grid(row=1, column=0, sticky=tk.E, padx=(0, 10), pady=(5, 5))

        # Output log
        self.font_output = font.Font(family="Consolas", size=10)
        self.text_output = scrolledtext.ScrolledText(self.window, wrap=tk.CHAR, font=self.font_output)
        self.text_output.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        for tag in COLOR_CODES_TO_TK_COLORS.values():
            if tag != "reset":
                self.text_output.tag_config(tag, foreground=tag)
        self.text_output.config(state=tk.DISABLED)

        # Error handling
        def show_error(ex, gui: DynosDecompGUI, *args):
            err = traceback.format_exception(*args)
            gui.error("Exception: " + "".join(err))
            gui.unlock_buttons()
        tk.Tk.report_callback_exception = lambda ex, *args: show_error(ex, self, *args)

        # Replace prints functions
        prints.info = lambda message, **kwargs: self.info(message, **kwargs)
        prints.warning = lambda message, **kwargs: self.warning(message, **kwargs)
        prints.error = lambda message, **kwargs: self.error(message, **kwargs)


    def mainloop(self):
        self.window.mainloop()


if __name__ == "__main__":
    gui = DynosDecompGUI()
    gui.mainloop()
