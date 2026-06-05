#textual
from textual.app import App,ComposeResult
from textual.containers import VerticalScroll, HorizontalGroup
from textual.widgets import Button, Footer, Header, DataTable
from textual import work
#local
from rich.text import Text
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
#local functions
from core.hosts import load_hosts
from core.hosts import load_hosts
from core.pinger import ping_all


class NetworkTool(App):
    CSS_PATH = "mainStyle.tcss"
    BINDINGS = [("d", "toggle_dark", "toggle_light")]
    hosts = []
    def __init__(self):
        super().__init__()
        all_hosts = load_hosts("hosts.txt")
        seen = set()
        self.hosts=[]
        self.duplicates = []
        for host in all_hosts:
            if host.address in seen:
                self.duplicates.append(host.address)
            else:
                seen.add(host.address)
                self.hosts.append(host)

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable()
        yield Button("Ping every host", id="pingAll")
        yield Button("Ping marked hosts", id="pingMarked")
        yield Footer()
    def action_toggle_dark(self) -> None:
        self.theme = (
                "textual-dark" if self.theme == "textual-light" else "textual-light"
                )
    def on_mount(self)->None:
        table = self.query_one(DataTable)
        table.add_column("Address", key="Address")
        table.add_column("Label", key="Label")
        table.add_column("TTL", key="TTL")
        table.add_column("Time", key="Time")
        table.add_column("Loss", key="Loss")
        table.add_column("Error", key="Error")       

        if self.duplicates:
            self.notify(f"Duplicate hosts skipped: {', '.join(self.duplicates)}", severity="warning")
      #hosts = load_hosts("hosts.txt")
        for host in self.hosts:
            table.add_row(host.address, host.label, "-", "-", "-", "", key=host.address)
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "pingAll":
            self.run_ping_all()

    @work(thread=True)
    def run_ping_all(self) -> None:
        results = ping_all(self.hosts)
        self.app.call_from_thread(self.update_table, results)

    def update_table(self, results) -> None:
        #self.notify(str(list(table.columns.keys())))
        table = self.query_one(DataTable)
        for host, pings in results.items():
            first = pings[0]
            if first.error:
                table.update_cell(host.address, "Error", "FAIL")
                table.update_cell(host.address, "TTL", "-")
                table.update_cell(host.address, "Time", "-")
                table.update_cell(host.address, "Loss", "100%")
                table.update_cell(host.address, "Error", Text("ERROR", style="bold red"))

            else:
                avg_time = sum(p.time for p in pings) / len(pings)
                table.update_cell(host.address, "TTL", str(first.ttl))
                table.update_cell(host.address, "Time", f"{avg_time:.1f}ms")
                table.update_cell(host.address, "Loss", f"{first.percentOfLossPackets}%")
                table.update_cell(host.address, "Error", "")
                table.update_cell(host.address, "Error", Text("OK", style="bold green"))

if __name__ == "__main__":
    app=NetworkTool()
    app.run()

