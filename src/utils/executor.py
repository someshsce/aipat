import subprocess
from src.utils.formatter import RichConsole

console = RichConsole()

class ShellExecutor:
    @staticmethod
    def execute(command):
        try:
            console.log(f"Executing command: {command}")
            result = subprocess.run(command, shell=True, text=True, capture_output=True)
            if result.returncode == 0:
                console.print_success(result.stdout)
            else:
                console.print_error(result.stderr)
        except Exception as e:
            console.print_error(f"Failed to execute command: {e}")
