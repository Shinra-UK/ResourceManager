from config import DISCORD_TOKEN, COMMAND_PREFIX
from discord.ext import commands

bot = commands.Bot(command_prefix=COMMAND_PREFIX)

def discord():
    print(DISCORD_TOKEN)
    print(COMMAND_PREFIX)

    @bot.event
    async def on_ready():
        print(f'{bot.user.name} is online.')

    bot.run(DISCORD_TOKEN)

    print("Goodbye World!")