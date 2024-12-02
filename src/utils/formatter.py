from rich.text import Text
from rich.console import Console
from rich.markdown import Markdown

class RichConsole:
    def __init__(self):
        self.console = Console()
        
    def ask_input(self, prompt):
        return self.console.input(f"[bold cyan]\n{prompt}[/bold cyan] ").strip()

    def print_response(self, message, markdown=False):
        if markdown:
            self.console.print(Markdown(message))
        else:
            self.console.print(Text(message, style="bold magenta"))

    def print_code(self, code):
        self.console.print(Markdown(code, style="bold yellow"))

    def print_success(self, message):
        self.console.print(Text(message, style="bold green"))

    def print_error(self, message):
        self.console.print(Text(message, style="bold red"))

    def log(self, message):
        self.console.log(message, style="bold blue")

    def ask_confirmation(self, question):
        """Ask a yes/no question and return True/False."""
        response = self.console.input(f"[bold cyan]{question}[/bold cyan] ").strip().lower()
        return response in ['y', 'yes']
    
    def ask_input_number(self, prompt, min_value, max_value):
        """
        Prompts the user for a number input and validates it within the specified range.
        :param prompt: The prompt to display to the user.
        :param min_value: Minimum valid value.
        :param max_value: Maximum valid value.
        :return: Validated number input.
        """
        while True:
            response = self.ask_input(prompt)
            if response.isdigit():
                response = int(response)
                if min_value <= response <= max_value:
                    return response
            self.print_error(f"Please enter a valid number between {min_value} and {max_value}.")
