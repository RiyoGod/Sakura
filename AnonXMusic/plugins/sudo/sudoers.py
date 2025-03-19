from pyrogram import filters
from pyrogram.types import Message

from AnonXMusic import app
from AnonXMusic.misc import SUDOERS, OWNERS
from AnonXMusic.utils.database import add_sudo, remove_sudo, add_owner, remove_owner
from AnonXMusic.utils.decorators.language import language
from AnonXMusic.utils.extraction import extract_user
from config import BANNED_USERS, OWNER_ID


# ⌬ ᴀᴅᴅ sᴜᴅᴏ (ᴏᴡɴᴇʀ & ᴀᴅᴅᴇᴅ ᴏᴡɴᴇʀs ᴄᴀɴ ᴜsᴇ)
@app.on_message(filters.command(["addsudo"]) & filters.user(OWNERS))
@language
async def useradd(client, message: Message, _):
    if not message.reply_to_message and len(message.command) != 2:
        return await message.reply_text("<b>ᴜsᴇ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ ᴄᴏʀʀᴇᴄᴛʟʏ.</b>", parse_mode="html")

    user = await extract_user(message)

    if user.id in SUDOERS:
        return await message.reply_text(f"<b>{user.mention} ɪs ᴀʟʀᴇᴀᴅʏ ᴀ sᴜᴅᴏ ᴜsᴇʀ.</b>", parse_mode="html")

    added = await add_sudo(user.id)
    if added:
        SUDOERS.add(user.id)
        await message.reply_text(f"<b>{user.mention} ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ sᴜᴅᴏ ᴜsᴇʀs.</b>", parse_mode="html")
    else:
        await message.reply_text("<b>ғᴀɪʟᴇᴅ ᴛᴏ ᴀᴅᴅ sᴜᴅᴏ ᴜsᴇʀ.</b>", parse_mode="html")


# ⌬ ʀᴇᴍᴏᴠᴇ sᴜᴅᴏ
@app.on_message(filters.command(["delsudo", "rmsudo"]) & filters.user(OWNERS))
@language
async def userdel(client, message: Message, _):
    if not message.reply_to_message and len(message.command) != 2:
        return await message.reply_text("<b>ᴜsᴇ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ ᴄᴏʀʀᴇᴄᴛʟʏ.</b>", parse_mode="html")

    user = await extract_user(message)

    if user.id not in SUDOERS:
        return await message.reply_text(f"<b>{user.mention} ɪs ɴᴏᴛ ᴀ sᴜᴅᴏ ᴜsᴇʀ.</b>", parse_mode="html")

    removed = await remove_sudo(user.id)
    if removed:
        SUDOERS.remove(user.id)
        await message.reply_text(f"<b>{user.mention} ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ sᴜᴅᴏ ᴜsᴇʀs.</b>", parse_mode="html")
    else:
        await message.reply_text("<b>ғᴀɪʟᴇᴅ ᴛᴏ ʀᴇᴍᴏᴠᴇ sᴜᴅᴏ ᴜsᴇʀ.</b>", parse_mode="html")


# ⌬ ᴀᴅᴅ ᴏᴡɴᴇʀ (ᴏɴʟʏ ᴍᴀɪɴ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ)
@app.on_message(filters.command(["addowner"]) & filters.user(OWNER_ID))
@language
async def owneradd(client, message: Message, _):
    if not message.reply_to_message and len(message.command) != 2:
        return await message.reply_text("<b>ᴜsᴇ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ ᴄᴏʀʀᴇᴄᴛʟʏ.</b>", parse_mode="html")

    user = await extract_user(message)

    if user.id in OWNERS:
        return await message.reply_text(f"<b>{user.mention} ɪs ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴏᴡɴᴇʀ.</b>", parse_mode="html")

    added = await add_owner(user.id)
    if added:
        OWNERS.add(user.id)
        await message.reply_text(f"<b>{user.mention} ʜᴀs ʙᴇᴇɴ ɢʀᴀɴᴛᴇᴅ ᴏᴡɴᴇʀ ᴘʀɪᴠɪʟᴇɢᴇs.</b>", parse_mode="html")
    else:
        await message.reply_text("<b>ғᴀɪʟᴇᴅ ᴛᴏ ᴀᴅᴅ ᴏᴡɴᴇʀ.</b>", parse_mode="html")


# ⌬ ʀᴇᴍᴏᴠᴇ ᴏᴡɴᴇʀ (ᴏɴʟʏ ᴍᴀɪɴ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ)
@app.on_message(filters.command(["delowner"]) & filters.user(OWNER_ID))
@language
async def ownerdel(client, message: Message, _):
    if not message.reply_to_message and len(message.command) != 2:
        return await message.reply_text("<b>ᴜsᴇ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ ᴄᴏʀʀᴇᴄᴛʟʏ.</b>", parse_mode="html")

    user = await extract_user(message)

    if user.id not in OWNERS:
        return await message.reply_text(f"<b>{user.mention} ɪs ɴᴏᴛ ᴀɴ ᴏᴡɴᴇʀ.</b>", parse_mode="html")

    removed = await remove_owner(user.id)
    if removed:
        OWNERS.remove(user.id)
        await message.reply_text(f"<b>{user.mention} ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ᴏᴡɴᴇʀs.</b>", parse_mode="html")
    else:
        await message.reply_text("<b>ғᴀɪʟᴇᴅ ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴏᴡɴᴇʀ.</b>", parse_mode="html")
