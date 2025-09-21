import traceback
from typing import Optional, Dict, Any
from discord.ext import commands
from discord import Message
from llm.client import LLMClient
from llm.prompts import TOOL_PROMPT
from utils.channel_resolver import ChannelResolver


class MessageHandler:
    """Handles processing of Discord messages."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the MessageHandler with the bot instance.

        Args:
            bot: The bot instance.
        """
        self.bot: commands.Bot = bot
        self.llm_client: LLMClient = LLMClient()
        self.channel_resolver: ChannelResolver = ChannelResolver(bot)

    async def handle_message(self, message: Message) -> None:
        """Main message handling entry point.

        Args:
            message: The Discord message to handle.
        """
        # Check if we should process this message
        if not await self._should_process_message(message):
            return

        # Process the message
        await self._process_user_message(message)

    async def _should_process_message(self, message: Message) -> bool:
        """Check if the bot should process this message.

        Args:
            message: The Discord message to check.

        Returns:
            bool: True if the message should be processed, False otherwise.
        """
        if message.author == self.bot.user:
            print("Ignoring message from bot")
            return False

        if not self.bot.user.mentioned_in(message):
            print("Bot not mentioned, ignoring")
            return False

        print("Bot user was mentioned!")
        return True

    async def _process_user_message(self, message: Message) -> None:
        """Process a message that mentions the bot.

        Args:
            message: The Discord message to process.
        """
        print(f"Bot mentioned! Processing message: {message.content}")
        print(f"Clean content: {message.clean_content}")

        try:
            # Create prompt and get LLM response
            user_message: str = message.clean_content
            print(f"User message extracted: '{user_message}'")

            prompt: str = TOOL_PROMPT.format(user_message=user_message)
            print("Prompt created successfully")

            print("About to call LLM...")
            llm_response: Optional[Dict[str, Any]] = await self.llm_client.get_response(prompt)
            print("LLM call completed")

            # Process the response
            await self._process_llm_response(message, llm_response)

        except Exception as e:
            print(f"Exception occurred in message processing: {e}")
            traceback.print_exc()
            await message.channel.send(f"Sorry, I encountered an error: {str(e)}")

    async def _process_llm_response(self, message: Message, llm_response: Optional[Dict[str, Any]]) -> None:
        """Process the response from the LLM.

        Args:
            message: The original Discord message.
            llm_response: The response from the LLM.
        """
        print(f"LLM Response type: {type(llm_response)}")
        print(f"LLM Response: {llm_response}")

        if not llm_response:
            print("LLM response was None or empty")
            await message.channel.send("Sorry, I had a problem thinking about that.")
            return

        # Check if it's a tool call
        if isinstance(llm_response, dict) and llm_response.get("tool_name") == "send_discord_message":
            await self._handle_tool_call(message, llm_response)
        elif isinstance(llm_response, str):
            print("LLM returned a string response")
            await message.channel.send(llm_response)
        else:
            print(f"Unexpected response type from LLM: {type(llm_response)}")
            print(f"Response content: {llm_response}")
            await message.channel.send("I got a response I don't understand from the model.")

    async def _handle_tool_call(self, message: Message, llm_response: Dict[str, Any]) -> None:
        """Handle a tool call from the LLM.

        Args:
            message: The original Discord message.
            llm_response: The response from the LLM.
        """
        print("LLM returned a tool call!")
        messaging_cog = self.bot.get_cog("MessagingCog")
        print(f"MessagingCog found: {messaging_cog is not None}")

        if not messaging_cog:
            print("MessagingCog not found!")
            await message.channel.send("Messaging functionality is not available.")
            return

        try:
            channel_identifier: str = llm_response["channel"]
            message_text: str = llm_response["message"]
            print(f"Message: {message_text}")

            # Resolve channel
            channel_id: Optional[int] = await self.channel_resolver.resolve_channel(channel_identifier)

            if channel_id is None:
                await message.channel.send(f"Sorry, I couldn't find a channel named '{channel_identifier}'")
                return

            print(f"Attempting to send message '{message_text}' to channel {channel_id}")
            await messaging_cog.send_discord_message(channel_id, message_text)
            await message.add_reaction("✅")
            print("Message sent successfully!")

        except (KeyError, TypeError, ValueError) as e:
            print(f"Error executing tool call: {e}")
            await message.channel.send("Sorry, I couldn't understand the tool call from the model.")
