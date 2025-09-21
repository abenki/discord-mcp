"""Utility for resolving channel names to IDs."""
from typing import Optional
from discord.ext import commands
from discord import Guild, TextChannel


class ChannelResolver:
    """Resolves channel names/identifiers to Discord channel IDs."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the ChannelResolver with the bot instance.

        Args:
            bot: The bot instance.
        """
        self.bot: commands.Bot = bot

    async def resolve_channel(self, channel_identifier: str) -> Optional[int]:
        """Resolve a channel name or ID to a channel ID.

        Args:
            channel_identifier: The channel name or ID to resolve.

        Returns:
            int: The resolved channel ID, or None if the channel is not found.
        """
        print(f"Channel identifier: {channel_identifier}")

        # Check if it's already a numeric ID
        try:
            channel_id: int = int(channel_identifier)
            print(f"Using channel ID directly: {channel_id}")
            return channel_id
        except ValueError:
            pass

        # It's a channel name, try to find it
        return await self._find_channel_by_name(channel_identifier)

    async def _find_channel_by_name(self, channel_identifier: str) -> Optional[int]:
        """Find a channel by its name.

        Args:
            channel_identifier: The channel name to find.

        Returns:
            int: The channel ID, or None if the channel is not found.
        """
        channel_name: str = channel_identifier.lstrip('#').lower()
        print(f"Looking for channel named: {channel_name}")

        # Search through all channels the bot can see
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                if channel.name.lower() == channel_name:
                    print(f"Found channel '{
                          channel.name}' with ID: {channel.id}")
                    return channel.id

        print(f"Channel '{channel_identifier}' not found")
        return None
