import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch
from AnonXMusic import app
from config import YOUTUBE_IMG_URL

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

def truncate(text):
    words = text.split(" ")
    text1, text2 = "", ""
    for word in words:
        if len(text1) + len(word) < 30:
            text1 += " " + word
        elif len(text2) + len(word) < 30:
            text2 += " " + word
    return [text1.strip(), text2.strip()]

def crop_center_circle(img, output_size, border, glow_intensity=20):
    half_w, half_h = img.size[0] / 2, img.size[1] / 2
    crop_size = int(output_size * 1.5)
    img = img.crop((half_w - crop_size / 2, half_h - crop_size / 2, half_w + crop_size / 2, half_h + crop_size / 2))
    img = img.resize((output_size - 2 * border, output_size - 2 * border))

    final_img = Image.new("RGBA", (output_size, output_size), "black")
    mask_main = Image.new("L", (output_size - 2 * border, output_size - 2 * border), 0)
    draw_main = ImageDraw.Draw(mask_main)
    draw_main.ellipse((0, 0, output_size - 2 * border, output_size - 2 * border), fill=255)
    final_img.paste(img, (border, border), mask_main)

    glow = final_img.filter(ImageFilter.GaussianBlur(glow_intensity))
    final_img.paste(glow, (0, 0), glow)

    return final_img

async def get_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}_radio.png"):
        return f"cache/{videoid}_radio.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    results = VideosSearch(url, limit=1)
    for result in (await results.next())["result"]:
        try:
            title = re.sub("\W+", " ", result["title"]).title()
        except:
            title = "Unknown Title"
        try:
            duration = result["duration"]
        except:
            duration = "Unknown Mins"
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        try:
            views = result["viewCount"]["short"]
        except:
            views = "Unknown Views"
        try:
            channel = result["channel"]["name"]
        except:
            channel = "Unknown Channel"

    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    youtube = Image.open(f"cache/thumb{videoid}.png")
    image1 = changeImageSize(1280, 720, youtube)
    image2 = image1.convert("RGBA")
    
    background = image2.filter(ImageFilter.GaussianBlur(15))
    enhancer = ImageEnhance.Brightness(background)
    background = enhancer.enhance(0.4)
    
    draw = ImageDraw.Draw(background)
    title_font = ImageFont.truetype("AnonXMusic/assets/font3.ttf", 45)
    info_font = ImageFont.truetype("AnonXMusic/assets/font2.ttf", 30)
    
    circle_thumbnail = crop_center_circle(youtube, 450, 25, glow_intensity=30)
    background.paste(circle_thumbnail, (120, 160), circle_thumbnail)

    text_x_position = 600
    title1 = truncate(title)
    draw.text((text_x_position, 180), title1[0], fill=(255, 255, 255), font=title_font)
    draw.text((text_x_position, 230), title1[1], fill=(255, 255, 255), font=title_font)
    draw.text((text_x_position, 320), f"{channel}  |  {views[:23]}", fill=(255, 255, 255), font=info_font)

    progress_bar_x = text_x_position
    progress_bar_y = 380
    progress_width = 600

    completed_width = int(progress_width * 0.6)
    draw.line([(progress_bar_x, progress_bar_y), (progress_bar_x + completed_width, progress_bar_y)], fill="red", width=10)
    draw.line([(progress_bar_x + completed_width, progress_bar_y), (progress_bar_x + progress_width, progress_bar_y)], fill="white", width=8)

    circle_radius = 10
    circle_position = (progress_bar_x + completed_width, progress_bar_y)
    draw.ellipse([circle_position[0] - circle_radius, circle_position[1] - circle_radius,
                  circle_position[0] + circle_radius, circle_position[1] + circle_radius], fill="red")
    
    draw.text((progress_bar_x, 400), "00:00", (255, 255, 255), font=info_font)
    draw.text((progress_bar_x + progress_width - 80, 400), duration, (255, 255, 255), font=info_font)

    play_icons = Image.open("AnonXMusic/assets/play_icons.png")
    play_icons = play_icons.resize((580, 62))
    background.paste(play_icons, (progress_bar_x, 450), play_icons)

    try:
        os.remove(f"cache/thumb{videoid}.png")
    except:
        pass
    
    background.save(f"cache/{videoid}_radio.png")
    return f"cache/{videoid}_radio.png"
