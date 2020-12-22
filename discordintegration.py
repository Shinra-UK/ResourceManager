from config import DISCORD_TOKEN, COMMAND_PREFIX
import characters
import settlements
import utilities
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=COMMAND_PREFIX, case_insensitive=True)

entities = {'Character': characters.Character,
            'Settlement': settlements.Settlement,
            'Characters': characters.Character,
            'Settlements': settlements.Settlement,
            'All': utilities.Entity,
            'C': characters.Character,
            'S': settlements.Settlement,
            'A': utilities.Entity
            }


def discord_integration():
    @bot.event
    async def on_ready():
        print(f'{bot.user.name} is online.')

    @bot.command(name='HelpMe')
    async def help_me(ctx):
        response = "Help is on the way!"
        await ctx.send(response)

    @bot.command(name='List')
    async def list_entities(ctx, entity_type):
        entity_type = entity_type.title()
        embed = discord.Embed(title=f"__**{ctx.guild.name} {entity_type}:**__",
                              color=0x03f8fc,
                              timestamp=ctx.message.created_at)
        for x in entities[entity_type].directory:
            print(x.name)
            value = f""
            for y in x.AMENDABLE:
                if y != 0:
                    value += f'> {y}: {getattr(x, y)}\n'

            embed.add_field(name=f'**{x.name}**',
                            value=value,
                            # value=f'> Gold: {x.gp}\n> Mirror Coins: {x.mc}\n> Exp: {x.xp}',
                            inline=False)
        response = embed
        await ctx.send(embed=response)

    @bot.command(name='Create')
    async def create(ctx, entity_type, name):
        entity_type = entity_type.title()
        entity = entities[entity_type]
        new = utilities.create(entity, name)
        response = new.msg
        await ctx.send(response)

    @bot.command(name='Amend')
    async def amend(ctx, entity_type, name, attribute, mod):
        entity_type = entity_type.title()
        attribute = attribute.lower()
        entity = utilities.find(entities[entity_type].directory, "name", name.title())
        if entity is None:
            response = f"Unable to find a {entity_type} with the name {name}"
        else:
            response = entity.amend(attribute, mod)
        await ctx.send(response)

    bot.run(DISCORD_TOKEN)
