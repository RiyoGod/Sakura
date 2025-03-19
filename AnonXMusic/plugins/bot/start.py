import time
import random
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from AnonXMusic import app
from AnonXMusic.misc import _boot_
from AnonXMusic.plugins.sudo.sudoers import sudoers_list
from AnonXMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from AnonXMusic.utils.decorators.language import LanguageStart
from AnonXMusic.utils.formatters import get_readable_time
from AnonXMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string

# 📌 Random Start Images
START_IMAGES = [
    "https://files.catbox.moe/tycblb.jpg",
    "https://files.catbox.moe/6eisf0.jpg",
    "https://files.catbox.moe/31xhoe.jpg",
    "https://files.catbox.moe/enj0uu.jpg",
    "https://files.catbox.moe/k8kj67.jpg",
    "https://files.catbox.moe/i87dkb.jpg",
    "https://files.catbox.moe/zwdy84.jpg",
]

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    start_image = random.choice(START_IMAGES)

    args = message.text.split()
    if len(args) > 1:
        name = args[1]

        if name.startswith("help"):
            keyboard = help_pannel(_)
            return await message.reply_photo(
                photo=start_image,
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )

        if name.startswith("sud"):
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"**{message.from_user.mention} ᴊᴜsᴛ ᴄʜᴇᴄᴋᴇᴅ sᴜᴅᴏʟɪsᴛ.**\n\n"
                         f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                         f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
            return

        if name.startswith("inf"):
            m = await message.reply_text("🔎 Searching...")
            query = f"https://www.youtube.com/watch?v={name.replace('info_', '', 1)}"
            results = VideosSearch(query, limit=1)
            result_data = (await results.next())["result"]

            if not result_data:
                return await m.edit("❌ No results found.")

            result = result_data[0]
            searched_text = _["start_6"].format(
                result["title"],
                result["duration"],
                result["viewCount"]["short"],
                result["publishedTime"],
                result["channel"]["link"],
                result["channel"]["name"],
                app.mention,
            )
            key = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(text=_["S_B_8"], url=result["link"]),
                    InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                ]]
            )

            await m.delete()
            await app.send_photo(
                chat_id=message.chat.id,
                photo=result["thumbnails"][0]["url"].split("?")[0],
                caption=searched_text,
                reply_markup=key,
            )
            return

    # Default start message
    out = private_panel(_)
    await message.reply_photo(
        photo=start_image,
        caption=_["start_2"].format(message.from_user.mention, app.mention),
        reply_markup=InlineKeyboardMarkup(out),
    )
    
    if await is_on_off(2):
        return await app.send_message(
            chat_id=config.LOGGER_ID,
            text=f"<b>{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.</b>\n\n"
                 f"<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
                 f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
        )

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    start_image = random.choice(START_IMAGES)

    await message.reply_photo(
        photo=start_image,
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)

@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass

            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)

                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                start_image = random.choice(START_IMAGES)

                await message.reply_photo(
                    photo=start_image,
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)
