import asyncio
import os
from typing import Optional
from dotenv import load_dotenv
from bot.bot import MCPBot
from utils.config_validator import ConfigValidator


def main() -> None:
    """Main entry point for the Discord MCP bot.

    This function loads the environment variables, validates the configuration,
    and starts the bot.
    """
    load_dotenv()

    # Validate configuration before starting
    try:
        ConfigValidator.validate_environment()
    except Exception as e:
        print(f"Configuration error: {e}")
        print("Please fix the configuration and try again.")
        return

    DISCORD_BOT_TOKEN: Optional[str] = os.getenv("DISCORD_BOT_TOKEN")

    # Initialize and start the bot
    bot = MCPBot()
    asyncio.run(bot.start_bot(DISCORD_BOT_TOKEN))


if __name__ == "__main__":
    main()
