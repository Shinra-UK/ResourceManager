import discord
from discord.ext import commands

import characters
import maps
import settlements
import time
import users
import utilities
from config import DISCORD_TOKEN, COMMAND_PREFIX, ADMIN_ROLE_ID, PLAYER_ROLE_ID

bot = commands.Bot(command_prefix=COMMAND_PREFIX, case_insensitive=True)

entities = {'Character': characters.Character,
            'Settlement': settlements.Settlement,
            'User': users.User,
            'Characters': characters.Character,
            'Settlements': settlements.Settlement,
            'Users': users.User,
            'All': utilities.Entity,
            'C': characters.Character,
            'S': settlements.Settlement,
            'U': users.User,
            'A': utilities.Entity
            }

arrow_emojies = {u"\u2199": 'sw',
                 u"\u2B05": 'w',
                 u"\u2196": 'nw',
                 u"\u2B06": 'n',
                 u"\u2197": 'ne',
                 u"\u27A1": 'e',
                 u"\u2198": 'se',
                 u"\u2B07": 's'
                 }


# NEIGHBOURS = (("nw", "n", "ne"), ("w", "c", "e"), ("sw", "s", "se"))

def build_map_embed(center, mobile=False):
    if mobile:
        NEIGHBOURS = (("c"))
    else:
        NEIGHBOURS = (("nw", "n", "ne"), ("w", "c", "e"), ("sw", "s", "se"))
    center.update_neighbours()

    embed = discord.Embed(title=f"__**Map of Surrounding Area: {center.name} - {center.coordinates}:**__",
                          color=0x03f8fc
                          )
    # timestamp=ctx.message.created_at)

    for line in NEIGHBOURS:
        for neighbour in line:
            current_neighbour = getattr(center, neighbour)
            field_value = utilities.build_table(current_neighbour, "description")

            if field_value == f"":
                field_value = f"> empty"
            embed.add_field(name=f'**{current_neighbour.name}**', value=field_value, inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=False)

    return embed
    # message = await ctx.send(embed=response)
    #
    # reactions = [u"\u2B05", u"\u2B06", u"\u2B07", u"\u27A1", u"\U0001F4DD"]
    # for reaction in reactions:
    #     await message.add_reaction(reaction)


def get_user(uid):
    return utilities.find(users.User.directory, "uid", uid)


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

    @bot.command(name='Map')
    @commands.check(is_admin)
    async def embed_map(ctx, *center_coordinates):
        user = get_user(ctx.author.id)
        if center_coordinates == ():
            try:
                center_coordinates = user.viewing_fragment.coordinates
            except:
                center_coordinates = (0, 0, 0)
        elif isinstance(center_coordinates[0], str):
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
            while len(conversion) < 3:
                conversion.append(0)
            center_coordinates = tuple(int(i) for i in conversion)

        if isinstance(center_coordinates, tuple):
            center = maps.find_fragment(center_coordinates)
            print(center.coordinates)

            center.update_neighbours()
            if user:
                user.viewing_fragment = center
            embed = build_map_embed(center)

            # embed = discord.Embed(title=f"__**Map of Surrounding Area: {center.name} - {center.coordinates}:**__",
            #                       color=0x03f8fc,
            #                       timestamp=ctx.message.created_at)
            #
            # for line in NEIGHBOURS:
            #     for neighbour in line:
            #         current_neighbour = getattr(center, neighbour)
            #         field_value = utilities.build_table(current_neighbour, "description")
            #
            #         if field_value == f"":
            #             field_value = f"> empty"
            #         embed.add_field(name=f'**{current_neighbour.name}**', value=field_value, inline=True)
            #     embed.add_field(name='\u200b', value='\u200b', inline=False)
            #
            # response = embed
            response = embed
            message = await ctx.send(embed=response)

            reactions = []
            for i in arrow_emojies:
                reactions.append(i)

            reactions.append(u"\U0001F4DD")
            reactions.append(u"\U0001F4F1")
            for reaction in reactions:
                await message.add_reaction(reaction)

    @bot.event
    async def on_reaction_add(reaction, discord_user):
        if discord_user.bot:
            return

        if reaction.me:
            emoji = reaction.emoji
            message = reaction.message
            user = get_user(discord_user.id)
            channel_id = message.channel
            # channel = bot.get_channel(channel_id)
            channel = bot.get_channel(787017194965041172)
            message_id = message.id
            message = await channel.fetch_message(message_id)
            await reaction.remove(discord_user)
            #
            #             if emoji == u"\u2B05":
            #                 print("left")
            #                 print(F'Left - user: {user}')
            # #target_center = center.nw
            # # center_coordinates = (0,0,0)
            # # center = maps.find_fragment(center_coordinates)
            # # embed = build_map_embed(center)
            # #center = maps.find_fragment()
            #                 user.viewing_fragment = user.viewing_fragment.w
            #                 embed = build_map_embed(user.viewing_fragment)
            #                 await message.edit(embed=embed)
            #             elif emoji == u"\u2B06":
            #                 print("up")
            #                 user.viewing_fragment = user.viewing_fragment.n
            #                 embed = build_map_embed(user.viewing_fragment)
            #                 await message.edit(embed=embed)
            #             elif emoji == u"\u2B07":
            #                 user.viewing_fragment = user.viewing_fragment.s
            #                 embed = build_map_embed(user.viewing_fragment)
            #                 await message.edit(embed=embed)
            #             elif emoji == u"\u27A1":
            #                 user.viewing_fragment = user.viewing_fragment.e
            #                 embed = build_map_embed(user.viewing_fragment)
            #                 await message.edit(embed=embed)
            #             elif emoji == u"\U0001F4DD":
            #                 print("edit")
            #                 await message.edit(embed="edit")

            for i in arrow_emojies:
                if emoji == i:
                    user.viewing_fragment = getattr(user.viewing_fragment, arrow_emojies[i])
                    embed = build_map_embed(user.viewing_fragment, user.mobile)
                    await message.edit(embed=embed)
                    return
            if emoji == u"\U0001F4DD":
                print("edit")
                fragment = user.viewing_fragment
                await message.edit(content="What did you find there?")
                description_request = await bot.wait_for('message')
                proposed_log_entry = maps.Log_Entry(time.time(), user, description_request.content)
                print(f'{description_request}')
                print(proposed_log_entry.entry)
                #reply with edit confirmation

            elif emoji == u"\U0001F4F1":
                user.mobile = not user.mobile
                embed = build_map_embed(user.viewing_fragment, user.mobile)
                await message.edit(embed=embed)
            # print(message)
            # print(type(message))
            # print(dir(message))
            # print(dir(reaction))
            # print(dir(emoji))
            # # print(message.id)

        #
        # print(dir(emoji))
        # print(dir(reaction.me))
        # print(dir(reaction.message))
        # print(reaction.me)
        # print(reaction.message)
        # print(dir(user))

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

    @bot.command(name='Register')
    async def register(ctx):
        discord_id = ctx.author.id
        print(f'Registering {discord_id}')
        user = users.create_user(discord_id)
        if not check_membership(ctx, PLAYER_ROLE_ID):
            role = discord.utils.get(ctx.guild.roles, id=PLAYER_ROLE_ID)
            print(role)
            await ctx.author.add_roles(role)
        response = user.msg
        await ctx.send(response)

    @bot.command(name='MakeTea')
    @commands.check(is_player)
    async def make_tea(ctx):
        await register(ctx)
        response = f"Beep Boop making the tea... for {ctx.author.name}"
        message = await ctx.send(response)
        await message.add_reaction(u"\U0001F375")

    bot.run(DISCORD_TOKEN)
