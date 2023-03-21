from typing import ClassVar
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Button, Header, Footer, Static
from textual.reactive import reactive
from textual.widgets import Input, Label
from textual.containers import Horizontal, Vertical
from textual.binding import Binding

import datetime


class Minput(Input):

    BINDINGS = [
        Binding("shift-enter", "section", "New section", show=False),
    ] + Input.BINDINGS

    def __init__(self, log_file, **kwargs) -> None:
        super().__init__(**kwargs)
        self.value = ""
        self.password = True
        self.log_file = log_file

    def handle_word(self):
        self.log_file.write(self.value+" ")
        self.value = ""

    def handle_line(self):
        self.log_file.write(f"\n")

    def action_submit(self) -> None:
        self.handle_word()
        self.handle_line()

    def insert_text_at_cursor(self, text: str) -> None:
        if text == " ":
            self.handle_word()
        else:
            super().insert_text_at_cursor(text)

    def action_section(self) -> None:
        self.handle_word()
        self.handle_line()
        self.log_file.write(f"\n@Datetime({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")


class MindStreamApp(App):

    CSS_PATH = "mindstream.css"

    def __init__(self, log_file, **kwargs) -> None:
        super().__init__(**kwargs)
        self.log_file = log_file
        
    def on_mount(self) -> None:
        input = self.query_one("Input")
        input.focus()

    def compose(self) -> ComposeResult:
        yield Minput(self.log_file)

def main():
    with open("mindstream.log", "a", encoding='utf-8') as f:
        f.write(f"@Datetime({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
        app = MindStreamApp(f)
        app.run()
        f.write("\n")

if __name__ == "__main__":
    main()