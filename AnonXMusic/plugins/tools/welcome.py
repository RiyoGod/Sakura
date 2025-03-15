import random
from pyrogram import Client, filters
from pyrogram.types import Message
from AnonXMusic import app

# 200+ Unique Welcome Messages in Bold Old Font  
WELCOME_MESSAGES = [
    "**ʙᴇ ʀᴇᴀᴅʏ, {mention} ʜᴀs ᴇɴᴛᴇʀᴇᴅ ᴛʜᴇ ʀᴇᴀʟᴍ.**",
    "**ᴛʜᴇ ᴘᴀᴛʜ ᴛᴏ ɢʟᴏʀʏ ʙᴇɢɪɴs ɴᴏᴡ, {mention}.**",
    "**ᴀ ɴᴇᴡ ʙʀᴇᴇᴢᴇ ʙʟᴏᴡs ᴛʜʀᴏᴜɢʜ ᴛʜᴇ ʀᴀɴᴋs. ᴡᴇʟᴄᴏᴍᴇ, {mention}.**",
    "**ᴛʜᴇ ᴏʟᴅ ᴡᴏʀʟᴅ ғᴀᴅᴇs, ᴀ ɴᴇᴡ ᴇʀᴀ ʙᴇɢɪɴs ᴡɪᴛʜ {mention}.**",
    "**ᴛʜᴇ ᴡɪɴᴅ ᴛᴇʟʟs ᴀ ɴᴇᴡ ᴛᴀʟᴇ, {mention} ʜᴀs ᴊᴏɪɴᴇᴅ ᴛʜᴇ ᴊᴏᴜʀɴᴇʏ.**",
    "**ʀɪsᴇ, {mention}. ʏᴏᴜʀ ᴛɪᴍᴇ ʜᴀs ᴄᴏᴍᴇ.**",
    "**ᴛʜᴇ sᴛᴏʀᴍ ɪs ɴᴇᴀʀ, {mention} ʜᴀs ᴀʀʀɪᴠᴇᴅ.**",
    "**ᴛʜᴇ ᴛɪᴍᴇʟɪɴᴇ sʜɪғᴛs, {mention} sᴛᴇᴘs ɪɴ.**",
    "**ʙᴇᴡᴀʀᴇ ᴛʜᴇ ᴄʜᴀɴɢᴇ, {mention} ʜᴀs ᴇɴᴛᴇʀᴇᴅ.**",
    "**ᴛʜᴇ ᴡᴀᴛᴄʜ ʙᴇɢɪɴs ᴀs {mention} ᴀʀʀɪᴠᴇs.**",
    "**ʙᴏʀɴ ᴏғ ᴛʜᴇ sɪʟᴇɴᴄᴇ, {mention} sᴛᴇᴘs ғᴏʀᴡᴀʀᴅ.**",
    "**ᴀ sʜᴀᴅᴏᴡ ʀɪsᴇs, {mention} ʜᴀs ᴊᴏɪɴᴇᴅ ᴜs.**",
    "**ᴛʜᴇ ᴏᴘᴇɴɪɴɢ ᴄʜᴏʀᴅ ʜᴀs ʙᴇᴇɴ sᴛʀᴜᴄᴋ, {mention} ʜᴀs ᴊᴏɪɴᴇᴅ.**",
    "**ʀɪsᴇ ᴡɪᴛʜ ᴜs, {mention}. ᴛʜᴇ ᴊᴏᴜʀɴᴇʏ ʜᴀs ʙᴇɢᴜɴ.**",
    "**ᴛʜᴇ ᴅᴀʀᴋɴᴇss ʙʀᴇᴀᴋs, {mention} ʜᴀs sᴛᴇᴘᴘᴇᴅ ғᴏʀᴡᴀʀᴅ.**",
    "**ʏᴏᴜʀ ᴘʀᴇsᴇɴᴄᴇ ʜᴀs ʙᴇᴇɴ ɴᴏᴛᴇᴅ, {mention}. ʙᴇ ʀᴇᴀᴅʏ.**",
    "**ᴛʜᴇ ᴅᴀᴡɴ ᴏғ ᴀ ɴᴇᴡ ᴇʀᴀ ɪs ʜᴇʀᴇ, {mention}.**",
    "**ᴛʜᴇ ᴄʏᴄʟᴇ ᴄᴏɴᴛɪɴᴜᴇs, {mention} ʜᴀs ᴊᴏɪɴᴇᴅ.**",
    "**ᴀ ᴍʏsᴛᴇʀʏ ᴜɴғᴏʟᴅs, {mention} ʜᴀs ᴀʀʀɪᴠᴇᴅ.**",
    "**ʏᴏᴜʀ ᴊᴏᴜʀɴᴇʏ ʜᴀs ʙᴇɢᴜɴ, {mention}.**",
    "**ʀᴜʟᴇs ᴀʀᴇ ᴍᴀᴅᴇ ᴛᴏ ʙᴇ ʙʀᴏᴋᴇɴ, {mention} ʜᴀs ᴇɴᴛᴇʀᴇᴅ.**",
    "**ᴛʜᴇ ᴏʟᴅ ɪs ɢᴏɴᴇ, {mention} ʙʀɪɴɢs ᴛʜᴇ ɴᴇᴡ.**",
    "**ᴛʜᴇ ʟɪɢʜᴛ ᴀɴᴅ sʜᴀᴅᴏᴡs ᴅᴀɴᴄᴇ, {mention} ʜᴀs ᴊᴏɪɴᴇᴅ.**",
    "**ᴛʜᴇ ᴅᴜsᴛ ʜᴀs ʙᴇᴇɴ sᴛɪʀʀᴇᴅ, {mention} ʜᴀs ᴀʀʀɪᴠᴇᴅ.**",
]

@app.on_message(filters.new_chat_members)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        mention = member.mention
        welcome_text = random.choice(WELCOME_MESSAGES).format(mention=mention)
        await message.reply_text(welcome_text)
