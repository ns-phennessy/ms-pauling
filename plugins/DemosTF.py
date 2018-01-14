"""
    Description:
        Lets you know your last demo from demostf

    Contributors:
        - Patrick Hennessy
"""
from arcbot import Plugin
from arcbot import command

import requests
import time
from datetime import datetime, timezone

class DemosTF(Plugin):
    @command("^demo$")
    def demos(self, event):
        self.bot.api.trigger_typing(event.channel_id)

        user = self.bot.users.find_one({"id": event.author.id})
        steam_id = user.get('steam_id', None)

        if steam_id is not None:
            response = requests.get(
                "https://api.demos.tf/demos/",
                params={"players[]": steam_id}
            )
            try:
                response.raise_for_status()
            except Exception as e:
                self.say(event.channel_id, "DemosTF machine broke :(")
                return

            demo_data = response.json()[0]

            date = datetime.fromtimestamp(demo_data['time'], timezone.utc).astimezone()
            date = date.strftime("%B %d, %Y @ %I:%M %p %Z")
            link = f"https://demos.tf/{demo_data['id']}"
            nick = demo_data['nick']
            blue_team = demo_data['blue']
            red_team = demo_data['red']
            map = demo_data['map']
            duration = time.strftime('%H:%M:%S', time.gmtime(demo_data['duration']))

            embed = {
                "title": f"{nick} - {blue_team} vs {red_team}",
                "description": f"*{date}*\n\n**{link}**",
                "fields": [
                    {
                        "name": "Map",
                        "value": f"{map}",
                        "inline": True
                    },
                    {
                        "name": "Duration",
                        "value": f"{duration}",
                        "inline": True
                    }
                ]
            }
            self.say(event.channel_id, embed=embed)
        else:
            self.say(event.channel_id, "Sorry, I don't have your steam id! Type `!steam <ID HERE>` to add it")
