import discord
from discord.ext import commands

import characters
import maps
import settlements
import time
import users
import utilities
import asyncio
import persistance


from config import DISCORD_TOKEN, COMMAND_PREFIX, ADMIN_ROLE_ID, PLAYER_ROLE_ID, EMBED_COLOR

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

arrow_emojis = {u"\u2199": 'sw',
                 u"\u2B05": 'w',
                 u"\u2196": 'nw',
                 u"\u2B06": 'n',
                 u"\u2197": 'ne',
                 u"\u27A1": 'e',
                 u"\u2198": 'se',
                 u"\u2B07": 's'
                }


# NEIGHBOURS = (("nw", "n", "ne"), ("w", "c", "e"), ("sw", "s", "se"))

def build_options_embed(emojis, title=" ", color=EMBED_COLOR):
    embed = discord.Embed(title=title, color=color)
    for key, value in emojis.items():
        name = f"{key}: {value} \n"
        field_value = "-"
        embed.add_field(name=name, value=field_value, inline=False)
    return embed

def build_options_content(emojis):
    content = ""
    for key, value in emojis.items():
        line = f"{key}: {value} \n"
        content += line
    return content



def build_map_embed(center, detailed=False):
    center.update_neighbours()
    embed = discord.Embed(title=f"__**Map of Surrounding Area: {center.name} - {center.coordinates}:**__",
                          color=0x03f8fc
                          )

    if detailed:
        NEIGHBOURS = (("c"))
        #timestamp = ctx.message.created_at
    else:
        NEIGHBOURS = (("nw", "n", "ne"), ("w", "c", "e"), ("sw", "s", "se"))
        for line in NEIGHBOURS:
            for neighbour in line:
                current_neighbour = getattr(center, neighbour)
                field_value = utilities.build_table(current_neighbour, "description")

                if field_value == f"":
                    field_value = f"> empty"
                embed.add_field(name=f'**{current_neighbour.name}**', value=field_value, inline=True)
            embed.add_field(name='\u200b', value='\u200b', inline=False)
    return embed


def get_user(uid):
    return utilities.find(users.User.directory, "uid", uid)


