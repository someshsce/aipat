<!-- PROJECT LOGO -->
![AIPATT](https://img.shields.io/badge/AIPATT-Tool-blue) ![PyPI](https://img.shields.io/pypi/v/aipatt)
<div align=center>

### AIPATT

A versatile terminal-based AI Powered Assistant Tool.

[View Demo](https://github.com/someshsce/aipatt) · [Report Bug](https://github.com/someshsce/aipatt/issues/new?labels=bug&template=bug-report---.md) · [Request Feature](https://github.com/someshsce/aipatt/issues/new?labels=enhancement&template=feature-request---.md)

</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>

1. [About The Project](#about-the-project)
   - [Built With](#built-with)
2. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Configuration](#configuration)
3. [Usage](#usage)
4. [Contributing](#contributing)
5. [License](#license)
6. [Contact](#contact)

</details>

<!-- ABOUT THE PROJECT -->
## About The Project

<div align=center>
  
</div>
<br />

AIPATT is an AI-powered Assistance Tool for Terminals designed to streamline your workflow by providing tools to generate code, execute shell commands, retrieve and summarize information from Google, and engage in interactive chats.

Here's why:

- **Boost productivity**: AIPATT helps automate repetitive tasks like coding, information retrieval, and system commands right from the terminal.
- **Easy integration**: Integrates seamlessly with your command-line environment, making it a powerful addition to your development toolkit.
- **Versatile**: Whether you're coding, querying data, or managing system tasks, AIPATT adapts to your needs.

AIPATT is built with an emphasis on simplicity, power, and flexibility, enabling developers and power users to get things done faster and smarter.

### Built With

These are the major frameworks and libraries used to build AIPATT:

- [![Python](https://img.shields.io/badge/Python-3.11.10-snake)](https://www.python.org)
- [![Ollama](https://img.shields.io/badge/Ollama-v0.4.7-green)](https://ollama.com)
- [![LLaMa3](https://img.shields.io/badge/LLaMa-3.2-blue)](https://example.com)
- [![Langchain](https://img.shields.io/badge/Langchain-0.3.9-blue)](https://langchain.com)
- [![Langgraph](https://img.shields.io/badge/Langgraph-0.2.53-red)](https://example.com)

<!-- GETTING STARTED -->
## Getting Started

To get a local copy of **AIPATT** up and running, follow these steps.

### Prerequisites

Before installing and using **AIPATT**, ensure you have the following installed:

- **Python 3.10+** - Ensure Python is installed on your system. You can download it from [here](https://www.python.org/downloads/).
- **Ollama** - To run the language models, you need to install Ollama. You can get Ollama from their [official site](https://ollama.com).
  - Once installed, you can run a model like `llama3.2` using:

    ```sh
    ollama run llama3.2
    ```

  - You can explore other models available on [Ollama's model library](https://ollama.com/search) that supports tools calling.

### Installation

Once the prerequisites are installed, follow these steps to install **AIPATT**:

1. Install **AIPATT** via **pip**:

   ```sh
   pip install aipatt
   ```

2. After the installation, you can start using AIPATT directly in your terminal by running:

   ```sh
   aipatt
   ```

### Configuration

The first time you run **AIPATT**, you will need to configure a few settings. You can either use the default settings or customize them as per your needs. Below are the configuration options you'll need to provide:

1. `DATABASE_PATH`: Default value is available, but you can specify your own database path.
2. `DEFAULT_MODEL`: Default model is set, but you can change it to any available model in Ollama.
3. `OPENWEATHERMAP_API_KEY`: You need to get your API key from OpenWeatherMap.
4. `GOOGLE_SEARCH_URL`: The default Google search URL is set, but you can override it.
5. `GOOGLE_CSE_ID`: Get your Custom Search Engine ID from Google CSE.
6. `GOOGLE_API_KEY`: Get your Google API Key from Google Cloud Console.
7. `SMTP_SERVER`: Default is set for Gmail, but you can configure your own SMTP server.
8. `PORT`: Default is set for Gmail. If using a different SMTP server, you need to provide the correct port.
9. `USERNAME`: Your email address or username for the SMTP server.
10. `PASSWORD`: Your email password or an app-specific password if using Gmail.

**`Note`**: When you first run AIPATT, it will ask you to enter these configuration values. You can also manually edit the `.aipatt.env` file that is created in the home directory to modify these settings.

<!-- USAGE EXAMPLES -->
## Usage

Here are some useful examples of how you can use **AIPATT** to perform different tasks. Each command can be run directly in your terminal. For more details on the available commands, use the `-h` or `--help` option.

To see all available options, use:

  ```sh
  aipatt -h
  ```

### `Available Commands`

`Generate Code`: Use this to generate code based on your input query.

  ```sh
  aipatt -c "Write a Python script for Fibonacci series"
  ```

`Chat`: Engage in a continuous conversation with the AI.

  ```sh
  aipatt -ch
  ```

`YouTube Search`: Search and play YouTube videos directly from the terminal.

  ```sh
  aipatt -y "Top Python tutorials"
  ```

`Shell Command Generation`: Generate and execute shell commands based on a query.

  ```sh
  aipatt -s "How to update my system?"
  ```

`Mail Composer`: Compose and send an email using AI.

  ```sh
  aipatt -m "Send email to example@gmail.com, Meeting at 10 AM"
  ```

`Google Search and Summarize`: Search on Google and get a summarized answer.

  ```sh
  aipatt -gs "What is the capital of France?"
  ```

`Update Configuration`: Use this command to update your configuration settings.

  ```sh
  aipatt -u
  ```

`Clear Memory`: Clear the entire chat memory.

  ```sh
  aipatt -cm
  ```

`Version Info`: Get the version of AIPATT installed.

  ```sh
  aipatt -v
  ```

`Help`: Display the help message with all available options.

  ```sh
  aipatt -h
  ```

### `Example Commands`

`Ask a Question`: Query the AI to answer questions directly:

  ```sh
  aipatt "What is internet?"
  ```

`Search Latest News About AI`: Use AIPATT to stay updated with the latest AI news:

  ```sh
  aipatt "Latest news about AI"
  ```

`Search and Play YouTube Videos`: Search for specific videos on YouTube and play them:

  ```sh
  aipatt -y "Top Python tutorials"
  ```

`Generate Shell Command`: Run a query and generate a shell command, or execute a script:

  ```sh
  aipatt -s "How to update my system?"
  ```

`Summarize Google Search Results`: Use AIPATT to search Google and get a summary of the results:

  ```sh
  aipatt -gs "What is the capital of France?"
  ```

`Current Weather Conditions`: Get the weather report of a city:

  ```sh
  aipatt "Current Weather Condition of New York"
  ```

`Generate Code`: Generate code for a common task like a Fibonacci series:

  ```sh
  aipatt -c "Write a Python script for Fibonacci series"
  ```

`Send an Email`: Compose and send an email using AI:

  ```sh
  aipatt -m "Send email to example@gmail.com, Meeting at 10 AM"
  ```

`Explain Shell Script`: You can even pipe a shell script into AIPATT and get an explanation of the code:

  ```sh
  cat install.sh | aipatt "Explain the code"
  ```

<!-- Contributing -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

Don't forget to give the project a star! Thanks again!

### Steps to Contribute

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

[See](CONTRIBUTING.md) `CONTRIBUTING.md` for more information.

<!-- LICENSE -->
## License

Distributed under the [GNU AGPLv3 License](LICENSE). See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

**Author**: `Somesh Sharma`

<table border="0">
  <tr>
    <td><strong>AIPATT</strong></td>
    <td><a href="https://pypi.org/project/aipatt/">PyPI Link</a></td>
  </tr>
  <tr>
    <td><strong>LinkedIn</strong></td>
    <td><a href="https://www.linkedin.com/in/somesh9">Somesh Sharma</a></td>
  </tr>
  <tr>
    <td><strong>Instagram</strong></td>
    <td><a href="https://www.instagram.com/somesh_el">Somesh Sharma</a></td>
  </tr>
  <tr>
    <td><strong>Email</strong></td>
    <td><a href="mailto:someshs.ce@gmail.com">someshs.ce@gmail.com</a></td>
  </tr>
</table>
