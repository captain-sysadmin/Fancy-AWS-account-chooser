from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import ListView, ListItem, Static, Button
from textual.binding import Binding

import os
import configparser
import subprocess

config = configparser.ConfigParser()
aws_conf_path = os.path.expanduser("~/.aws/config")

accounts = config.read(aws_conf_path)
if accounts == []:
    raise ValueError(f"Cannot find aws config at {aws_conf_path}")


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
    #main_content {
        height: 80%;
    }
    #control_buttons {
        width: 100%;
        border: solid $primary;
        padding: 1; 
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self.data = {"last_item": "Final item content"}
        self.selected_aws_account = ""
        self.load_aws_accounts()

    def load_aws_accounts(self) -> None:
        """This finds the local AWS config file and
        tries to pull out the accounts that we can request
        ephemeral creds for
        """

        config = configparser.ConfigParser()
        aws_conf_path = os.path.expanduser("~/.aws/config")

        accounts = config.read(aws_conf_path)
        if accounts == []:
            raise ValueError(f"Cannot find aws config at {aws_conf_path}")
        for profile in config.sections():
            nice_name = profile.replace("profile ", "")
            if config[profile].get("sso_session", None):
                self.data[nice_name] = (
                    f"Aws account ID: {config[profile].get('sso_account_id', 'broken')}"
                )

    def retrieve_creds(self, account_name: str) -> bool:
        """renew the credentials for a given account,
        this uses subprocess, so might be a bit shit"""

        print(f"fart {account_name}")
        output = subprocess.run(
            f"aws sso login --profile {account_name}", shell=True, capture_output=True
        )
        if output.returncode == 0:
            return True
        else:
            return False

    def set_default_profile(self, account_name: str) -> None:
        """update the env and shell to point default account to which ever one we just
        got creds for
        """
        with open(os.path.expanduser("~/.aws_includes"), "w") as fh:
            fh.write(f'export AWS_DEFAULT_PROFILE="{account_name}"\n')

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal(id="main_content"):
                # List pane
                list_view = ListView(id="list_pane")
                list_view.border_title = "Items"
                yield list_view

                # Info pane
                info_pane = Static("Select an item from the list", id="info_pane")
                info_pane.border_title = "Details"
                yield info_pane
            with Horizontal(id="Control_buttons"):
                yield Button("Get AWS credentials", id="get_creds")
                yield Button("Quit", id="quit_button")

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
        if event.button.id == "get_creds":
            list_view = self.query_one("#list_pane", ListView)
            selected_item = list_view.highlighted_child
            selected_account = selected_item.children[0].renderable
            info_pane = self.query_one("#info_pane", Static)
            info_pane.update(
                f"Getting SSO credentials for {selected_account}, this will launch a browser window"
            )
            working = self.retrieve_creds(selected_account)
            if not working:
                info_pane.update("Could not get creds.")
            else:
                info_pane.update("WE HAVE CREDENTIALS, Quitting")
                self.set_default_profile(selected_account)
                self.exit()
        if event.button.id == "quit_button":
            self.exit()


if __name__ == "__main__":
    TwoPaneApp().run()
