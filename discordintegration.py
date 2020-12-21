from config import DISCORD_TOKEN, COMMAND_PREFIX
import characters
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=COMMAND_PREFIX)


def discord_integration(character_list):
    @bot.event
    async def on_ready():
        print(f'{bot.user.name} is online.')

    @bot.command(name='Help')
    async def helpme(ctx):
        response = "Help is on the way!"
        await ctx.send(response)

    @bot.command(name='CharacterList')
    async def characterlist(ctx):
        embed = discord.Embed(title=f"__**{ctx.guild.name} Characters:**__",
                              color=0x03f8fc,
                              timestamp=ctx.message.created_at)
        for x in character_list:
            print(x.name)

            embed.add_field(name=f'**{x.name}**',
                            value=f'> Gold: {x.gp}\n> Mirror Coins: {x.mc}\n> Exp: {x.xp}',
                            inline=False)
        response = embed
        await ctx.send(embed = response)

    @bot.command(name='CreateCharacter')
    async def create_character(ctx, name):
        characters.create_character(name)
        response = f'{name} has arrived!'
        await ctx.send(response)

    @bot.command(name='Ammend')
    async def ammend_character(ctx, name, attribute, mod):
        characters.find_character(search)

        await ctx.send(response)



    bot.run(DISCORD_TOKEN)
