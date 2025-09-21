# Discord MCP Bot

A Discord bot that integrates with the Ollama API to provide intelligent responses and messaging capabilities.


## Features

- **LLM Integration**: Uses the Ollama API for natural language processing
- **Channel Management**: Resolves and interacts with Discord channels
- **Message Handling**: Processes and responds to user messages
- **Configuration Validation**: Ensures proper setup before running

## Installation

### Prerequisites

- Python 3.8 or higher
- uv
- Ollama installed and running

### Steps

1. Clone the repository:

```bash
git clone git@github.com:abenki/discord-mcp.git
```

2. Install the required dependencies:

```bash
uv sync
```

3. Set up the environment variables:

Create a `.env` file in the root directory with the following variables (see `.env.example` for reference):

```env
DISCORD_BOT_TOKEN=your_discord_bot_token
OLLAMA_API_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=qwen2.5:14b
```

For more details regarding how to get the Discord Bot Token, check [this tutorial](https://www.writebots.com/discord-bot-token/#:~:text=A%20Discord%20Bot%20Token%20is,Discord%20Bot%20Token%20with%20anyone).

4. Invite the bot to your Discord server


## Usage

### Starting the Ollama service:

```bash
ollama serve
```

### Running the Bot

To start the bot, run:

```bash
uv run src/main.py
```

### Interacting with the Bot
1. Mention the bot in a channel with your message
2. The bot will process your message and respond accordingly

### Example Commands

- `@BotName send hello to #general`: Sends "hello" to the general channel
- `@BotName post announcement in the announcements channel`: Posts a message in the announcements channel

## Configuration

The bot can be configured using environment variables in the `.env` file:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| DISCORD_BOT_TOKEN | Your Discord bot token | None |
| OLLAMA_API_URL | URL for the Ollama API | http://localhost:11434/api/generate |
| OLLAMA_MODEL | Model to use for LLM responses | qwen2.5:14b |

To change the configuration, modify the values in the `.env` file and restart the bot.
