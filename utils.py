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
        Em.set_footer(
            text="MR ROBOT",
            icon_url="https://cdn.discordapp.com/avatars/1087375480304451727/"
            "f780c7c8c052c66c89f9270aebd63bc2.png?size=1024",
        )
        return Em
