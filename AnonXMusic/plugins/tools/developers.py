from AnonXMusic import app  # Importing the bot instance from AnonXMusic
from pyrogram import filters

# Public channel username
SOURCE_CHAT_USERNAME = "RsOwners"  # No @ symbol, just the username
MESSAGE_ID = 3  # Message ID of the post to forward

@app.on_message(filters.command("dev"))
async def forward_dev_message(client, message):
    try:
        await client.forward_messages(
            chat_id=message.chat.id,  # Forward to the chat where the command was used
            from_chat_id=SOURCE_CHAT_USERNAME,
            message_ids=MESSAGE_ID
        )
    except Exception as e:
        await message.reply_text(f"Error: {e}")  # Send error message if something goes wrong
