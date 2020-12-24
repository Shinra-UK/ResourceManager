from config import DISCORD_TOKEN, COMMAND_PREFIX, ADMIN_ROLE_ID, PLAYER_ROLE_ID
import characters
import settlements
import maps
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
NEIGHBOURS = (("nw", "n", "ne"), ("w", "c", "e"), ("sw", "s", "se"))


def discord_integration():
    def check_membership(ctx, role_id):
        print(role_id in ctx.author.roles)
        for role in ctx.author.roles:
            match = role_id == role.id
            if match:
                return match

    async def is_admin(ctx):
        return check_membership(ctx, ADMIN_ROLE_ID)

    async def is_player(ctx):
        return check_membership(ctx, PLAYER_ROLE_ID)

    @bot.event
    async def on_ready():
        print(f'{bot.user.name} is online.')

    @bot.command(name='HelpMe')
    @commands.check(is_player)
    async def help_me(ctx):
        response = "Help is on the way!"
        await ctx.send(response)

    @bot.command(name='List')
    @commands.check(is_admin)
    async def list_entities(ctx, entity_type="All"):
        entity_type = entity_type.title()
        embed = discord.Embed(title=f"__**{ctx.guild.name} {entity_type}:**__",
                              color=0x03f8fc,
                              timestamp=ctx.message.created_at)
        directory = entities.get(entity_type, utilities.Entity).directory
        for entity in directory:
            field_value = utilities.build_table(entity, *[*entity.AMENDABLE, *entity.EDITABLE])

            if field_value == f"":
                field_value = f"> empty"
            embed.add_field(name=f'**{entity.name}**',
                            value=field_value,
                            inline=False)
        response = embed
        await ctx.send(embed=response)

#Does not convert -1's
    @bot.command(name='Map')
    @commands.check(is_admin)
    async def embed_map(ctx, center_coordinates=(0, 0, 0)):
        if isinstance(center_coordinates[0], str):
            conversion = []
            for i in center_coordinates:
                if len(conversion) < 3:
                    try:
                        conversion.append(int(i))
                    except:
                        print(f'{i} cannot be converted to an int')
                        pass
                else:
                    break
            center_coordinates = tuple(int(i) for i in conversion)

        if isinstance(center_coordinates, tuple):
            center = maps.find_fragment(center_coordinates)
            center.update_neighbours()

            embed = discord.Embed(title=f"__**Map of Surrounding Area: {center.name} - {center.coordinates}:**__",
                                  color=0x03f8fc,
                                  timestamp=ctx.message.created_at)

            for line in NEIGHBOURS:
                for neighbour in line:
                    current_neighbour = getattr(center, neighbour)
                    field_value = utilities.build_table(current_neighbour, "description")

                    if field_value == f"":
                        field_value = f"> empty"
                    embed.add_field(name=f'**{current_neighbour.name}**', value=field_value, inline=True)
                embed.add_field(name='\u200b', value='\u200b', inline=False)

            response = embed
            await ctx.send(embed=response)

    @bot.command(name='Create')
    @commands.check(is_admin)
    async def create(ctx, entity_type, name):
        entity_type = entity_type.title()
        entity = entities[entity_type]
        new = utilities.create(entity, name)
        response = new.msg
        await ctx.send(response)

    @bot.command(name='Amend')
    @commands.check(is_admin)
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
    @commands.check(is_admin)
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
