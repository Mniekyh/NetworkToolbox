from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.widgets import Button, Digits, Footer, Header

class TimeDisplay(Digits):
    """A widget to display elapsed time."""
class Stopwatch(HorizontalGroup):
    "** Stopwatch class **"
    def compose(self) -> ComposeResult:
        "** Create child widgets of stopwatch **"
        yield Button("Start", id="start", variant="success") 
        "yield smth u want to show in console, give it text, give it id (like in css), and choose class for this from framework (like bootstrap)"
        yield Button ("Stop", id="stop", variant="error")      
        yield Button ("Reset", id="reset")
        yield TimeDisplay("00:00:00.00")
class StopwatchApp(App):

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        "** create visual of app **"
        yield Header()
        yield Footer()
        yield VerticalScroll(Stopwatch(), Stopwatch(), Stopwatch())

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

if __name__ == "__main__":
    app = StopwatchApp()
    app.run()
