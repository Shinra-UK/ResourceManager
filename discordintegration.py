from config import DISCORD_TOKEN, COMMAND_PREFIX
from discord.ext import commands

bot = commands.Bot(command_prefix=COMMAND_PREFIX)


def discord(character_list):
    @bot.event
    async def on_ready():
        print(f'{bot.user.name} is online.')

    @bot.command(name='Help')
    async def helpme(ctx):
        response = "Help is on the way!"
        await ctx.send(response)

    #bot.run(DISCORD_TOKEN)
    print(character_list)
    print("Goodbye World!")
