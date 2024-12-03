import os
from dotenv import load_dotenv

def setup_config(env_path):
    """Prompt user for configuration details and save to the .aipatt.env file."""
    print("Configuration file not found. Let's set it up.")

    home_dir = os.path.expanduser("~")
    db_path = os.path.join(home_dir, ".aipatt_memory.db")

    try:
        DATABASE_PATH = input("Enter path for the database file (default: {db_path}): ")
        if not DATABASE_PATH:
            DATABASE_PATH = db_path

        DEFAULT_MODEL = input("Enter the default model (default: llama3.2): ")
        if not DEFAULT_MODEL:
            DEFAULT_MODEL = "llama3.2"

        OPENWEATHERMAP_API_KEY = input("Enter your OpenWeatherMap API Key: ")

        GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

        GOOGLE_CSE_ID = input("Enter your Google Custom Search Engine ID: ")
        GOOGLE_API_KEY = input("Enter your Google API Key: ")

        SMTP_SERVER = input("Enter your SMTP Server (default: smtp.gmail.com): ")
        if not SMTP_SERVER:
            SMTP_SERVER = "smtp.gmail.com"

        PORT = input("Enter your SMTP Port (default: 465): ")
        if not PORT:
            PORT = "465"

        USERNAME = input("Enter your SMTP username (email): ")
        PASSWORD = input("Enter your SMTP password: ")
    except KeyboardInterrupt:
        print("\nConfiguration setup cancelled.\nBut you need to set up the configuration to use the AI assistant.")
        return

    with open(env_path, "w") as f:
        f.write(f"DATABASE_PATH={DATABASE_PATH}\n")
        f.write(f"DEFAULT_MODEL={DEFAULT_MODEL}\n")
        f.write(f"OPENWEATHERMAP_API_KEY={OPENWEATHERMAP_API_KEY}\n")
        f.write(f"GOOGLE_SEARCH_URL={GOOGLE_SEARCH_URL}\n")
        f.write(f"GOOGLE_CSE_ID={GOOGLE_CSE_ID}\n")
        f.write(f"GOOGLE_API_KEY={GOOGLE_API_KEY}\n")
        f.write(f"SMTP_SERVER={SMTP_SERVER}\n")
        f.write(f"PORT={PORT}\n")
        f.write(f"USERNAME={USERNAME}\n")
        f.write(f"PASSWORD={PASSWORD}\n")

    print("Configuration saved successfully!")

def update_config(env_path):
    """Prompt user to update the configuration file."""
    load_dotenv(env_path)

    home_dir = os.path.expanduser("~")
    db_path = os.path.join(home_dir, ".aipatt_memory.db")

    print("Configuration file found. You can update the following settings:")

    try:
        DATABASE_PATH = input(f"Enter path for the database file (current: {os.getenv('DATABASE_PATH', '.aipatt_memory.db')}): ")
        if not DATABASE_PATH:
            DATABASE_PATH = db_path

        DEFAULT_MODEL = input(f"Enter the default model (current: {os.getenv('DEFAULT_MODEL', 'llama3.2')}): ")
        if not DEFAULT_MODEL:
            DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama3.2")

        OPENWEATHERMAP_API_KEY = input(f"Enter your OpenWeatherMap API Key (current: {os.getenv('OPENWEATHERMAP_API_KEY')}): ")

        GOOGLE_SEARCH_URL = input(f"Enter the Google Search URL (current: {os.getenv('GOOGLE_SEARCH_URL', 'https://www.googleapis.com/customsearch/v1')}): ")
        if not GOOGLE_SEARCH_URL:
            GOOGLE_SEARCH_URL = os.getenv("GOOGLE_SEARCH_URL", "https://www.googleapis.com/customsearch/v1")

        GOOGLE_CSE_ID = input(f"Enter your Google Custom Search Engine ID (current: {os.getenv('GOOGLE_CSE_ID')}): ")
        GOOGLE_API_KEY = input(f"Enter your Google API Key (current: {os.getenv('GOOGLE_API_KEY')}): ")

        SMTP_SERVER = input(f"Enter your SMTP Server (current: {os.getenv('SMTP_SERVER', 'smtp.gmail.com')}): ")
        if not SMTP_SERVER:
            SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")

        PORT = input(f"Enter your SMTP Port (current: {os.getenv('PORT', '465')}): ")
        if not PORT:
            PORT = os.getenv("PORT", "465")

        USERNAME = input(f"Enter your SMTP username (current: {os.getenv('USERNAME')}): ")
        PASSWORD = input(f"Enter your SMTP password (current: {os.getenv('PASSWORD')}): ")

    except KeyboardInterrupt:
        print("\nConfiguration update cancelled.")
        return

    with open(env_path, "w") as f:
        f.write(f"DATABASE_PATH={DATABASE_PATH}\n")
        f.write(f"DEFAULT_MODEL={DEFAULT_MODEL}\n")
        f.write(f"OPENWEATHERMAP_API_KEY={OPENWEATHERMAP_API_KEY}\n")
        f.write(f"GOOGLE_SEARCH_URL={GOOGLE_SEARCH_URL}\n")
        f.write(f"GOOGLE_CSE_ID={GOOGLE_CSE_ID}\n")
        f.write(f"GOOGLE_API_KEY={GOOGLE_API_KEY}\n")
        f.write(f"SMTP_SERVER={SMTP_SERVER}\n")
        f.write(f"PORT={PORT}\n")
        f.write(f"USERNAME={USERNAME}\n")
        f.write(f"PASSWORD={PASSWORD}\n")

    print("Configuration updated successfully!")
