import asyncio
import os
from dotenv import load_dotenv
from bot.bot import MCPBot
from utils.config_validator import ConfigValidator


async def main():
    """Main entry point for the Discord MCP bot."""
    load_dotenv()

    # Validate configuration before starting
    try:
        ConfigValidator.validate_environment()
    except Exception as e:
        print(f"Configuration error: {e}")
        print("Please fix the configuration and try again.")
        return

    DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

    # Initialize and start the bot
    bot = MCPBot()
    await bot.start_bot(DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
