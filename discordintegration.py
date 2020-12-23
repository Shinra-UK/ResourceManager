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
    async def list_entities(ctx, entity_type="All"):
        entity_type = entity_type.title()
        embed = discord.Embed(title=f"__**{ctx.guild.name} {entity_type}:**__",
                              color=0x03f8fc,
                              timestamp=ctx.message.created_at)
        directory = entities.get(entity_type, utilities.Entity).directory
        for entity in directory:
            print(entity.name)
            field_value = f""

            for amendable in entity.AMENDABLE:
                attribute_value = getattr(entity, amendable)
                if attribute_value != 0:
                    print(f'> {amendable}: {attribute_value}\n')
                    field_value += f'> {amendable}: {attribute_value}\n'

            for editable in entity.EDITABLE:
                attribute_value = getattr(entity, editable)
                if attribute_value != "":
                    print(f'> {editable}: {attribute_value}\n')
                    field_value += f'> {editable}: {attribute_value}\n'

            if field_value == f"":
                field_value = f"> empty"
            embed.add_field(name=f'**{entity.name}**',
                            value=field_value,
                            # field_value=f'> Gold: {entity.gp}\n> Mirror Coins: {entity.mc}\n> Exp: {entity.xp}',
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

    @bot.command(name='Edit')
    async def edit(ctx, entity_type, name, attribute, new):
        entity_type = entity_type.title()
        attribute = attribute.lower()
        entity = utilities.find(entities[entity_type].directory, "name", name.title())
        if entity is None:
            response = f"Unable to find a {entity_type} with the name {name}"
        else:
            response = entity.edit(attribute, new)
        await ctx.send(response)

    bot.run(DISCORD_TOKEN)
