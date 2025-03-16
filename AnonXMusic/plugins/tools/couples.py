/eval import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from AnonXMusic import app  # Use your bot instance

COUPLE_QUOTES = [
    "💓 <b>ʟᴏᴠᴇ ɪsɴ'ᴛ ғᴏᴜɴᴅ, ɪᴛ's ᴄʀᴇᴀᴛᴇᴅ ʙʏ ᴛᴡᴏ ʜᴇᴀʀᴛs ᴛʜᴀᴛ ʙᴇᴀᴛ ᴀs ᴏɴᴇ.</b>",
    "🦋 <b>ᴛʜᴇ ʙᴇsᴛ ʟᴏᴠᴇ ᴡᴀs ɴᴇᴠᴇʀ ᴘʟᴀɴɴᴇᴅ, ɪᴛ ʜᴀᴘᴘᴇɴᴇᴅ ᴡɪᴛʜ ᴛʜᴇ ʀɪɢʜᴛ ᴘᴇʀsᴏɴ.</b>",
    "💓 <b>ʏᴏᴜ ᴅᴏɴ'ᴛ ɴᴇᴇᴅ ᴛᴏ ғɪɴᴅ ʟᴏᴠᴇ, ʟᴏᴠᴇ ᴡɪʟʟ ғɪɴᴅ ʏᴏᴜ.</b>",
    "🦋 <b>ʟᴏᴠᴇ ɪsɴ'ᴛ ᴀ ᴅᴇsᴛɪɴᴀᴛɪᴏɴ, ɪᴛ's ᴀ ᴊᴏᴜʀɴᴇʏ ᴛʜᴀᴛ sᴛᴀʀᴛs ᴡɪᴛʜ ᴛʜᴇ ʀɪɢʜᴛ ᴘᴇʀsᴏɴ.</b>",
    "💓 <b>ʀᴇᴀʟ ʟᴏᴠᴇ ʜᴀᴘᴘᴇɴs ᴡʜᴇɴ ᴛᴡᴏ sᴏᴜʟs ᴄᴏɴɴᴇᴄᴛ, ɴᴏᴛ ᴊᴜsᴛ ʜᴇᴀʀᴛs.</b>",
    "🦋 <b>ᴍᴀʏʙᴇ ʏᴏᴜ'ʀᴇ ᴛʜᴇ ᴍɪʀᴀᴄʟᴇ ᴛʜᴀᴛ sᴏᴍᴇᴏɴᴇ ʜᴀs ʙᴇᴇɴ ᴡᴀɪᴛɪɴɢ ғᴏʀ.</b>",
    "💓 <b>ʟᴏᴠᴇ ᴅᴏᴇsɴ'ᴛ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴘᴇʀғᴇᴄᴛ, ɪᴛ ᴊᴜsᴛ ɴᴇᴇᴅs ᴛᴏ ʙᴇ ᴛʀᴜᴇ.</b>",
    "🦋 <b>ʜᴇᴀʀᴛs ᴛʜᴀᴛ ʀᴇsᴏɴᴀᴛᴇ ᴄᴀɴ ɴᴇᴠᴇʀ ʙᴇ ᴘᴜʟʟᴇᴅ ᴀᴘᴀʀᴛ.</b>",
    "💓 <b>ʟᴏᴠᴇ ɪsɴ'ᴛ ᴀʙᴏᴜᴛ ғɪɴᴅɪɴɢ ᴛʜᴇ ᴘᴇʀғᴇᴄᴛ ᴘᴇʀsᴏɴ, ɪᴛ's ᴀʙᴏᴜᴛ sᴇᴇɪɴɢ ᴀɴ ɪᴍᴘᴇʀғᴇᴄᴛ ᴘᴇʀsᴏɴ ᴘᴇʀғᴇᴄᴛʟʏ.</b>",
    "🦋 <b>ᴛʜᴇ ᴏɴᴇ ᴡʜᴏ ᴛʀᴜʟʏ ʟᴏᴠᴇs ʏᴏᴜ ᴡɪʟʟ ɴᴇᴠᴇʀ ʟᴇᴛ ɢᴏ, ɴᴏ ᴍᴀᴛᴛᴇʀ ʜᴏᴡ ᴛᴏᴜɢʜ ᴛɪᴍᴇs ɢᴇᴛ.</b>",
    "💓 <b>ʟᴏᴠᴇ ɪs ᴀ ᴘʀᴏᴍɪsᴇ ᴏғ ᴇᴛᴇʀɴɪᴛʏ, ɴᴏᴛ ᴊᴜsᴛ ᴀ ᴍᴏᴍᴇɴᴛ ɪɴ ᴛɪᴍᴇ.</b>",
    "🦋 <b>ɪɴ ᴛʜᴇ ᴇɴᴅ, ᴡᴇ ᴏɴʟʏ ʀᴇɢʀᴇᴛ ᴛʜᴇ ʟᴏᴠᴇ ᴡᴇ ᴡᴇʀᴇ ᴛᴏᴏ sᴄᴀʀᴇᴅ ᴛᴏ ɢɪᴠᴇ.</b>",
    "💓 <b>ᴛʀᴜᴇ ʟᴏᴠᴇ ʜᴀs ɴᴏ ᴅᴇsɪɢɴ, ɪᴛ ᴊᴜsᴛ ʜᴀᴘᴘᴇɴs.</b>",
    "🦋 <b>ᴇᴠᴇʀʏ ʟᴏᴠᴇ sᴛᴏʀʏ ɪs ʙᴇᴀᴜᴛɪғᴜʟ, ʙᴜᴛ ᴏᴜʀs ɪs ᴍʏ ғᴀᴠᴏʀɪᴛᴇ.</b>",
    "💓 <b>ʟᴏᴠᴇ ɪs ᴀ ʟᴀɴɢᴜᴀɢᴇ ᴏғ ᴛʜᴇ ʜᴇᴀʀᴛ, ɴᴏᴛ ᴏғ ᴛʜᴇ ᴍɪɴᴅ.</b>",
    "🦋 <b>ᴏɴᴄᴇ ɪɴ ᴀ ʟɪғᴇᴛɪᴍᴇ, ʏᴏᴜ ғɪɴᴅ sᴏᴍᴇᴏɴᴇ ᴡʜᴏ ᴄʜᴀɴɢᴇs ᴇᴠᴇʀʏᴛʜɪɴɢ.</b>",
    "💓 <b>ᴛʜᴇ ʀɪɢʜᴛ ᴘᴇʀsᴏɴ ᴅᴏᴇsɴ'ᴛ ᴄᴏᴍᴇ ʙʏ ᴄʜᴀɴᴄᴇ, ᴛʜᴇʏ ᴀʀᴇ ᴀ ʙʟᴇssɪɴɢ.</b>",
    "🦋 <b>ᴛʜᴇ ʙᴇᴀᴜᴛʏ ᴏғ ʟᴏᴠᴇ ɪs ɴᴏᴛ ɪɴ ᴛʜᴇ ᴘᴇʀғᴇᴄᴛɪᴏɴ, ʙᴜᴛ ɪɴ ᴛʜᴇ ᴀᴄᴄᴇᴘᴛᴀɴᴄᴇ.</b>",
    "💓 <b>ʟᴏᴠᴇ ɪs ᴛʜᴇ ᴏɴʟʏ ᴛʜɪɴɢ ᴛʜᴀᴛ ɢʀᴏᴡs ᴡʜᴇɴ ɪᴛ's sʜᴀʀᴇᴅ.</b>",
    "🦋 <b>ɴᴏ ᴍᴀᴛᴛᴇʀ ᴡʜᴇʀᴇ ʟɪғᴇ ᴛᴀᴋᴇs ᴜs, ʀᴇᴀʟ ʟᴏᴠᴇ ᴀʟᴡᴀʏs ғɪɴᴅs ᴀ ᴡᴀʏ.</b>",
]

@app.on_message(filters.command("couples") & filters.group)
async def random_couple(client, message):
    chat_id = message.chat.id
    members = []

    async for member in client.get_chat_members(chat_id):
        if not member.user.is_bot:  # Exclude bots
            members.append(member.user)

    if len(members) < 2:
        await message.reply_text("Not enough members to form a couple.")
        return

    user1, user2 = random.sample(members, 2)  # Select two random users
    quote = random.choice(COUPLE_QUOTES)  # Select random quote

    couple_text = f"""<b>➠ ʀᴀɴᴅᴏᴍ ᴄᴏᴜᴘʟᴇ ᴏꜰ ᴛʜᴇ ᴅᴀʏ 💓</b>

 <b>💓 ᴅᴇsᴛɪɴʏ ʜᴀs ᴄʜᴏsᴇɴ: </b>
➛ {user1.mention}  
➛ {user2.mention}  

 {quote}"""

    buttons = [
        [InlineKeyboardButton(user1.first_name, url=f"tg://openmessage?user_id={user1.id}")],
        [InlineKeyboardButton(user2.first_name, url=f"tg://openmessage?user_id={user2.id}")],
    ]

    await message.reply_text(couple_text, reply_markup=InlineKeyboardMarkup(buttons))
