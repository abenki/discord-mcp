import discord
from discord.ext import commands
from bot.message_handler import MessageHandler


class MCPBot:
    """Main bot class that handles Discord bot setup and events."""

    def __init__(self):
        """Initialize the bot with required intents and settings."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True

        self.bot = commands.Bot(command_prefix="!", intents=intents)
        self.message_handler = MessageHandler(self.bot)

        # Set up event handlers
        self._setup_events()

    def _setup_events(self):
        """Set up bot event handlers."""

        @self.bot.event
        async def on_ready():
            print(f"We have logged in as {self.bot.user}")
            print(f"Bot ID: {self.bot.user.id}")
            print(f"To mention this bot, use: <@{self.bot.user.id}>")

        @self.bot.event
        async def on_message(message):
            print(f"Message received from {message.author}: {message.content}")
            await self.message_handler.handle_message(message)

    async def _load_cogs(self):
        """Load all bot cogs."""
        try:
            await self.bot.load_extension("cogs.messaging")
            print("MessagingCog loaded successfully")
        except Exception as e:
            print(f"Error loading MessagingCog: {e}")

    async def start_bot(self, token: str):
        """Start the bot with the given token."""
        await self._load_cogs()
        await self.bot.start(token)
