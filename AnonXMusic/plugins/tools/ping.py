import random
from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message

from AnonXMusic import app
from AnonXMusic.core.call import Anony
from AnonXMusic.utils import bot_sys_stats
from AnonXMusic.utils.decorators.language import language
from AnonXMusic.utils.inline import supp_markup
from config import BANNED_USERS

# Define 4 Ping Images
PING_IMAGES = [
    "https://files.catbox.moe/rpzdyk.jpg",
    "https://files.catbox.moe/u0ljod.jpg",
    "https://files.catbox.moe/6g1avn.jpg",
    "https://files.catbox.moe/sudvc2.jpg",
]

@app.on_message(filters.command(["ping"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()

    # Select a random ping image
    ping_image = random.choice(PING_IMAGES)

    response = await message.reply_photo(
        photo=ping_image,
        caption=_["ping_1"].format(app.mention),
    )

    pytgping = await Anony.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000

    await response.edit_text(
        _["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping),
        reply_markup=supp_markup(_),
    )
