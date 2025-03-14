import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch
from AnonXMusic import app
from config import YOUTUBE_IMG_URL


def resize_image(max_width, max_height, image):
    width_ratio = max_width / image.size[0]
    height_ratio = max_height / image.size[1]
    new_width = int(width_ratio * image.size[0])
    new_height = int(height_ratio * image.size[1])
    return image.resize((new_width, new_height))


def clean_title(text):
    words = text.split(" ")
    title = ""
    for word in words:
        if len(title) + len(word) < 40:  # Shorter title for better UI
            title += " " + word
    return title.strip()


async def get_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = re.sub(r"\W+", " ", result["title"]).title()
            except:
                title = "Unknown Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Duration"
            thumbnail_url = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Artist"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail_url) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        # Load image & apply blur for background
        youtube = Image.open(f"cache/thumb{videoid}.png")
        bg_image = resize_image(1280, 720, youtube).convert("RGBA")
        blurred_bg = bg_image.filter(ImageFilter.GaussianBlur(20))
        enhancer = ImageEnhance.Brightness(blurred_bg)
        blurred_bg = enhancer.enhance(0.5)

        # Create a pocket-style music player overlay
        player_ui = Image.new("RGBA", (500, 600), (25, 25, 25, 240))
        draw = ImageDraw.Draw(player_ui)
        draw.rounded_rectangle((0, 0, 500, 600), radius=50, fill=(30, 30, 30, 240))

        # Load fonts
        title_font = ImageFont.truetype("AnonXMusic/assets/font.ttf", 40)
        artist_font = ImageFont.truetype("AnonXMusic/assets/font2.ttf", 28)
        time_font = ImageFont.truetype("AnonXMusic/assets/font2.ttf", 25)

        # Draw text (Title, Artist)
        draw.text((50, 320), clean_title(title), (255, 255, 255), font=title_font)
        draw.text((50, 370), f"L {channel}", (180, 180, 180), font=artist_font)

        # Draw Progress Bar
        draw.rectangle((50, 450, 450, 460), fill=(200, 200, 200, 200))
        draw.rectangle((50, 450, 250, 460), fill=(255, 0, 0, 200))  # Progress

        # Draw Time Stamps
        draw.text((50, 470), "00:00", (255, 255, 255), font=time_font)
        draw.text((400, 470), duration, (255, 255, 255), font=time_font)

        # Draw Play/Pause Button
        draw.ellipse((210, 510, 290, 590), fill=(255, 0, 0, 220))
        draw.text((230, 525), "▶", (255, 255, 255), font=ImageFont.truetype("AnonXMusic/assets/font.ttf", 50))

        # Merge everything
        final_image = bg_image.copy()
        final_image.paste(player_ui, (390, 60), player_ui)

        # Save final thumbnail
        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
        final_image.save(f"cache/{videoid}.png")
        return f"cache/{videoid}.png"

    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL
