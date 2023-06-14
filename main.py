#!/bin/python

import asyncio
import logging
import re
from io import BytesIO
from typing import Optional, Set

import aiohttp
import disnake
from PIL import Image, ImageDraw, ImageFont

from utils import Embeds

_usage = "Format: TITLE;[SOURCE_URL | MESSAGE];PREVIEW_IMG_URL"
logger = logging.getLogger(__name__)

with open("webhooks.txt", "r") as file:
    WEBHOOKS: Set = {line for line in file.readlines()}


async def _req_img(img_url: str, session: aiohttp.ClientSession) -> BytesIO:
    async with session.get(img_url) as response:
        return BytesIO(await response.read())


def process_image(image: BytesIO, img_text: str) -> disnake.File:
    new_img = Image.open(image)
    font = ImageFont.truetype("fonts/Arial.ttf", 55)
    draw = ImageDraw.Draw(new_img)

    W, H = new_img.size
    _, _, w, h = draw.textbbox((0, 0), img_text, font=font)
    draw.text(
        ((W - w) / 2, (H - h) / 2), img_text, font=font, fill="white"
    )  # Change fill to your color
    file = BytesIO()
    new_img.save(file, "png")
    file.seek(0)
    logger.info("Image Processed")
    return disnake.File(fp=file, filename="image.png")


async def encrypt(url: str, session: aiohttp.ClientSession) -> str:
    """Encrypts the url"""
    API_KEY = "API_KEY"  # put your api key here
    URL = f"https://shrinkme.io/api?api={API_KEY}&url={url}"
    async with session.get(URL) as response:
        response.raise_for_status()
        data = await response.json()
        if data["status"] == "success":
            return data["shortenedUrl"]
        elif data["status"] == "error":
            raise AttributeError("Invalid Url Passed")
        else:
            raise Exception("Api didn't reponded")


async def send_webhook(
    webhook_url: str,
    username: str,
    avatar_url: str,
    session: aiohttp.ClientSession,
    embed: Optional[disnake.Embed] = None,
    content: Optional[str] = None,
) -> None:
    """Sends Webhook to the guild"""
    webhook = disnake.Webhook.from_url(webhook_url, session=session)
    if not embed:
        await webhook.send(content, username=username, avatar_url=avatar_url)
    else:
        await webhook.send(embed=embed, username=username, avatar_url=avatar_url)


async def broadcast(
    title: str,
    payload: str,
    img_text: str,
    session: aiohttp.ClientSession,
    preview: Optional[str] = None,
    ads=True,
) -> None:
    if re.match(r"^(https?://)", payload):
        payload = (
            f"**Link: {(await encrypt(payload, session=session)) if ads else payload}**"
        )
    embed = Embeds.emb(disnake.Color.random(), title, payload)
    for webhook in WEBHOOKS:
        if preview:
            image = await _req_img(img_url=preview, session=session)
            img_file = await asyncio.get_running_loop().run_in_executor(
                None, process_image, image, img_text
            )
            embed = Embeds.emb(disnake.Color.random(), title, payload).set_image(
                file=img_file
            )
        await send_webhook(
            webhook_url=webhook,
            embed=embed,
            username="SUPPLIER",
            avatar_url="https://images7.alphacoders.com/115/1154879.png",
            session=session,
        )


async def main():
    with open("contents.dat", "r") as file:
        lines = set(file.readlines())

    for line in lines:
        try:
            title, payload, preview = line.split(";")
        except Exception:
            raise Exception(_usage)

        async with aiohttp.ClientSession() as session:
            await broadcast(
                title=title,
                payload=payload,
                preview=preview,
                ads=True,  # ads=False to disable ads
                img_text="Hello World",  # Replace with your text
                session=session,
            )
    logger.info("Successfully Broadcasted")


asyncio.run(main())
