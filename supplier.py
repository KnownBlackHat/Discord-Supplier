#!/bin/python

import asyncio
import re
import sys

import aiohttp
import disnake

from utils import Embeds

_usage = "Usage: python supplier 'TITLE' 'SOURCE_URL | MESSAGE' " "'PREVIEW_IMG_URL'"

with open("webhooks.txt", "r") as file:
    WEBHOOKS: list = [line for line in file.readlines()]


async def encrypt(url: str) -> str:
    """Encrypts the url"""
    API_KEY = "5d7be8b0f901254621a61caefd3d2fd182a1cf07"
    URL = f"https://shrinkme.io/api?api={API_KEY}&url={url}"
    async with aiohttp.request("GET", URL) as response:
        response.raise_for_status()
        data = await response.json()
        if data["status"] == "success":
            return data["shortenedUrl"]
        elif data["status"] == "error":
            raise AttributeError("Invalid Url Passed")
        else:
            raise Exception("Api didn't reponded")


async def send_webhook(
    webhook_url,
    embed: disnake.Embed,
    username: str,
    content=None,
    avatar_url: str = "https://cdn.discordapp.com/avatars/1087375480304451727/"
    "f780c7c8c052c66c89f9270aebd63bc2.png?size=1024",
) -> None:
    """Sends Webhook to the guild"""
    async with aiohttp.ClientSession() as session:
        webhook = disnake.Webhook.from_url(webhook_url, session=session)
        await webhook.send(
            content, embed=embed, username=username, avatar_url=avatar_url
        )


async def main(title: str, payload: str, preview: None | str = None) -> None:
    try:
        if re.match(r"^(https?://)", payload):
            payload = f"**Link: {await encrypt(payload)}**"
        EMBED = Embeds.emb(disnake.Color.random(), title, payload).set_image(preview)

    except IndexError:
        raise AttributeError(f"Required arguments not passed\n{_usage}")
    for webhook in WEBHOOKS:
        await send_webhook(
            webhook_url=webhook,
            embed=EMBED,
            username="SUPPLIER",
            avatar_url="https://images7.alphacoders.com/115/1154879.png",
        )


asyncio.run(main(title=sys.argv[1], payload=sys.argv[2], preview=sys.argv[3]))
