import random
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from config import LOGGER_ID as LOG_GROUP_ID
from AnonXMusic import app 
from pyrogram.errors import RPCError

# Photo for logs
LOG_PHOTO = "https://files.catbox.moe/ro0pv8.jpg"

@app.on_message(filters.new_chat_members, group=2)
async def join_watcher(_, message):    
    chat = message.chat
    link = await app.export_chat_invite_link(chat.id)
    
    for member in message.new_chat_members:
        if member.id == app.id:
            count = await app.get_chat_members_count(chat.id)
            msg = (
                "◆━━━━━━━━━━━━━◆\n\n"
                "<b>#ᴀᴅᴅᴇᴅ_ɪɴ_ɢʀᴏᴜᴘ</b>\n\n"
                f"❖ ᴄʜᴀᴛ ɴᴀᴍᴇ : <code>{chat.title}</code>\n"
                f"❖ ᴄʜᴀᴛ ɪᴅ : <code>{chat.id}</code>\n"
                f"❖ ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ : @{chat.username}\n"
                f"❖ ᴄʜᴀᴛ ʟɪɴᴋ : {link}\n"
                f"❖ ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs : <code>{count}</code>\n"
                f"❖ ᴀᴅᴅᴇᴅ ʙʏ : {message.from_user.mention}\n\n"
                "◆━━━━━━━━━━━━━◆"
            )
            await app.send_photo(
                LOG_GROUP_ID, 
                photo=LOG_PHOTO,
                caption=msg,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("➤ sᴇᴇ ɢʀᴏᴜᴘ", url=f"{link}")]
                ])
            )

@app.on_message(filters.left_chat_member)
async def on_left_chat_member(_, message: Message):
    if (await app.get_me()).id == message.left_chat_member.id:
        remove_by = message.from_user.mention if message.from_user else "ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ"
        title = message.chat.title
        username = f"@{message.chat.username}" if message.chat.username else "ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ"
        chat_id = message.chat.id

        left = (
            "◆━━━━━━━━━━━━━◆\n\n"
            "<b># ʟᴇғᴛ_ɢʀᴏᴜᴘ</b>\n\n"
            f"❖ ᴄʜᴀᴛ ɴᴀᴍᴇ : <code>{title}</code>\n"
            f"❖ ᴄʜᴀᴛ ɪᴅ : <code>{chat_id}</code>\n"
            f"❖ ʀᴇᴍᴏᴠᴇᴅ ʙʏ : <code>{remove_by}</code>\n"
            f"❖ ʙᴏᴛ : @{app.username}\n\n"
            "◆━━━━━━━━━━━━━◆"
        )
        await app.send_photo(
            LOG_GROUP_ID, 
            photo=LOG_PHOTO,
            caption=left
        )
