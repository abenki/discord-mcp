from discord.ext import commands


class MessagingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_discord_message(self, channel_id: int, message: str):
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


async def setup(bot):
    await bot.add_cog(MessagingCog(bot))
