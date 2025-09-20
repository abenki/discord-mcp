"""Utility for resolving channel names to IDs."""


class ChannelResolver:
    """Resolves channel names/identifiers to Discord channel IDs."""

    def __init__(self, bot):
        self.bot = bot

    async def resolve_channel(self, channel_identifier):
        """Resolve a channel name or ID to a channel ID."""
        print(f"Channel identifier: {channel_identifier}")

        # Check if it's already a numeric ID
        try:
            channel_id = int(channel_identifier)
            print(f"Using channel ID directly: {channel_id}")
            return channel_id
        except ValueError:
            pass

        # It's a channel name, try to find it
        return await self._find_channel_by_name(channel_identifier)

    async def _find_channel_by_name(self, channel_identifier):
        """Find a channel by its name."""
        channel_name = channel_identifier.lstrip('#').lower()
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