def discord_integration():
    async def get_input(channel, raised_by, content="Beep,boop,buzzzt...ERROR", delay=0, timeout=30):
        message = await channel.send(content=content)
        try:
            user_input = await bot.wait_for('message', check=check_is_author(channel, raised_by), timeout=timeout)
            stripped_user_input = user_input.content.title().strip()
            await user_input.delete()
            await message.delete(delay=delay)
            return stripped_user_input
        except asyncio.TimeoutError:
            await message.delete()
            await destruct_message(channel, content="Selection Timed Out.")
           # raise TimeoutError

    async def get_reaction_input(channel, raised_by, content, emojis, timeout=10, key=True, **embed):
        if key == True:
            content += build_options_content(emojis)

        print(embed)
        if embed:
            message = await channel.send(content=content, embed=embed['embed'])
            pass
        else:
            message = await channel.send(content=content)

        for emoji in emojis:
            await message.add_reaction(emoji)

        try:
            reaction = await bot.wait_for('reaction_add', check=check_reaction(message, raised_by), timeout=timeout)
            selection = reaction[0].emoji
            user_input = emojis[selection]
            await message.delete()
            return user_input
        except asyncio.TimeoutError:
            await message.delete()
            await destruct_message(channel, content="Selection Timed Out.")
            return None

    async def destruct_message(channel, content, delay=30):
        message = await channel.send(content=content)
        await message.delete(delay=delay)
        return None

    async def get_confirmation(channel, raised_by, content):
        confirm_emojis = {u"\U0001f44d": True,
                        u"\U0001f44e": False}
        return await get_reaction_input(channel, raised_by, content, confirm_emojis)





    async def update_name(ctx, user):
        player_name = user.name
        character_list = user.characters
        selected_character = user.selected_character.name
        nickname = f"{player_name} ({selected_character})"
        print(nickname)
        print(len(nickname))
        await ctx.author.edit(nick=nickname)


    def check_membership(ctx, role_id):
        print(role_id in ctx.author.roles)
        for role in ctx.author.roles:
            match = role_id == role.id
            if match:
                return match

    # def check_is_author(m, x):
    #     print(m)
    #     print(x)
    #     return True

    def check_is_author(channel, author):
        def inner_check(message):
            print(f"message in check:\n{message}\n")
            if (message.author != author) or (message.channel != channel):
                return False
            else:
                print(author)
                print(message.author)
                print(channel)
                print(message.channel)
                return True
        return inner_check

    def check_reaction(message, raised_by):
        def inner_check(reaction, reactor):
            print(f"reaction:\n{reaction}\n")
            print(f"reactor:\n{reactor}\n")

            print(f"raised_by {raised_by} == {reactor}")
            print(f"reaction {reaction}")
            print(f"message {message} == {reaction.message}")
            if (reaction.message != message) or (reactor != raised_by) or (not reaction.me):
                return False
            else:
                return True
        return inner_check

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

    @bot.command(name='menu')
    @commands.check(is_player)
    async def menu(ctx):
        raised_by = ctx.author
        channel = ctx.channel
        user = get_user(ctx.author.id)

        content = f"Hello {user.selected_character.name}.  Please select from the options below:\n"
        menu_emojis = {u"\U0001f939\U0001f3ff": 'Characters',
                         u"\U0001f5fa\uFE0F": 'View Map',
                         u"\U0001fab5": 'Session Log',
                         u"\U0001f477\U0001f3fd": 'Tasks',
                         u"\u274C": 'Cancel',
                         }

        menu_selection = await get_reaction_input(channel, raised_by, content, menu_emojis)
        print(f"menu_selection is {menu_selection}")
        if menu_selection == 'Characters':
            print('Change Character')
            await character_menu(ctx)
        elif menu_selection == 'View Map':
            await map_menu(ctx)
            # viewing_fragment = user.viewing_fragment
            # print(user)
            # print(user.viewing_fragment)
            # await embed_map(ctx)
        elif menu_selection == 'Session Log':
            print('Session Log')
        elif menu_selection == 'Tasks':
            print('Tasks')
        else:
            print("CANCEL")


    @bot.command(name="character")
    @commands.check(is_player)
    async def character_menu(ctx):
        raised_by = ctx.author
        channel = ctx.channel
        user = get_user(ctx.author.id)
        num_characters = len(user.characters)

        content = f"You are now playing as {user.selected_character.name}\n"
        if num_characters <= 1:
            pass
        else:
            character_list = ""
            for i in user.characters[1:]:
                character_list += f"{i.name}, "
            content += f"Your other characters are {character_list}\n"

        if num_characters >= user.character_slots:
            content += f"You have used all of your character slots ({user.character_slots})\n"
        else:
            content += f"You are currently only using {num_characters}/{user.character_slots} character slots\n"

        change_character_emojis = {u"\U0001f504": 'Swap',
                                   u"\U0001f195": 'New',
                                   u"\u2620\uFE0F": 'Retire',
                                   u"\u274C": 'Return to Menu',
                                   }
        change_character_selection = await get_reaction_input(channel, raised_by, content, change_character_emojis)

        if change_character_selection == 'Swap':
            await swap_character(ctx)
            print('Change Character')
        elif change_character_selection == 'New':
            print('New')
            await new_character(ctx)
        elif change_character_selection == 'Retire':
            print('Retire')
            await retire_character(ctx)
        elif change_character_selection == 'Return to Menu':
            print('Return to Menu')
            await menu(ctx)
        else:
            print("CANCEL")
            await menu(ctx)
            pass

    async def swap_character(ctx):
        channel = ctx.channel
        user = get_user(ctx.author.id)

        previously_selected = user.characters.pop(0)
        user.characters.append(previously_selected)
        user.selected_character = user.characters[0]
        await update_name(ctx, user)

        content = f"That's enough {previously_selected.name}!\n" \
                  f"{user.selected_character.name} I choose you!"
        await destruct_message(channel, content)
        await character_menu(ctx)


    async def new_character(ctx):
        raised_by = ctx.author
        channel = ctx.channel
        user = get_user(ctx.author.id)
        num_characters = len(user.characters)

        if num_characters >= user.character_slots:
            content = f"Unable to create a new character because:\n" \
                      f"You have used all of your character slots ({user.character_slots})\n"
            await destruct_message(channel, content)
            await character_menu(ctx)
        else:
            name = await get_input(channel, raised_by, "Please provide your new character's name:")
            existing = utilities.find(characters.Character.directory, "name", name)
            if len(name) >= 15:
                await destruct_message(channel, "That name is too long")
                await character_menu(ctx)
            elif existing is None:
                new = utilities.create(characters.Character, name)
                user.characters.append(new)
                await destruct_message(channel, new.msg)
                await character_menu(ctx)
            else:
                content = f"It looks like the name {name} is already in use."
                await destruct_message(channel, content)
                await character_menu(ctx)

    async def retire_character(ctx):
        raised_by = ctx.author
        channel = ctx.channel
        user = get_user(ctx.author.id)

        content = f"Are you sure you want to retire {user.selected_character.name}?\n" \
                  f"This can't be undone.\n"

        retire_character_emojis = {u"\u274E": 'Return to Menu',
                                   u"\U0001f6b7": 'Return to Menu',
                                   u"\U0001f44e\U0001f3fe": 'Return to Menu',
                                   u"\u2620\uFE0F": 'Retire',
                                   u"\u26D4": 'Return to Menu',
                                   u"\U0001f645": 'Return to Menu',
                                   u"\u274C": 'Return to Menu',
                                   }
        confirmation = await get_reaction_input(channel, raised_by, content, retire_character_emojis)
        if confirmation == 'Retire':
            retired_character = user.selected_character
            user.characters.remove(retired_character)
            content = f"{retired_character.name} has been removed from your character list.\n" \
                      f"They will be retired once you swap to a new character."
            await destruct_message(channel, content)

        await character_menu(ctx)

    @bot.command(name='map')
    @commands.check(is_player)
    async def map_menu(ctx):
        raised_by = ctx.author
        channel = ctx.channel
        user = get_user(ctx.author.id)

        content = f"Hello {user.selected_character.name}.  Please select from the options below:\n"
        map_menu_emojis = {u"\U0001f5fa\uFE0F": 'Summary View',
                           u"\U0001F4F1": 'Detailed / Mobile View',
                           u"\u274C": 'Return To Menu',
                       }

        map_menu_selection = await get_reaction_input(channel, raised_by, content, map_menu_emojis)

        if map_menu_selection == 'Summary View':
            await summary_map(ctx)
            print('Summary View')
        elif map_menu_selection == 'Detailed / Mobile View':
            await detailed_map(ctx)
            print('Detailed / Mobile View')
        elif map_menu_selection == 'Return to Menu':
            print('Return to Menu')
            await menu(ctx)
        else:
            print("CANCEL")
            await menu(ctx)
            pass

    async def summary_map(ctx):
        raised_by = ctx.author
        channel = ctx.channel
        user = get_user(ctx.author.id)
        center_coordinates = user.viewing_fragment.coordinates
        center = maps.find_fragment(center_coordinates)

        center.update_neighbours()

        content = "-"
        embed = build_map_embed(center)

        summary_map_emojis = {}
        summary_map_emojis.update(arrow_emojis)
        summary_map_emojis.update({u"\U0001F4F1": 'Detailed / Mobile View',
                                    u"\u274C": 'Return To Menu'})

        summary_map_selection = await get_reaction_input(channel, raised_by, content, summary_map_emojis,
                                                         key=False, embed=embed)

        for i in arrow_emojis:
            if summary_map_selection == arrow_emojis[i]:
                user.viewing_fragment = getattr(user.viewing_fragment, summary_map_selection)
                await refresh_map(ctx)

        if summary_map_selection == 'Detailed / Mobile View':
            await detailed_map(ctx)
            print('Detailed / Mobile View')
        elif summary_map_selection == 'Return to Menu':
            print('Return to Menu')
            await map_menu(ctx)
        else:
            print("CANCEL")
            await map_menu(ctx)


    async def detailed_map(ctx):
        raised_by = ctx.author
        channel = ctx.channel
        user = get_user(ctx.author.id)
        center_coordinates = user.viewing_fragment.coordinates
        center = maps.find_fragment(center_coordinates)

        center.update_neighbours()

        content = "-"
        embed = build_map_embed(center, detailed=True)

        detailed_map_emojis = {}
        detailed_map_emojis.update(arrow_emojis)
        detailed_map_emojis.update({u"\U0001f5fa\uFE0F": 'Summary View',
                                    u"\U0001F4DD":'Edit Map',
                                   u"\u274C": 'Return To Menu'})

        detailed_map_selection = await get_reaction_input(channel, raised_by, content, detailed_map_emojis,
                                                         key=False, embed=embed)

        for i in arrow_emojis:
            if detailed_map_selection == arrow_emojis[i]:
                user.viewing_fragment = getattr(user.viewing_fragment, detailed_map_selection)
                await refresh_map(ctx, detailed=True)

        if detailed_map_selection == 'Summary View':
            await summary_map(ctx)
            print('Summary View')
        elif detailed_map_selection == 'Edit Map':
            print('Edit Map')
            await edit_map(ctx)
        elif detailed_map_selection == 'Return to Menu':
            print('Return to Menu')
            await map_menu(ctx)
        else:
            print("CANCEL")
            await map_menu(ctx)

    async def edit_map(ctx):
        raised_by = ctx.author
        channel = ctx.channel
        user = get_user(ctx.author.id)

        content = "Do you want to edit the name of this area?\n"
        confirmation = await get_confirmation(channel, raised_by, content)
        if confirmation:
            pass

        content = "Do you want to add a log entry for this area?\n"
        confirmation = await get_confirmation(channel, raised_by, content)
        if confirmation:
            pass

        await detailed_map(ctx)



    async def refresh_map(ctx, detailed=False):
        user = get_user(ctx.author.id)
        user.viewing_fragment.update_neighbours()
        if detailed:
            await detailed_map(ctx)
        else:
            await summary_map(ctx)


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

    @bot.command(name='OldMap')
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
            for i in arrow_emojis:
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
            await reaction.remove(discord_user)


    # @bot.event
    # async def on_reaction_add(reaction, discord_user):
    #     if discord_user.bot:
    #         return
    #
    #     if reaction.me:
    #         emoji = reaction.emoji
    #         message = reaction.message
    #         print(emoji)
    #         print(message)
    #         print(message.channel.id)
    #         user = get_user(discord_user.id)
    #         # channel_id = message.channel.id
    #         # channel = bot.get_channel(channel_id)
    #         # channel = bot.get_channel(801913604374790245)
    #         channel = message.channel
    #         print(channel)
    #         print(message.channel)
    #         message_id = message.id
    #         message = await channel.fetch_message(message_id)
    #         await reaction.remove(discord_user)
    #
    #
    #         for i in arrow_emojis:
    #             if emoji == i:
    #                 user.viewing_fragment = getattr(user.viewing_fragment, arrow_emojis[i])
    #                 embed = build_map_embed(user.viewing_fragment, user.mobile)
    #                 await message.edit(embed=embed)
    #                 return
    #         if emoji == u"\U0001F4DD":
    #             print("edit")
    #             await reaction.clear()
    #             fragment = user.viewing_fragment
    #             await message.edit(content="What did you find there?", embed=None)
    #             description_request = await bot.wait_for('message')
    #             proposed_log_entry = maps.Log_Entry(time.time(), user, description_request.content)
    #             print(f'{description_request}')
    #             print(proposed_log_entry.time_stamp)
    #             print(proposed_log_entry.author)
    #             print(proposed_log_entry.entry)
    #             await message.edit(content=f"Do you want to edit the description of {fragment.coordinates}?\n"
    #                                        f"{fragment.name} - Old Description was:\n"
    #                                        f"{fragment.description}\n"
    #                                        f"\n"
    #                                        f""
    #                                        f"New Timestamp - {proposed_log_entry.time_stamp}\n"
    #                                        f"New Author - {proposed_log_entry.author.uid}\n"
    #                                        f"New Description:\n"
    #                                        f" {proposed_log_entry.entry}")
    #             fragment.description_log.insert(0, proposed_log_entry)
    #
    #
    #         elif emoji == u"\U0001F4F1":
    #             user.mobile = not user.mobile
    #             embed = build_map_embed(user.viewing_fragment, user.mobile)
    #             await message.edit(embed=embed)


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
        player_name = ctx.author.display_name
        raised_by = ctx.author
        channel = ctx.channel
        # await ctx.message.delete()

        if not check_membership(ctx, PLAYER_ROLE_ID):
            # Prompt for OOC name
            content = f"Greetings {player_name}\n" \
                       f"How would you like to be addressed out of character?\n"
            player_name = await get_input(channel, raised_by, content)

            if player_name == None:
                await destruct_message(channel, "Please use !Register to start again")
                return None

            #Prompt for Character Name
            content = f"Sure, we'll call you {player_name}.\n" \
                      f"What is your character's name?"
            character_name = await get_input(channel, raised_by, content)
            print(character_name)
            print(len(character_name))
            if (len(player_name) >= 14) or (len(character_name) >= 15):
                content = f"One of your names are too long."
                await destruct_message(channel, content)
                confirmation = "No"
            elif utilities.find(characters.Character.directory, "name", character_name):
                content = f"It looks like the name {character_name} is already in use."
                await destruct_message(channel, content)
                confirmation = "No"
            else:
                #Confirm choices
                content = f"Please confirm you would like to use the following:\n" \
                          f"Your name = {player_name}\n" \
                          f"Playing as = {character_name}\n" \
                          f"Is this correct?  Please respond with Yes or No"
                confirmation = await get_input(channel, raised_by, content)

            if confirmation == "Yes":
                # Create User Object
                user = users.create_user(discord_id, player_name)
                # Create Character Object
                character = utilities.create(characters.Character, character_name)
                print(character)
                user.characters.append(character)
                user.selected_character = character
                # Rename to Player(Character)
                await update_name(ctx, user)


                # Finally add the player role
                role = discord.utils.get(ctx.guild.roles, id=PLAYER_ROLE_ID)
                await ctx.author.add_roles(role)
                await destruct_message(channel, content=f"Welcome to The Mirror.")
            if confirmation != "Yes":
                await destruct_message(channel, content="Woops, please use !Register to start again.")
        else:
            response = f"Greetings {player_name}\n" \
                       f"It looks like you are already registered.\n" \
                       f"Use !Menu to get started."
            await destruct_message(channel, response)


    @bot.command(name='MakeTea')
    @commands.check(is_player)
    async def make_tea(ctx):
        response = f"Beep Boop making the tea... for {ctx.author.name}"
        long_string = ""
        for i in range(205):
            long_string += "tea! "
        print(len(long_string))

        embed = discord.Embed(title="Test")
        embed.add_field(name="tea!", value=long_string)


        message = await ctx.send(response, embed=embed)
        await message.add_reaction(u"\U0001F375")

    @bot.command(name='Save')
    @commands.check(is_player)
    async def save(ctx):
        persistance.save_all()
        response = f"Saving."
        await ctx.send(response)

    @bot.command(name='Load')
    @commands.check(is_admin)
    async def load(ctx):
        persistance.load_all()
        response = f"Loading."
        await ctx.send(response)

    bot.run(DISCORD_TOKEN)
