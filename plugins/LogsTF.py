"""
    Description:
        Lets you know your last logs in logtf

    Contributors:
        - Patrick Hennessy
"""
from arcbot import Plugin
from arcbot import command

import requests
import time
from datetime import datetime, timezone

class LogsTF(Plugin):
    @command("^logs$", trigger="!")
    def logs(self, event):
        self.bot.api.trigger_typing(event.channel_id)

        user = self.bot.users.find_one({"id": event.author.id})
        steam_id = user.get('steam_id', None)

        if steam_id is not None:
            response = requests.get(
                "https://logs.tf/json_search",
                params={"player": steam_id, "limit": 1}
            )
            try:
                response.raise_for_status()
            except Exception as e:
                self.say(event.channel_id, "LogsTF machine broke :(")
                return

            log_data = response.json()["logs"][0]

            date = datetime.fromtimestamp(log_data['date'], timezone.utc).astimezone()
            date = date.strftime("%B %d, %Y @ %I:%M %p %Z")
            link = f"https://logs.tf/{log_data['id']}"
            title = log_data['title']

            embed = {
                "title": title,
                "description": f"*{date}*\n\n**{link}**"
            }
            self.say(event.channel_id, embed=embed)
        else:
            self.say(event.channel_id, "Sorry, I don't have your steam id! Type `!steam <ID HERE>` to add it")
