from typing import Union
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from PIL import Image, ImageFont, ImageDraw
import base64
from io import BytesIO

app = FastAPI()

#text colour: #9881BC
background_img = Image.open("assets/discord_plain_bg.png")
font = ImageFont.truetype("assets/Gilroy-ExtraBold.ttf", 156)
user_icon = Image.open("assets/user_icon.png").convert("RGBA")

@app.get("/{user_count}")
def generate_banner(user_count):
    img = background_img.copy()
    draw = ImageDraw.Draw(img)
    width, _ = font.getsize(user_count)
    total_width = width+user_icon.width+16
    draw.text(((img.width/2-total_width/2)+user_icon.width+16, img.height/2 + 130), user_count, (152, 129, 188), font=font)
    img.paste(user_icon, (img.width//2-total_width//2, img.height//2 + 150), user_icon)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())

    return HTMLResponse(content=bytes("data:image/png;base64,", encoding="utf-8") + img_str, status_code=200)
    