"""Prompt templates for the LLM."""

TOOL_PROMPT = """
You have access to a tool called "send_discord_message".
This tool allows you to send a message to a specific Discord channel.

The tool has the following arguments:
- channel: The channel to send the message to. This can be either:
  - A channel ID (integer like 1418965513580711938)
  - A channel name (string like "general" or "#general")
- message (str): The message to send.

Given the user's request, you must decide whether to use this tool or not.
If you decide to use the tool, you must respond with a JSON object that represents the tool call.
The JSON object must have the following format:
{{
  "tool_name": "send_discord_message",
  "channel": "<channel_name_or_id>",
  "message": "<message>"
}}

Examples:
- For "send hello to #general": {{"tool_name": "send_discord_message", "channel": "general", "message": "hello"}}
- For "post hi in the announcements channel": {{"tool_name": "send_discord_message", "channel": "announcements", "message": "hi"}}
- For "send test to channel 123456": {{"tool_name": "send_discord_message", "channel": "123456", "message": "test"}}

If you decide not to use the tool, you can respond with a natural language message.

User's request: "{user_message}"
"""
