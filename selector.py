from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import ListView, ListItem, Static, Button
from textual.binding import Binding

class TwoPaneApp(App):
    CSS = """
    #list_pane {
        width: 30%;
        border: solid $primary;
    }
    
    #info_pane {
        width: 70%;
        border: solid $primary;
        padding: 1;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]
    
    def __init__(self):
        super().__init__()
        self.data = {
            "item1": "This is the content for item 1\nIt can be multiple lines",
            "item2": "Content for item 2\nWith some more details here",
            "item3": "Item 3 information\nAnother line\nAnd another",
            "another_key": "Some other data\nWith multiple\nLines of text",
            "last_item": "Final item content"
        }
    
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Button("Click me!", id="my_button")
            with Horizontal():
                # List pane
                yield ListView(id="list_pane")
                
                # Info pane
                yield Static("Select an item from the list", id="info_pane")
    
    def on_mount(self) -> None:
        """Populate the list after mounting."""
        list_view = self.query_one("#list_pane", ListView)
        for key in self.data.keys():
            list_view.append(ListItem(Static(key)))
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle list selection."""
        selected_text = event.item.children[0].renderable
        info_content = self.data.get(selected_text, "No content available")
        info_pane = self.query_one("#info_pane", Static)
        info_pane.update(info_content)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "my_button":
            info_pane = self.query_one("#info_pane", Static)
            info_pane.update("Button was clicked!")

if __name__ == "__main__":
    TwoPaneApp().run()
