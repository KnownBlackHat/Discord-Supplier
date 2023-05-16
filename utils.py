import datetime

import disnake


class Embeds:
    red = 0xFF0000
    green = 0x00FF00
    blue = 0x0000FF
    black = 0x000000
    orange = 0xFFA500
    yellow = 0xFFFF00

    @staticmethod
    def emb(color, name=None, value=None) -> disnake.Embed:
        """Returns a embed"""
        Em = disnake.Embed(color=color, title=name, description=value)
        Em.timestamp = datetime.datetime.utcnow()
        return Em
