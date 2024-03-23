from rich.segment import Segment
from rich.style import Style

from textual.app import App, ComposeResult
from textual.strip import Strip
from textual.widget import Widget
from textual.widgets import Log
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static, Placeholder
from textual.reactive import reactive

from client import client_settings

class MainDisplay(Static):
    CSS_PATH = "maindisplay.tcss"

    current_update = reactive([['1', '2', '3', '1', '2', '3', '1', '2', '3'],
                               ['1', '2', '3', '1', '2', '3', '1', '2', '3'],
                               ['1', '2', '3', '1', '2', '3', '1', '2', '3'],
                               ['1', '2', '3', '1', '2', '3', '1', '2', '3'],
                               ['1', '2', '3', '1', '2', '3', '1', '2', '3'],
                               ['1', '2', '3', '1', '2', '3', '1', '2', '3'],
                               ['1', '2', '3', '1', '2', '3', '1', '2', '3'],
                               ['1', '2', '3', '1', '2', '3', '1', '2', '3'],
                               ['1', '2', '3', '1', '2', '3', '1', '2', '3']])

    def on_mount(self):
        self.set_interval(
            1/10,
            self.update_update
        )

    def update_update(self):
        self.current_update = client_settings.update

    def compose(self) -> ComposeResult:
        yield Vertical(
            Horizontal(
                Static(self.current_update[0][0], classes="box"),
                Static(self.current_update[0][1], classes="box"),
                Static(self.current_update[0][2], classes="box"),
                Static(self.current_update[0][3], classes="box"),
                Static(self.current_update[0][4], classes="box"),
                Static(self.current_update[0][5], classes="box"),
                Static(self.current_update[0][6], classes="box"),
                Static(self.current_update[0][7], classes="box"),
                Static(self.current_update[0][8], classes="box"),
                classes="display_row"),
            Horizontal(
                Static(self.current_update[1][0], classes="box"),
                Static(self.current_update[1][1], classes="box"),
                Static(self.current_update[1][2], classes="box"),
                Static(self.current_update[1][3], classes="box"),
                Static(self.current_update[1][4], classes="box"),
                Static(self.current_update[1][5], classes="box"),
                Static(self.current_update[1][6], classes="box"),
                Static(self.current_update[1][7], classes="box"),
                Static(self.current_update[1][8], classes="box"),
                classes="display_row"),
            Horizontal(
                Static(self.current_update[2][0], classes="box"),
                Static(self.current_update[2][1], classes="box"),
                Static(self.current_update[2][2], classes="box"),
                Static(self.current_update[2][3], classes="box"),
                Static(self.current_update[2][4], classes="box"),
                Static(self.current_update[2][5], classes="box"),
                Static(self.current_update[2][6], classes="box"),
                Static(self.current_update[2][7], classes="box"),
                Static(self.current_update[2][8], classes="box"),
                classes="display_row"),
            Horizontal(
                Static(self.current_update[3][0], classes="box"),
                Static(self.current_update[3][1], classes="box"),
                Static(self.current_update[3][2], classes="box"),
                Static(self.current_update[3][3], classes="box"),
                Static(self.current_update[3][4], classes="box"),
                Static(self.current_update[3][5], classes="box"),
                Static(self.current_update[3][6], classes="box"),
                Static(self.current_update[3][7], classes="box"),
                Static(self.current_update[3][8], classes="box"),
                classes="display_row"),
            Horizontal(
                Static(self.current_update[4][0], classes="box"),
                Static(self.current_update[4][1], classes="box"),
                Static(self.current_update[4][2], classes="box"),
                Static(self.current_update[4][3], classes="box"),
                Static(self.current_update[4][4], classes="box"),
                Static(self.current_update[4][5], classes="box"),
                Static(self.current_update[4][6], classes="box"),
                Static(self.current_update[4][7], classes="box"),
                Static(self.current_update[4][8], classes="box"),
                classes="display_row"),
            Horizontal(
                Static(self.current_update[5][0], classes="box"),
                Static(self.current_update[5][1], classes="box"),
                Static(self.current_update[5][2], classes="box"),
                Static(self.current_update[5][3], classes="box"),
                Static(self.current_update[5][4], classes="box"),
                Static(self.current_update[5][5], classes="box"),
                Static(self.current_update[5][6], classes="box"),
                Static(self.current_update[5][7], classes="box"),
                Static(self.current_update[5][8], classes="box"),
                classes="display_row"),
            Horizontal(
                Static(self.current_update[6][0], classes="box"),
                Static(self.current_update[6][1], classes="box"),
                Static(self.current_update[6][2], classes="box"),
                Static(self.current_update[6][3], classes="box"),
                Static(self.current_update[6][4], classes="box"),
                Static(self.current_update[6][5], classes="box"),
                Static(self.current_update[6][6], classes="box"),
                Static(self.current_update[6][7], classes="box"),
                Static(self.current_update[6][8], classes="box"),
                classes="display_row"),
            Horizontal(
                Static(self.current_update[7][0], classes="box"),
                Static(self.current_update[7][1], classes="box"),
                Static(self.current_update[7][2], classes="box"),
                Static(self.current_update[7][3], classes="box"),
                Static(self.current_update[7][4], classes="box"),
                Static(self.current_update[7][5], classes="box"),
                Static(self.current_update[7][6], classes="box"),
                Static(self.current_update[7][7], classes="box"),
                Static(self.current_update[7][8], classes="box"),
                classes="display_row"),
            Horizontal(
                Static(self.current_update[8][0], classes="box"),
                Static(self.current_update[8][1], classes="box"),
                Static(self.current_update[8][2], classes="box"),
                Static(self.current_update[8][3], classes="box"),
                Static(self.current_update[8][4], classes="box"),
                Static(self.current_update[8][5], classes="box"),
                Static(self.current_update[8][6], classes="box"),
                Static(self.current_update[8][7], classes="box"),
                Static(self.current_update[8][8], classes="box"),
                classes="display_row"),
                classes="display_container"
        )


class InfoBox(Widget):
    CSS_PATH = "maindisplay.tcss"
    def compose(self) -> ComposeResult:

        yield Vertical(

        )

class ChatBox(Widget):
    CSS_PATH = "maindisplay.tcss"
    def compose(self) -> ComposeResult:
        yield Vertical(
            Log("hello", classes="log"),
            classes="chatbox_container"
        )

class ClientUI(App):
    CSS_PATH = "maindisplay.tcss"

    def compose(self) -> ComposeResult: 

        yield Horizontal(
            Vertical(
                MainDisplay(),
                ChatBox()
            ),
            Vertical(
                InfoBox(),
                classes="infobox_container"
            )
        )
        
        


clientUI = ClientUI()

clientUI.run()