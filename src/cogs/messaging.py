from discord.ext import commands
from discord import ChannelType
from typing import Optional


class MessagingCog(commands.Cog):
    """A cog for handling messaging operations in Discord."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the MessagingCog with the bot instance.

        Args:
            bot: The bot instance.
        """
        self.bot = bot

    async def send_discord_message(self, channel_id: int, message: str) -> None:
        """Sends a message to a Discord channel.

        Args:
            channel_id: The ID of the channel to send the message to.
            message: The message to send.
        """
        channel = self.bot.get_channel(channel_id)
        if channel:
            await channel.send(message)
            print(f"Message sent to channel {channel_id}")
        else:
            print(f"Could not find channel with ID {channel_id}")


async def setup(bot: commands.Bot) -> None:
    """Add the MessagingCog to the bot.

    Args:
        bot: The bot instance.
    """
    await bot.add_cog(MessagingCog(bot))
