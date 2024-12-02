import os
import re
import uuid
import sqlite3
import platform
from src.ai.agent import agent
from dotenv import load_dotenv
from rich.console import Console
from langchain_ollama import ChatOllama
from src.utils.formatter import RichConsole
from src.utils.youtube import YoutubeSearch
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage
from src.utils.email import EmailInput, compose_and_send_email
from langgraph.graph import MessagesState, StateGraph, START, END

env_path = os.path.join(os.path.expanduser("~"), ".aipat.env")
load_dotenv(env_path)

console = RichConsole()
console2 = Console()

class LLM:        
    def __init__(self):
        """
        Initialize the LLM with database persistence and session management.
        """
        self.conn = sqlite3.connect(os.getenv('DATABASE_PATH', 'memory.db'))
        self.session_id = self._get_or_create_session_id()
        self.llm = ChatOllama(model=os.getenv('DEFAULT_MODEL'))
        self.memory = MemorySaver()
        self.thread_id = str(uuid.uuid4())
        self.config = {"configurable": {"thread_id": self.thread_id}}
        self.workflow = self._build_workflow()
        self._init_db()

    def _init_db(self):
            """Initialize SQLite database for persistent memory."""
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversation_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    user_message TEXT NOT NULL,
                    ai_response TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()

    def _get_or_create_session_id(self) -> str:
        """
        Retrieve the last session ID from the database or create a new one.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT session_id FROM conversation_memory ORDER BY timestamp DESC LIMIT 1")
        last_session = cursor.fetchone()
        return last_session[0] if last_session else str(uuid.uuid4())

    def _build_workflow(self):
        """
        Build the workflow graph for handling AI interactions with memory.
        """
        workflow = StateGraph(MessagesState)

        def call_model(state: MessagesState):
            """
            Define the function to call the LLM model.
            """
            response = self.llm.invoke(state["messages"])
            return {"messages": response}

        def should_continue(state: MessagesState):
            """
            Determine whether to continue the workflow or end it.
            """
            return END

        workflow.add_node("agent", call_model)
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges(
            "agent", should_continue, [END]
        )

        return workflow.compile(checkpointer=self.memory)

    def save_to_memory(self, user_message: str, ai_response: str):
        """Persist conversation data into the SQLite database."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO conversation_memory (session_id, user_message, ai_response)
            VALUES (?, ?, ?)
        """, (self.session_id, user_message, ai_response))
        self.conn.commit()

    def get_memory(self) -> list:
        """Retrieve conversation history for the current session."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT user_message, ai_response FROM conversation_memory
            WHERE session_id = ?
            ORDER BY timestamp
        """, (self.session_id,))
        results = cursor.fetchall()
        return results

    def clear_memory(self):
        """Clear conversation history for the current session."""
        cursor = self.conn.cursor()
        cursor.execute("""
            DELETE FROM conversation_memory WHERE session_id = ?
        """, (self.session_id,))
        self.conn.commit()

    def get_system_info(self) -> dict:
        """
        Get system information such as OS, version, and current working directory.
        """
        return {
            "os_name": platform.system(),
            "os_version": platform.release(),
            "cwd": os.getcwd(),
        }

    def extract_command(self, response_text):
        """
        Extracts a valid shell command from the AI's response.
        """
        match = re.search(r"`([^`]+)`|^\s*([^\n]+)", response_text, re.MULTILINE)

        if match:
            command = match.group(1) or match.group(2)
            print(f"Extracted Command: {command}")
            return command.strip()

        print("Debugging AI Response:", response_text)
        raise ValueError("No valid command found in AI response.")

    def parse_email_response(self, prompt: str, email_content: str) -> dict:
        """
        Parses the AI-generated email response into a structured dictionary.
        Extracts recipient, subject, and body details.
        
        :param prompt: The original user query or input.
        :param email_content: The email content generated by the AI.
        :return: A dictionary with keys: 'recipient', 'subject', 'body'.
        """
        recipient = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", prompt)
        recipient = recipient.group(0) if recipient else None

        subject_line = next((line for line in email_content.split("\n") if line.startswith("Subject:")), None)
        subject = subject_line.replace("Subject: ", "").strip() if subject_line else "No Subject Provided"

        body_start = email_content.find("\n") + 1
        body = email_content[body_start:].strip() if body_start > 0 else "No Body Content Provided"

        return {
            "recipient": recipient,
            "subject": subject,
            "body": body,
        }

    def ask(self, prompt: str) -> str:
        """
        Process a user query, maintain conversation history,
        save conversation to memory, and return the AI response.
        """
        try:
            if "youtube" in prompt.lower():
                query = prompt.replace("Search youtube for", "").strip()

                with console2.status("[bold green]Searching YouTube...[/bold green]"):
                    try:
                        search = YoutubeSearch(query, max_results=5)
                        videos = search.to_dict()
                    except Exception as e:
                        return f"Error during YouTube search: {e}"

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
                        return f"Playing video: {videos[choice - 1]['title']}"
                    else:
                        return "Invalid video choice."
                return "No video selected."

            elif "mail to" in prompt.lower() or "email" in prompt.lower():
                with console2.status("[bold green]Composing Email...[/bold green]"):
                    response = self.llm.invoke([HumanMessage(content=f"Compose an Email for: {prompt}")])
                try:
                    email_content = response.content
                except AttributeError:
                    return "Failed to compose email: Response object does not have 'content' attribute."

                email_data = self.parse_email_response(prompt, email_content)

                try:
                    structured_input = EmailInput(**email_data)
                    email_response = compose_and_send_email(structured_input)
                    return email_response
                except Exception as e:
                    return f"Failed to send email: {e}"

            with console2.status("[bold green]Processing query...[/bold green]"):
                messages = agent.invoke({"messages": [("user", prompt)]})
            response_content = messages["messages"][-1].content

            return response_content

        except Exception as e:
            return f"An error occurred while using the agent: {e}"


    def chat_ask(self, prompt: str) -> str:
        """
        Process a user query, maintain conversation history,
        save conversation to memory, and return the AI response.
        """
        try:
            if "youtube" in prompt.lower():
                query = prompt.replace("Search youtube for", "").strip()

                with console2.status("[bold green]Searching YouTube...[/bold green]"):
                    try:
                        search = YoutubeSearch(query, max_results=5)
                        videos = search.to_dict()
                    except Exception as e:
                        return f"Error during YouTube search: {e}"

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
                        return f"Playing video: {videos[choice - 1]['title']}"
                    else:
                        return "Invalid video choice."
                return "No video selected."

            elif "mail to" in prompt.lower() or "email" in prompt.lower():
                with console2.status("[bold green]Composing Email...[/bold green]"):
                    response = self.llm.invoke([HumanMessage(content=f"Compose an Email for: {prompt}")])
                try:
                    email_content = response.content
                except AttributeError:
                    return "Failed to compose email: Response object does not have 'content' attribute."

                email_data = self.parse_email_response(prompt, email_content)

                try:
                    structured_input = EmailInput(**email_data)
                    email_response = compose_and_send_email(structured_input)
                    return email_response
                except Exception as e:
                    return f"Failed to send email: {e}"

            chat_history = self.get_memory()
            message_history = [
                ("human", user) if i % 2 == 0 else ("ai", ai)
                for i, (user, ai) in enumerate(chat_history)
            ]

            message_history.append(
                ("system", "You are an AI assistant named AIPAT: AI Powered Assistance Tool for Terminal.")
            )

            message_history.append(("human", prompt))

            with console2.status("[bold green]Processing query...[/bold green]"):
                messages = agent.invoke({"messages": message_history})
            response_content = messages["messages"][-1].content

            self.save_to_memory(prompt, response_content)
            return response_content

        except Exception as e:
            return f"An error occurred while using the agent: {e}"

    def ask_shell_command(self, query: str) -> str:
        """
        Ask the AI to generate a shell command suitable for the user's OS.
        """
        system_info = self.get_system_info()
        user_message = HumanMessage(content=
                                    f"You are an AI assistant named AIPAT, running on the following system:\n"
                                    f"OS: {system_info['os_name']} {system_info['os_version']}\n"
                                    f"Current Working Directory: {system_info['cwd']}\n\n"
                                    f"Provide only the shell command for: {query}\n"
                                    f"Response format: `<command>`")
        response = None
        for event in self.workflow.stream(
            {"messages": [user_message]}, self.config, stream_mode="values"
        ):
            response = event["messages"][-1]

        self.save_to_memory(query, response.content)
        return response.content

    def ask_code(self, query: str) -> str:
        """
        Ask the AI to generate code based on the user's request.
        """
        user_message = HumanMessage(content=
                                    f"You are a coding assistant named AIPAT. Write code for the following request:\n"
                                    f"{query}\n\n"
                                    f"Response format: Plain code with no explanation. And write only the code.")
        response = None
        for event in self.workflow.stream(
            {"messages": [user_message]}, self.config, stream_mode="values"
        ):
            response = event["messages"][-1]

        self.save_to_memory(query, response.content)
        return response.content
