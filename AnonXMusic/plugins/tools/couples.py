import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

COUPLE_QUOTES = [
    "💓 **ʟᴏᴠᴇ ɪꜱɴ'ᴛ ᴀʙᴏᴜᴛ ᴘᴇʀꜰᴇᴄᴛɪᴏɴ, ɪᴛ'ꜱ ᴀʙᴏᴜᴛ ꜰɪɴᴅɪɴɢ ꜱᴏᴍᴇᴏɴᴇ ᴡʜᴏ ᴍᴀᴋᴇꜱ ʏᴏᴜ ᴘᴇʀꜰᴇᴄᴛʟʏ ᴄᴏᴍᴘʟᴇᴛᴇ.** 🦋",
    "🦋 **ʟᴏᴠᴇ ɪꜱ ᴀ ᴊᴏᴜʀɴᴇʏ ᴡɪᴛʜ ᴛʜᴇ ʀɪɢʜᴛ ᴘᴇʀꜱᴏɴ ʙʏ ʏᴏᴜʀ ꜱɪᴅᴇ.** 💓",
    "💓 **ᴡʜᴇɴ ʜᴇᴀʀᴛꜱ ʙᴇᴀᴛ ᴀꜱ ᴏɴᴇ, ᴅᴇꜱᴛɪɴʏ ᴘʟᴀʏꜱ ɪᴛꜱ ᴘᴀʀᴛ.** 🦋",
    "🦋 **ɪɴ ᴛʜᴇ ʙᴏᴏᴋ ᴏꜰ ʟɪꜰᴇ, ʏᴏᴜ ᴀʀᴇ ᴛʜᴇ ᴄʜᴀᴘᴛᴇʀ ɪ ɴᴇᴠᴇʀ ᴡᴀɴᴛ ᴛᴏ ᴇɴᴅ.** 💓"
]

@Client.on_message(filters.command("couples") & filters.group)
async def random_couple(client, message):
    chat_id = message.chat.id
    members = [u for u in await client.get_chat_members(chat_id) if not u.user.is_bot]

    if len(members) < 2:
        await message.reply("💓 **ɴᴏᴛ ᴇɴᴏᴜɢʜ ᴍᴇᴍʙᴇʀꜱ ᴛᴏ ꜰᴏʀᴍ ᴀ ᴄᴏᴜᴘʟᴇ!** 🦋")
        return

    user1, user2 = random.sample(members, 2)

    caption = f"""
**➤ "ʀᴀɴᴅᴏᴍ ᴄᴏᴜᴘʟᴇ ᴏꜰ ᴛʜᴇ ᴅᴀʏ"**  

💓 **ᴅᴇꜱᴛɪɴʏ ʜᴀꜱ ᴄʜᴏꜱᴇɴ:**  
➛ **[{user1.user.first_name}](tg://user?id={user1.user.id})**  
➛ **[{user2.user.first_name}](tg://user?id={user2.user.id})**  

🦋 **ʟᴏᴠᴇ ꜰɪɴᴅꜱ ɪᴛꜱ ᴡᴀʏ ᴛᴏ ᴛʜᴏꜱᴇ ᴡʜᴏ ʙᴇʟɪᴇᴠᴇ.**  

{random.choice(COUPLE_QUOTES)}
    """

    buttons = [
        [
            InlineKeyboardButton(
                text=f"💓 {user1.user.first_name}",
                url=f"tg://user?id={user1.user.id}"
            ),
            InlineKeyboardButton(
                text=f"🦋 {user2.user.first_name}",
                url=f"tg://user?id={user2.user.id}"
            )
        ]
    ]

    await message.reply_text(caption, reply_markup=InlineKeyboardMarkup(buttons))
