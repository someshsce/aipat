import os
import sys
import click
from rich.align import Align
from aipatt.ai.llm import LLM
from dotenv import load_dotenv
from rich.console import Console
from aipatt.utils.formatter import RichConsole
from aipatt.utils.youtube import YoutubeSearch
from aipatt.utils.executor import ShellExecutor
from aipatt.utils.google_search import google_search
from aipatt.config import setup_config, update_config
from aipatt.utils.email import EmailInput, compose_and_send_email
from importlib.metadata import version as get_version, PackageNotFoundError

console = RichConsole()
console2 = Console()

def check_and_load_config():
    """Check if the configuration file exists, if not, prompt the user to create it."""
    env_path = os.path.join(os.path.expanduser("~"), ".aipatt.env")
    if not os.path.exists(env_path):
        setup_config(env_path)
    else:
        load_dotenv(env_path)

@click.group(
    invoke_without_command=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.pass_context
@click.option('-c', '--code', is_flag=True, help="Generate Code.")
@click.option('-ch', '--chat', is_flag=True, help="Continious Chat with the AI.")
@click.option('-s', '--shell', is_flag=True, help="Generate and Execute shell commands.")
@click.option('-y', '--youtube', is_flag=True, help="To Search and Play YouTube Videos.")
@click.option('-gs', '--gsearch', is_flag=True, help="To Search on Google and Summarize it by an AI.")
@click.option('-m', '--mail', is_flag=True, help="To Compose an Email by an AI and Send.")
@click.option('-cm', '--clear-memory', is_flag=True, help="Clear the whole chat memory.")
@click.option('-v', '--version', 'show_version', is_flag=True, help="Print version.")
@click.option('-u', '--update-config', 'update_configuration', is_flag=True, help="Update the configuration settings.")
@click.option('-h', '--help', 'show_help', is_flag=True, help="Print help message.")
@click.argument('query', required=False, default=None)

def cli(ctx, shell, code, chat, youtube, mail, gsearch, clear_memory, show_version, show_help, query, update_configuration):
    """
    AIPATT: AI Powered Assistant Tool for Terminals
    """
    if update_configuration:
        env_path = os.path.join(os.path.expanduser("~"), ".aipatt.env")
        update_config(env_path)
        sys.exit(0)

    if show_version:
        try:
            package_version = get_version("aipatt")
            console.print_success(f"AIPATT version {package_version}")
        except PackageNotFoundError:
            console.print_error("Version information not available.")
        sys.exit(0)

    if show_help:
        console2.print(Align(f"[bold green]Welcome to AIPATT: AI Powered Assistant Tool for Terminals[/bold green]", align="center"))
        console2.print("""
[bold yellow]Usage:[/bold yellow] aipatt [OPTIONS] [QUERY]

[bold yellow]Options:[/bold yellow]
-c,     --code                                     Generate Code.
-ch     --chat                                     Continious Chat with the AI.
-y,     --youtube                                  To Search and Play YouTube Videos.
-s,     --shell                                    Generate and Execute shell commands.
-m,     --mail                                     To Compose an Email by an AI and Send.
-gs,    --gsearch                                  To Search on Google and Summarize it by an AI.
-u,     --update-config                            Update the configuration settings.
-cm,    --clear-memory                             To clear the whole chat memory.
-v,     --version                                  Print version of AIPATT.
-h,     --help                                     Print help message.

[bold yellow]Examples:[/bold yellow]
aipatt "What is internet?"
aipatt "Latest news about AI"
aipatt -y "Top Python tutorials"
aipatt -s "How to update my system?"
cat install.sh | aipatt "Explain the code"
aipatt -gs "What is the capital of France?"
aipatt "Current Weather Condition of New York"
aipatt -c "Write a Python script for Fibonacci series"
aipatt -m "Send email to example@gmail.com, Meeting at 10 AM"
            """)
        sys.exit(0)

    check_and_load_config()

    handler = LLM()

    if clear_memory:
        memories = handler.get_memory()
        count = len(memories)
        handler.clear_memory()
        console.print_success(f"Memory cleared. Removed {count} entries.")
        return

    if not ctx.invoked_subcommand:
        if not query and sys.stdin.isatty():
            console.print_error("No query provided. Use --help for options.")
            return

        piped_data = sys.stdin.read().strip() if not sys.stdin.isatty() else None
        if piped_data:
            with console2.status("[bold green]Processing...[/bold green]"):
                response = handler.ask_t(f"Explain this code like you are a Pro Coder:\n{piped_data}")
            console.print_response(response, markdown=True)

        elif query:
            if shell:
                with console2.status("[bold green]Writing Command...[/bold green]") as status:
                    response = handler.ask_shell_command(f"Provide only the shell command for: {query}")
                try:
                    command = handler.extract_command(response)
                    console.print_response(f"Generated Command: {command}")
                    execute = console.ask_confirmation("Do you want to execute this command? (y/n): ")
                    if execute:
                        status.update(status="Executing command...")
                        ShellExecutor.execute(command)
                except ValueError as e:
                    console.print_error(str(e))

            elif code:
                with console2.status("[bold green]Writing Code...[/bold green]"):
                    response = handler.ask_code(f"Write code for: {query}")
                console.print_code(response)

            elif chat:
                console.print_response("Entering 💬 chat mode! Type 'exit' to leave.", markdown=True)
                response = handler.chat_ask(query)
                console2.print("")
                console.print_response(f"🤖> {response}", markdown=True)
                console2.print(Align("\n--------------------------------", align="center"))
                while True:
                    user_input = console.ask_input("🧑🏻‍💻>")
                    if user_input.strip().lower() == 'exit':
                        console.print_response("✅ Exiting chat mode. Goodbye!", markdown=True)
                        break
                    response = handler.chat_ask(user_input)
                    console2.print("")
                    console.print_response(f"🤖> {response}", markdown=True)
                    console2.print(Align("\n--------------------------------", align="center"))

            elif youtube:
                with console2.status("[bold green]Searching...[/bold green]"):
                    try:
                        search = YoutubeSearch(query, max_results=5)
                        videos = search.to_dict()

                    except Exception as e:
                        console.print_error(f"Error: {e}")

                console.print_response("YouTube Search Results:\n")
                for idx, video in enumerate(videos, start=1):
                    console2.print(f"{idx}. {video['title']}")
                    console2.print(f"   Channel: {video['channel']}")
                    console2.print(f"   Duration: {video['duration']}")
                    console2.print(f"   Views: {video['views']}")
                    console2.print(f"   Published: {video['publish_time']}")
                    console2.print(f"   URL: {video['url']}\n")

                play = console.ask_confirmation("Do you want to play any of these videos? (y/n): ")
                if play:
                    choice = console.ask_input_number(f"Enter the video number to play (1-{len(videos)}): ", 1, len(videos))
                    if 1 <= choice <= len(videos):
                        import webbrowser
                        webbrowser.open(videos[choice - 1]['url'])
                    else:
                        console.log("Invalid choice.")

            elif mail:
                with console2.status("[bold green]Composing Email...[/bold green]"):
                    response = handler.ask_t(f"Compose an Email for: {query}")
                email_data = handler.parse_email_response(query, response)

                try:
                    structured_input = EmailInput(**email_data)
                    email_response = compose_and_send_email(structured_input)
                    console.print_success(email_response)
                except Exception as e:
                    console.print_error(f"Failed to send email: {e}")

            elif gsearch:
                with console2.status("[bold green]Searching from Google...[/bold green]"):
                    try:
                        results = google_search(f"Search {query}")
                    except Exception as e:
                        console.print_error(f"Error: {e}")
                console.print_response("Google Search Done!\n")
                with console2.status("[bold green]Processing query...[/bold green]"):
                    response = handler.ask_t(f"Google Search Result of '{query}' is: \n\n{results} \n\nAnswer the question of '{query}' in a summarize way.")
                console.print_response(response, markdown=True)

            else:
                response = handler.ask(query)
                console.print_response(response, markdown=True)

if __name__ == "__main__":
    cli()
