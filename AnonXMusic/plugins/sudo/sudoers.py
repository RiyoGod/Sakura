from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from AnonXMusic import app
from AnonXMusic.misc import SUDOERS
from AnonXMusic.utils.database import add_sudo, remove_sudo
from AnonXMusic.utils.decorators.language import language
from AnonXMusic.utils.extraction import extract_user
from config import BANNED_USERS, OWNER_ID


# ⌬ ᴀᴅᴅ sᴜᴅᴏ
@app.on_message(filters.command(["addsudo"]) & filters.user(OWNER_ID))
@language
async def useradd(client, message: Message, _):
    if not message.reply_to_message and len(message.command) != 2:
        return await message.reply_text("ᴘʟᴇᴀsᴇ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴏʀʀᴇᴄᴛʟʏ.")

    user = await extract_user(message)
    
    if user.id in SUDOERS:
        return await message.reply_text(f"{user.mention} ɪs ᴀʟʀᴇᴀᴅʏ ᴀ sᴜᴅᴏ ᴜsᴇʀ.")

    added = await add_sudo(user.id)
    if added:
        SUDOERS.add(user.id)
        await message.reply_text(f"{user.mention} ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ sᴜᴅᴏ ᴜsᴇʀs.")
    else:
        await message.reply_text("ғᴀɪʟᴇᴅ ᴛᴏ ᴀᴅᴅ sᴜᴅᴏ ᴜsᴇʀ.")


# ⌬ ʀᴇᴍᴏᴠᴇ sᴜᴅᴏ
@app.on_message(filters.command(["delsudo", "rmsudo"]) & filters.user(OWNER_ID))
@language
async def userdel(client, message: Message, _):
    if not message.reply_to_message and len(message.command) != 2:
        return await message.reply_text("ᴘʟᴇᴀsᴇ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴏʀʀᴇᴄᴛʟʏ.")

    user = await extract_user(message)
    
    if user.id not in SUDOERS:
        return await message.reply_text(f"{user.mention} ɪs ɴᴏᴛ ᴀ sᴜᴅᴏ ᴜsᴇʀ.")

    removed = await remove_sudo(user.id)
    if removed:
        SUDOERS.remove(user.id)
        await message.reply_text(f"{user.mention} ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ sᴜᴅᴏ ᴜsᴇʀs.")
    else:
        await message.reply_text("ғᴀɪʟᴇᴅ ᴛᴏ ʀᴇᴍᴏᴠᴇ sᴜᴅᴏ ᴜsᴇʀ.")


# ⌬ sᴜᴅᴏ ʟɪsᴛ (ᴏɴʟʏ ғᴏʀ ᴏᴡɴᴇʀ & sᴜᴅᴏ)
@app.on_message(filters.command(["sudolist", "listsudo", "sudoers"]) & ~BANNED_USERS)
@language
async def sudoers_list(client, message: Message, _):
    if message.from_user.id not in SUDOERS:
        return await message.reply_text("ʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴠɪᴇᴡ ᴛʜɪs ʟɪsᴛ.")

    text = "˹ ᴛʜᴇ sᴜᴅᴏ ᴜsᴇʀs ˼\n\n"
    
    owner = await app.get_users(OWNER_ID)
    owner = owner.first_name if not owner.mention else owner.mention
    text += f"ᴏᴡɴᴇʀ ⌲ {owner}\n"

    count = 1
    for user_id in SUDOERS:
        if user_id != OWNER_ID:
            try:
                user = await app.get_users(user_id)
                user = user.first_name if not user.mention else user.mention
                text += f"sᴜᴅᴏ {count} ⌲ {user}\n"
                count += 1
            except:
                continue

    await message.reply_text(text)
