from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
from AnonXMusic.utils.database import get_sudoers

def stats_buttons(_, user_id):
    if user_id not in SUDO_USERS:
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="🚫 ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ",
                        callback_data="close",
                    )
                ]
            ]
        )
    
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["SA_B_2"],
                    callback_data="bot_stats_sudo",
                ),
                InlineKeyboardButton(
                    text=_["SA_B_3"],
                    callback_data="TopOverall",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ],
        ]
    )
    return upl


def back_stats_buttons(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="stats_back",
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ],
        ]
    )
    return upl


@app.on_callback_query(filters.regex("bot_stats_sudo"))
async def check_access(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in SUDO_USERS:
        await callback_query.answer(
            "ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ 🚫\n\nᴏɴʟʏ sᴜᴅᴏ ᴜsᴇʀs ᴄᴀɴ ᴠɪᴇᴡ ᴛʜɪs.",
            show_alert=True,
        )
        return
    await callback_query.message.edit_text("ʟᴏᴀᴅɪɴɢ sᴛᴀᴛs...")
