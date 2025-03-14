import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch

from AnonXMusic import app
from config import YOUTUBE_IMG_URL


def resize_image(image, width, height):
    """Resize image while maintaining aspect ratio."""
    return image.resize((width, height), Image.LANCZOS)


def clean_text(text, max_length=60):
    """Shorten the title to fit within the image constraints."""
    words = text.split(" ")
    title = ""
    for word in words:
        if len(title) + len(word) < max_length:
            title += " " + word
    return title.strip()


async def get_thumb(videoid):
    """Generate a stylish thumbnail for a YouTube video."""
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    try:
        # 🔥 Fetch YouTube Video Data
        results = VideosSearch(videoid, limit=1)
        data = await results.get()
        
        if not data["result"]:
            return YOUTUBE_IMG_URL  # Return default image if no data
        
        result = data["result"][0]
        title = re.sub(r"\W+", " ", result.get("title", "Unknown Title")).title()
        duration = result.get("duration", "0:00")
        views = result.get("viewCount", {}).get("short", "Unknown Views")
        channel = result.get("channel", {}).get("name", "Unknown Channel")
        thumbnail_url = result["thumbnails"][-1]["url"].split("?")[0]

        # 🔥 Download Thumbnail
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail_url) as resp:
                if resp.status == 200:
                    async with aiofiles.open(f"cache/thumb{videoid}.png", "wb") as f:
                        await f.write(await resp.read())

        # 🔥 Open Image and Resize
        youtube = Image.open(f"cache/thumb{videoid}.png")
        youtube = resize_image(youtube, 1280, 720)
        
        # 🔥 Blur Background & Darken It
        bg = youtube.filter(ImageFilter.GaussianBlur(20))
        enhancer = ImageEnhance.Brightness(bg)
        bg = enhancer.enhance(0.6)  # Darken background
        
        # 🔥 Create Overlay Panel
        overlay = Image.new("RGBA", (900, 450), (0, 0, 0, 180))
        bg.paste(overlay, (190, 135), overlay)

        # 🔥 Album Cover (Rounded)
        album = youtube.crop((280, 170, 580, 470))
        mask = Image.new("L", (300, 300), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 300, 300), fill=255)
        album = album.resize((300, 300), Image.LANCZOS)
        bg.paste(album, (250, 210), mask)

        # 🔥 Draw Text
        draw = ImageDraw.Draw(bg)
        font_title = ImageFont.truetype("AnonXMusic/assets/font.ttf", 50)
        font_info = ImageFont.truetype("AnonXMusic/assets/font2.ttf", 35)
        
        draw.text((580, 215), unidecode(channel), fill="white", font=font_info)
        draw.text((580, 265), clean_text(title), fill="white", font=font_title)
        
        # 🔥 Progress Bar Calculation
        total_seconds = sum(
            int(x) * 60 ** i for i, x in enumerate(reversed(duration.split(":")))
        )
        progress = total_seconds // 4  # Assume 1/4 of video watched
        bar_length = 720  # Length of progress bar
        progress_length = int((progress / total_seconds) * bar_length) if total_seconds > 0 else 0

        # 🔥 Progress Bar Drawing
        draw.rectangle([(280, 550), (1000, 565)], fill=(150, 150, 150, 180))
        draw.rectangle([(280, 550), (280 + progress_length, 565)], fill=(255, 255, 255, 200))  

        # 🔥 Icons (Replace with real icons if needed)
        draw.text((230, 540), "⭐", fill="white", font=font_title)  # Favorite
        draw.text((1020, 540), "🎧", fill="white", font=font_title)  # Headphones
        
        # 🔥 Time Stamps
        draw.text((250, 580), "00:24", fill="white", font=font_info)
        draw.text((950, 580), duration, fill="white", font=font_info)
        
        # 🔥 Cleanup and Save
        os.remove(f"cache/thumb{videoid}.png")
        bg.save(f"cache/{videoid}.png")
        
        return f"cache/{videoid}.png"

    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL
