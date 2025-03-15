import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch

# Import from your project
from AnonXMusic import app
from config import YOUTUBE_IMG_URL

from io import BytesIO

async def download_image(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return Image.open(BytesIO(await resp.read()))

def add_rounded_corners(image, radius=40):
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), image.size], radius, fill=255)
    image.putalpha(mask)
    return image

async def generate_music_thumbnail(video_title, artist, duration, current_time, thumbnail_url):
    # Load YouTube thumbnail
    bg_image = await download_image(thumbnail_url)
    bg_image = bg_image.resize((1280, 720)).filter(ImageFilter.GaussianBlur(15))

    # Create main UI overlay
    overlay = Image.new("RGBA", (900, 500), (0, 0, 0, 150))  # Semi-transparent black
    overlay = add_rounded_corners(overlay, 50)

    # Load album art and add rounded corners
    album_art = await download_image(thumbnail_url)
    album_art = album_art.resize((200, 200))
    album_art = add_rounded_corners(album_art, 30)

    # Create final image
    final_image = Image.new("RGBA", (1280, 720))
    final_image.paste(bg_image, (0, 0))
    final_image.paste(overlay, (190, 110), overlay)
    final_image.paste(album_art, (220, 170), album_art)

    # Load font
    font_path = "AnonXMusic/assets/font3.ttf"  # Update this path
    title_font = ImageFont.truetype(font_path, 50)
    artist_font = ImageFont.truetype(font_path, 35)
    progress_font = ImageFont.truetype(font_path, 30)

    draw = ImageDraw.Draw(final_image)

    # Add song title & artist
    draw.text((450, 180), video_title, font=title_font, fill="white")
    draw.text((450, 250), artist, font=artist_font, fill="white")

    # Progress bar
    bar_x, bar_y = 450, 350
    bar_width, bar_height = 350, 10
    progress = current_time / duration  # Percentage completion

    # Draw empty progress bar
    draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_height], 5, fill=(100, 100, 100, 200))
    
    # Draw filled progress
    draw.rounded_rectangle([bar_x, bar_y, bar_x + (bar_width * progress), bar_y + bar_height], 5, fill="white")

    # Draw timestamps
    draw.text((bar_x - 40, bar_y - 10), f"{int(current_time // 60)}:{int(current_time % 60):02d}", font=progress_font, fill="white")
    draw.text((bar_x + bar_width + 10, bar_y - 10), f"{int(duration // 60)}:{int(duration % 60):02d}", font=progress_font, fill="white")

    # Save or show
    final_image.show()
    final_image.save("music_thumbnail.png")

# Example usage
video_title = "Junoon"
artist = "MITRAZ"
duration = 168  # 2:48 in seconds
current_time = 24  # Progress time
thumbnail_url = f"{YOUTUBE_IMG_URL}/vi/VIDEO_ID/maxresdefault.jpg"  # Replace VIDEO_ID with actual ID

import asyncio
asyncio.run(generate_music_thumbnail(video_title, artist, duration, current_time, thumbnail_url))
