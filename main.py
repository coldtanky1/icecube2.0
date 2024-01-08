import sqlite3
import asyncio
import discord
from discord.ext import commands
from discord.utils import get

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents, case_insensitive=True)

new_line = '\n'
bot.remove_command('help')
debug = False
# MUST READ NOTES:
# nation_score, gdp and population have no logic behind them, meaning it's worthless for now
# there is no way to recruit troops
# there are no weapons
# you can't make planes
# you can't make tanks
# you can't make barracks
# you can't make AA
# you can't make artillery
# you can't view info about infra
# good luck making most of that stuff rev (hehe)


# Basic Error Handler - Just add a new elif if you want to add another error to the list
# If you get the "Unspecified error" error, and you want to check what the issue is through the terminal, either remove
@bot.event
async def on_command_error(ctx, error):
    global debug
    if debug is False:   # Checks if bot is in debug mode
        if hasattr(ctx.command, 'on_error'):
            return
        error = getattr(error, 'original', error)
        if isinstance(error, commands.CommandNotFound, ):
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description="Command not found.")
            embed.set_footer(text="Check the help command")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description="An unspecified error has occurred.")
            embed.set_footer(text="Ping a dev so they can look into it")
            await ctx.send(embed=embed)
    else:
        print(error)


def dev_check(usid):
    return usid == 837257162223910912 or usid == 669517694751604738


# Connect to the sqlite DB (it will create a new DB if it doesn't exit)

conn = sqlite3.connect('player_info.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_info(
        user_id INTEGER PRIMARY KEY,
        nation_name TEXT
        )
    ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_stats(
        name TEXT PRIMARY KEY,
        nation_score INTEGER,
        gdp INTEGER,
        population INTEGER
        )
    ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_mil(
        name_nation TEXT PRIMARY KEY,
        troops INTEGER,
        planes INTEGER,
        weapon INTEGER,
        tanks INTEGER,
        artillery INTEGER,
        anti_air INTEGER,
        barracks INTEGER
        )
    ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS infra(
        name TEXT PRIMARY KEY,
        basic_house INTEGER,
        small_flat INTEGER,
        apt_complex INTEGER,
        skyscraper INTEGER,
        lumber_mill INTEGER,
        coal_mine INTEGER,
        iron_mine INTEGER,
        lead_mine INTEGER,
        bauxite_mine INTEGER,
        oil_derrick INTEGER,
        uranium_mine INTEGER,
        farm INTEGER,
        aluminium_factory INTEGER,
        steel_factory INTEGER,
        oil_refinery INTEGER,
        ammo_factory INTEGER,
        concrete_factory INTEGER
        )
    ''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS resources(
        name TEXT PRIMARY KEY,
        wood INTEGER,
        coal INTEGER,
        iron INTEGER,
        lead INTEGER,
        bauxite INTEGER,
        oil INTEGER,
        uranium INTEGER,
        food INTEGER,
        steel INTEGER,
        aluminium INTEGER,
        gasoline INTEGER,
        ammo INTEGER,
        concrete INTEGER
        )
    ''')


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


@bot.command()
async def ping(ctx):
    lat = int(bot.latency * 1000)
    await ctx.send(f'Pong! {lat}ms')


@bot.command()   # Debug mode status
async def debug_status(ctx):
    if dev_check(ctx.author.id):
        global debug
        await ctx.send(f'Debug Status: {debug}')
    else:
        print(f'{ctx.author} attempted to enable debug')
        await ctx.send(f'Permission denied: You are not a developer.')


@bot.command()   # Debug mode switcher
async def debug_mode(ctx):
    if dev_check(ctx.author.id):
        global debug
        if debug:
            debug = False
            await ctx.send(f'Debug mode: OFF')
            print("Debug disabled")
        else:
            debug = True
            await ctx.send(f'Debug mode: ON')
            print("Debug enabled")
    else:
        print(f'{ctx.author} attempted to enable debug')
        await ctx.send(f'Permission denied: You are not a developer.')


# Private Channel Command
@bot.command()
async def private(ctx):
    ch_name = ctx.author.name

    def kat_chan_id(context, ch_name):  # Finds and gets id of channel
        for channel in context.guild.channels:
            if channel.name == ch_name:
                return channel.id

    if any(ch_name in channel.name for channel in ctx.guild.channels):  # Checks if channel already exists
        chid = kat_chan_id(ctx, ch_name)
        embed = discord.Embed(colour=0x8212DF, title="Instance Already Running", type='rich',
                              description=f'Cannot start another instance because an instance for you already exists in <#{str(chid)}>')
        await ctx.send(embed=embed)
    else:  # Creates Private Channel
        topic = ch_name + '\'s Project Thaw private channel'
        category = bot.get_channel()  # Private channel category DON'T FORGET TO INSERT THE ID OF THE CATEGORY YOU WANT THE PRIVATE CHANNELS TO BE IN
        overwrites = {
            discord.utils.get(ctx.guild.roles, name="Overseer"): discord.PermissionOverwrite(read_messages=True),
            # Overseer / Game Master Role
            ctx.message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True)
        }
        await ctx.guild.create_text_channel(name=ch_name, category=category, overwrites=overwrites, topic=topic)
        asyncio.sleep(10)
        channel = get(ctx.guild.channels, name=ch_name)  # Gets channel
        print(f"Channel: {channel}")
        if channel:
            print(f"Channel Name: {channel.name}")
            print(f"Channel ID: {channel.id}")
            msg = await channel.send(f'<@{ctx.author.id}>')
            await msg.delete()
        else:
            print("Error: Channel is None")
        await msg.delete()
        await asyncio.sleep(3600)  # Time before channel gets deleted
        await channel.delete()


@bot.command()
async def create(ctx):
    user_id = ctx.author.id

    # Check if the user already has an account
    cursor.execute('SELECT 1 FROM user_info WHERE user_id = ?', (user_id,))
    existing_record = cursor.fetchone()

    if existing_record:
        embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                              description=f'You already created a nation.')
        embed.set_footer(text="Dementia")
        await ctx.send(embed=embed)
        return

    embed = discord.Embed(colour=0xFFF86E, title="Creating Nation", type='rich',
                          description="What is the name of your nation?"
                                      "Name cannot be longer than 25 characters.")
    emb = await ctx.send(embed=embed)

    # Checks if response is made by the same user and in the same channel
    def msgchk(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        nt_name = await bot.wait_for('message', check=msgchk, timeout=30.0)
    except asyncio.TimeoutError:
        return await ctx.send("You took too long to respond.")
    nat_name = nt_name.content

    if len(nat_name) > 25:
        embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                              description=f'Your nation name cannot be longer than 25 characters.')
        await emb.edit(embed=embed)
        return

    embed = discord.Embed(
        title='Nation Successfully Created',
        description=f'This is the glorious start of the **{nat_name}**! '
                    f'{new_line}We wish you a successful journey in leading your people to greatness.',
        color=0x5BF9A0
    )
    await emb.edit(embed=embed)

    # insert data into the table
    cursor.execute('INSERT INTO user_info (user_id, nation_name) VALUES (?, ?)', (user_id, nat_name))
    conn.commit()

    print(f"Successfully added {user_id}({nat_name})")

    # add base stats to the user
    cursor.execute('INSERT INTO user_stats (name, nation_score, gdp, population) VALUES (?, ?, ?, ?)',
                   (nat_name, 0, 0, 100000))
    conn.commit()

    # add base mil stats to the user
    cursor.execute(
        'INSERT INTO user_mil (name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (nat_name, 0, 0, 0, 0, 0, 0, 0))
    conn.commit()

    # Add base resources to the user
    cursor.execute(
        'INSERT INTO resources (name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (nat_name, 500, 300, 50, 50, 0, 50, 0, 10000, 50, 50, 100, 1000, 0))
    conn.commit()

    print(f"Successfully added stats to {user_id}({nat_name})")

    # Add base infra stats to the user
    cursor.execute(
        'INSERT INTO infra (name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
        (nat_name, 12500, 1000, 834, 0, 10, 100, 10, 10, 10, 10, 0, 2500, 0, 0, 0, 0,
         0))  # the values came from ice cube's game sheet so just use that as a reference
    conn.commit()

    print(f"Successfully added infra to {user_id}({nat_name})")


@bot.command()
async def rename(ctx, new_name: str):
    if new_name == "":
        embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                              description=f'You forgot to write the new name.{new_line}{new_line}'
                                          f'Command Format: `$rename [new_name]`')
        await ctx.send(embed=embed)

    user_id = ctx.author.id

    if len(new_name) > 25:
        embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                              description=f'Your nation name cannot be longer than 25 characters.')
        await ctx.send(embed=embed)
        return

    cursor.execute('SELECT nation_name FROM user_info WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    nation_name = result[0]

    cursor.execute('SELECT 1 FROM user_info WHERE user_id = ?', (user_id,))
    existing_record = cursor.fetchone()

    if existing_record:
        # updates the user_info table
        cursor.execute('UPDATE user_info SET nation_name = ? WHERE user_id = ?', (new_name, user_id))
        conn.commit()
        # updates the user_stats table
        cursor.execute('UPDATE user_stats SET name = ? WHERE name = ?', (new_name, nation_name))
        conn.commit()
        # updates the user_mil table
        cursor.execute('UPDATE user_mil SET name_nation = ? WHERE name_nation = ?', (new_name, nation_name))
        conn.commit()
        # updates the infra table
        cursor.execute('UPDATE infra SET name = ? WHERE name = ?', (new_name, nation_name))
        conn.commit()
        # updates the resources table
        cursor.execute('UPDATE resources SET name = ? WHERE name = ?', (new_name, nation_name))
        conn.commit()

        embed = discord.Embed(
            title='Nation Rename',
            description=f'You have successfully changed your nation\'s name to **{new_name}**!',
            color=0x5BF9A0
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                              description=f'You do not have a nation.{new_line}'
                                          f'To create one, type `$create`.')
        await ctx.send(embed=embed)


@bot.command()
async def stats(ctx):
    user_id = ctx.author.id

    # fetch user nation_name
    cursor.execute('SELECT nation_name FROM user_info WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        nation_name = result[0]

        # fetch user stats
        cursor.execute('SELECT name, nation_score, gdp, population FROM user_stats WHERE name = ?', (nation_name,))
        stats_result = cursor.fetchone()

        if stats_result:
            name, nation_score, gdp, population = stats_result

            embed = discord.Embed(
                title=f"📊 {name}'s Stats",
                description=f'Name: {name}',
                color=0x04a5e5
            )
            embed.add_field(name='🫅 Ruler', value=f"<@{user_id}>", inline=False)
            embed.add_field(name='', value='', inline=False)
            embed.add_field(name='🏆 Nation Score', value=f'{nation_score:,}', inline=False)
            embed.add_field(name='', value='', inline=False)
            embed.add_field(name='📈 Gross Domestic Product', value=f'{gdp:,}', inline=False)
            embed.add_field(name='', value='', inline=False)
            embed.add_field(name='👪 Population', value=f'{population:,}', inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Cannot find stats.')
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                              description=f'You do not have a nation.{new_line}'
                                          f'To create one, type `$create`.')
        await ctx.send(embed=embed)


@bot.command()
async def mstats(ctx):
    user_id = ctx.author.id

    # fetch user nation_name
    cursor.execute('SELECT nation_name FROM user_info WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        nation_name = result[0]

        # fetch user's mil stats
        cursor.execute(
            'SELECT name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks FROM user_mil WHERE name_nation = ?',
            (nation_name,))
        mil_result = cursor.fetchone()

        if mil_result:
            name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks = mil_result

            embed = discord.Embed(
                title=f"⚔ {name_nation}'s Military Stats",
                description='',
                color=0xe64553
            )
            embed.add_field(name='🪖 Troops', value=f'{troops:,}', inline=False)
            embed.add_field(name='', value='', inline=False)
            embed.add_field(name='⛟ Tanks', value=f'{tanks:,}', inline=False)
            embed.add_field(name='', value='', inline=False)
            embed.add_field(name='💥 Artillery', value=f'{artillery:,}', inline=False)
            embed.add_field(name='', value='', inline=False)
            embed.add_field(name='💥 Anti-Air', value=f'{anti_air:,}', inline=False)
            embed.add_field(name='', value='', inline=False)
            embed.add_field(name='🛫 Planes', value=f'{planes:,}', inline=False)
            embed.add_field(name='', value='', inline=False)
            embed.add_field(name='🎖 Barracks', value=f'{barracks:,}', inline=False)
            embed.add_field(name='', value='', inline=False)
            embed.add_field(name='🔫 Weapon', value=f'{weapon}', inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Cannot find stats.')
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                              description=f'You do not have a nation.{new_line}'
                                          f'To create one, type `$create`.')
        await ctx.send(embed=embed)


@bot.command()
async def infra(ctx):
    user_id = ctx.author.id

    # fetch user nation_name
    cursor.execute('SELECT nation_name FROM user_info WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        nation_name = result[0]

        # fetch user's infra
        cursor.execute(
            'SELECT name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory FROM infra WHERE name = ?',
            (nation_name,))
        infra_result = cursor.fetchone()

        if infra_result:
            name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory = infra_result

            fields = [
                ("Housing", f"Displays {name}'s housing infra."),
                ("", ""),
                ("Basic House", str(basic_house)),
                ("", ""),
                ("Small Flat", str(small_flat)),
                ("", ""),
                ("Apartment Complex", str(apt_complex)),
                ("", ""),
                ("Skyscraper", str(skyscraper)),
                ("", ""),
                ("Production", f"Displays {name}'s production infra."),
                ("", ""),
                ("Lumber Mill", str(lumber_mill)),
                ("", ""),
                ("Coal Mine", str(coal_mine)),
                ("", ""),
                ("Iron Mine", str(iron_mine)),
                ("", ""),
                ("Lead Mine", str(lead_mine)),
                ("", ""),
                ("Bauxite Mine", str(bauxite_mine)),
                ("", ""),
                ("Oil Derrick", str(oil_derrick)),
                ("", ""),
                ("Uranium Mine", str(uranium_mine)),
                ("", ""),
                ("Farm", str(farm)),
                ("", ""),
                ("Aluminium Factory", str(aluminium_factory)),
                ("", ""),
                ("Steel Factory", str(steel_factory)),
                ("", ""),
                ("Oil Refinery", str(oil_refinery)),
                ("", ""),
                ("Munitions Factory", str(ammo_factory)),
                ("", ""),
                ("Concrete Factory", str(concrete_factory)),
            ]

            # paginate (if that's a word) the fields
            pages = []
            current_page = 0
            fields_per_page = 10

            while current_page < len(fields):
                embed = discord.Embed(title=f"{name}'s Infrastructure", color=0x8839ef)

                for field_name, field_value in fields[current_page:current_page + fields_per_page]:
                    embed.add_field(name=field_name, value=field_value, inline=False)

                pages.append(embed)
                current_page += fields_per_page

            # Send the first page and add reactions for navigation
            message = await ctx.send(embed=pages[0])
            await message.add_reaction('⬅️')
            await message.add_reaction('➡️')

            def check(react, usr):
                return usr == ctx.author and str(react.emoji) in ['⬅️', '➡️']

            current_page = 0

            while True:
                try:
                    reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                except TimeoutError:
                    break

                if str(reaction.emoji) == '➡️' and current_page + 1 < len(pages):
                    current_page += 1
                elif str(reaction.emoji) == '⬅️' and current_page > 0:
                    current_page -= 1

                await message.edit(embed=pages[current_page])
                await message.remove_reaction(reaction.emoji, user)
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Cannot find stats.')
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                              description=f'You do not have a nation.{new_line}'
                                          f'To create one, type `$create`.')
        await ctx.send(embed=embed)


@bot.command()
async def res(ctx):
    user_id = ctx.author.id

    # fetch user nation_name
    cursor.execute('SELECT nation_name FROM user_info WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        nation_name = result[0]

        # fetch user's production infra
        cursor.execute(
            'SELECT name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory FROM infra WHERE name = ?',
            (nation_name,))
        infra_result = cursor.fetchone()


        if infra_result:
            name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory = infra_result

            # The production of each resource
            prod_wood = lumber_mill * 2
            prod_coal = coal_mine * 1.2
            prod_iron = iron_mine * 1
            prod_lead = lead_mine * 0.8
            prod_bauxite = bauxite_mine * 0.6
            prod_oil = oil_derrick * 1
            prod_uranium = uranium_mine * 0.05
            prod_farm = farm * 10
            prod_aluminium = aluminium_factory * 0.4
            prod_steel = steel_factory * 0.3
            prod_gas = oil_refinery * 0.2
            prod_ammo = ammo_factory * 0.5
            prod_concrete = concrete_factory * 0.6


            # The consumption of each resource
            usage_iron_wood = prod_wood * 0
            usage_lead_wood = prod_wood * 0
            usage_bauxite_wood = prod_wood * 0
            usage_iron_coal = prod_coal * 0
            usage_lead_coal = prod_coal * 0
            usage_bauxite_coal = prod_coal * 0
            usage_iron_iron = prod_iron * 0
            usage_lead_iron = prod_iron * 0
            usage_bauxite_iron = prod_iron * 0
            usage_iron_lead = prod_lead * 0
            usage_lead_lead = prod_lead * 0
            usage_bauxite_lead = prod_lead * 0
            usage_iron_bauxite = prod_bauxite * 0
            usage_lead_bauxite = prod_bauxite * 0
            usage_bauxite_bauxite = prod_bauxite * 0
            usage_iron_oil = prod_oil * 0
            usage_lead_oil = prod_oil * 0
            usage_bauxite_oil = prod_oil * 0
            usage_iron_uranium = prod_uranium * 0
            usage_lead_uranium = prod_uranium * 0
            usage_bauxite_uranium = prod_uranium * 0
            usage_iron_food = prod_farm * 0
            usage_lead_food = prod_farm * 0
            usage_bauxite_food = prod_farm * 0
            usage_iron_aluminium = prod_aluminium * 0.2
            usage_lead_aluminium = prod_aluminium * 0.1
            usage_bauxite_aluminium = prod_aluminium * 1.2
            usage_iron_steel = prod_steel * 1.4
            usage_lead_steel = prod_steel * 0.3
            usage_bauxite_steel = prod_steel * 0.3
            usage_oil_gas = prod_gas * 2
            usage_lead_gas = prod_gas * 0
            usage_bauxite_gas = prod_gas * 0
            usage_iron_ammo = prod_ammo * 0.2
            usage_lead_ammo = prod_ammo * 1.1
            usage_bauxite_ammo = prod_ammo * 0
            usage_iron_concrete = prod_concrete * 0.5
            usage_lead_concrete = prod_concrete * 0
            usage_bauxite_concrete = prod_concrete * 0

            final_usage_iron = usage_iron_wood + usage_iron_coal + usage_iron_iron + usage_iron_lead + usage_iron_bauxite + usage_iron_oil + usage_iron_uranium + usage_iron_food + usage_iron_aluminium + usage_iron_steel + usage_iron_ammo + usage_iron_concrete
            final_usage_lead = usage_lead_wood + usage_lead_coal + usage_lead_iron + usage_lead_lead + usage_lead_bauxite + usage_lead_oil + usage_lead_uranium + usage_lead_food + usage_lead_aluminium + usage_lead_steel + usage_lead_ammo + usage_lead_concrete
            final_usage_bauxite = usage_bauxite_wood + usage_bauxite_coal + usage_bauxite_iron + usage_bauxite_lead + usage_bauxite_bauxite + usage_bauxite_oil + usage_bauxite_uranium + usage_bauxite_food + usage_bauxite_aluminium + usage_bauxite_steel + usage_bauxite_ammo + usage_bauxite_concrete

            final_prod_iron = prod_iron - final_usage_iron
            final_prod_lead = prod_lead - final_usage_lead
            final_prod_bauxite = prod_bauxite - final_usage_bauxite
            final_prod_oil = prod_oil - usage_oil_gas



            embed = discord.Embed(
                title='Production',
                description=f'Display {name}\'s production.',
                color=discord.Color.red()
            )
            embed.add_field(name='⛏ Mined Resources', value='', inline=False)
            embed.add_field(name='🏭 Manufactured Resources', value='', inline=False)

            mined_resources = [
                f'Wood: {prod_wood:,}',
                f'Coal: {prod_coal:,}',
                f'Iron: {final_prod_iron:,}',
                f'Lead: {final_prod_lead:,}',
                f'Bauxite: {final_prod_bauxite:,}',
                f'Oil: {final_prod_oil:,}',
                f'Uranium: {prod_uranium:,}',
                f'Food: {prod_farm:,}',
            ]

            manufactured_resources = [
                f'Aluminium: {prod_aluminium:,}',
                f'Steel: {prod_steel:,}',
                f'Gasoline: {prod_gas:,}',
                f'Ammo: {prod_ammo:,}',
                f'Concrete: {prod_concrete:,}',
            ]

            pages = [mined_resources, manufactured_resources]
            current_page = 0

            message = await ctx.send(embed=embed)

            # Add reactions for navigation
            await message.add_reaction('◀')
            await message.add_reaction('▶')

            def check(reaction, user, current_page, max_page):
                return user == ctx.author and str(reaction.emoji) in ['◀', '▶'] and 0 <= current_page < max_page

            while True:
                try:
                    reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=lambda r, u: check(r, u, current_page, len(pages)))

                    if str(reaction.emoji) == '▶' and current_page < len(pages) - 1:
                        current_page += 1
                    elif str(reaction.emoji) == '◀' and current_page > 0:
                        current_page -= 1

                    embed.clear_fields()
                    embed.add_field(name='⛏ Mined Resources' if current_page == 0 else '🏭 Manufactured Resources', value='\n'.join(pages[current_page]), inline=False)
                    await message.edit(embed=embed)
                    await message.remove_reaction(reaction, user)

                except TimeoutError:
                    break

            # Remove reactions when the loop ends
            await message.clear_reactions()

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Cannot find stats.')
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                              description=f'You do not have a nation.{new_line}'
                                          f'To create one, type `$create`.')
        await ctx.send(embed=embed)

# Reserve Command
@bot.command()
async def reserve(ctx):
    user_id = ctx.author.id

    # fetch user nation_name
    cursor.execute('SELECT nation_name FROM user_info WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        nation_name = result[0]

        # fetch user's resources
        cursor.execute(
            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
            (nation_name,))
        resource_result = cursor.fetchone()

        if resource_result:
            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = resource_result

            embed=discord.Embed(
                title=f'{name}\'s Reserves',
                description='Displays nation\'s national reserves.',
                color=0x4CAF50)
            embed.add_field(name=f'Wood: {wood:,}', value='', inline=False)
            embed.add_field(name=f'Coal: {coal:,}', value='', inline=False)
            embed.add_field(name=f'Iron: {iron:,}', value='', inline=False)
            embed.add_field(name=f'Lead: {lead:,}', value='', inline=False)
            embed.add_field(name=f'Bauxite: {bauxite:,}', value='', inline=False)
            embed.add_field(name=f'Oil: {oil:,}', value='', inline=False)
            embed.add_field(name=f'Uranium: {uranium:,}', value='', inline=False)
            embed.add_field(name=f'Food: {food:,}', value='', inline=False)
            embed.add_field(name=f'Steel: {steel:,}', value='', inline=False)
            embed.add_field(name=f'Aluminium: {aluminium:,}', value='', inline=False)
            embed.add_field(name=f'Gasoline: {gasoline:,}', value='', inline=False)
            embed.add_field(name=f'Ammo: {ammo:,}', value='', inline=False)
            embed.add_field(name=f'Concrete: {concrete:,}', value='', inline=False)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Cannot find stats.')
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                              description=f'You do not have a nation.{new_line}'
                                          f'To create one, type `$create`.')
        await ctx.send(embed=embed)



# Construct Command
@bot.command()
async def construct(ctx, building: str, amount: int):
    user_id = ctx.author.id
    building = building.lower()

    if amount <= 0:
        await ctx.send("Invalid building amount, try a positive number.")
        return


    # fetch user nation_name
    cursor.execute('SELECT nation_name FROM user_info WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        nation_name = result[0]

        # fetch user's resources
        cursor.execute(
            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
            (nation_name,))
        res_result = cursor.fetchone()

        # fetch user's production infra
        cursor.execute(
            'SELECT name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory FROM infra WHERE name = ?',
            (nation_name,))
        infra_result = cursor.fetchone()

        if infra_result:
            name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory = infra_result


            match building: # Each building the user wants to build. You can reuse later for info command.
                case "basic_house":
                    basichouse_amt = amount
                    basichouse_wood = basichouse_amt * 2
                    basichouse_conrete = basichouse_amt * 0.6
                    embed = discord.Embed(colour=0xdd7878, title="Construct: Basic House", type='rich',
                                                            description=f'{basichouse_amt:,} will be constructed.{new_line}{new_line}'
                                                                        f'The basic houses will cost: {basichouse_wood:,} Wood{new_line}'
                                                                        f'The basic houses will cost: {basichouse_conrete:,} Concrete')
                    await ctx.send(embed=embed)

                    try:
                        await ctx.send("Would you like to proceed? Respond with y/n.")

                        def check(message):
                            return message.content.lower() in ['y', 'n'] 

                        response_message = await bot.wait_for('message', timeout=30, check=check)


                        if response_message.content.lower() == 'y':
                            constructing = discord.Embed(colour=0xdd7878, title='Construct', type='rich',
                                                                description='Constructing...')
                            construct_msg = await ctx.send(embed=constructing)


                            if res_result:
                                name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                                # Check if user has enough wood and concrete
                                if (wood > basichouse_wood) and (concrete > basichouse_conrete):

                                    # If user has enough wood and concrete then it proceeds normally.
                                    # Update the resources table
                                    cursor.execute('''
                                        UPDATE resources SET
                                        wood = wood - ?,
                                        concrete = concrete - ?
                                        WHERE name = ?
                                    ''', (basichouse_wood, basichouse_conrete, nation_name))

                                    cursor.execute('UPDATE infra SET basic_house = basic_house + ? WHERE name = ?', (basichouse_amt, nation_name))

                                    # Commit the changes to the database
                                    conn.commit()

                                    cons_done = discord.Embed(colour=0xdd7878, title='Contruct', type='rich',
                                                            description='Construction complete!')
                                    await construct_msg.edit(embed=cons_done)

                                else:
                                    cons_error = discord.Embed(colour=0xEF2F73, title='Error', type='rich',
                                                            description='You do not have enough resources.')
                                    await construct_msg.edit(embed=cons_error)
                                    return
                        else:
                            await ctx.send("Aborting.")
                            return
                    except asyncio.TimeoutError:
                        return await ctx.send("You took too long to respond.")
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Cannot find stats.')
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                              description=f'You do not have a nation.{new_line}'
                                          f'To create one, type `$create`.')
        await ctx.send(embed=embed)





# Update Command
@bot.command()
async def update(ctx):
    user_id = ctx.author.id

    # fetch user nation_name
    cursor.execute('SELECT nation_name FROM user_info WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        nation_name = result[0]

        # fetch user's production infra
        cursor.execute(
            'SELECT name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory FROM infra WHERE name = ?',
            (nation_name,))
        infra_result = cursor.fetchone()


        if infra_result:
            name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory = infra_result

            # The production of each resource
            prod_wood = lumber_mill * 2
            prod_coal = coal_mine * 1.2
            prod_iron = iron_mine * 1
            prod_lead = lead_mine * 0.8
            prod_bauxite = bauxite_mine * 0.6
            prod_oil = oil_derrick * 1
            prod_uranium = uranium_mine * 0.05
            prod_farm = farm * 10
            prod_aluminium = aluminium_factory * 0.4
            prod_steel = steel_factory * 0.3
            prod_gas = oil_refinery * 0.2
            prod_ammo = ammo_factory * 0.5
            prod_concrete = concrete_factory * 0.6


            # The consumption of each resource
            usage_iron_wood = prod_wood * 0
            usage_lead_wood = prod_wood * 0
            usage_bauxite_wood = prod_wood * 0
            usage_iron_coal = prod_coal * 0
            usage_lead_coal = prod_coal * 0
            usage_bauxite_coal = prod_coal * 0
            usage_iron_iron = prod_iron * 0
            usage_lead_iron = prod_iron * 0
            usage_bauxite_iron = prod_iron * 0
            usage_iron_lead = prod_lead * 0
            usage_lead_lead = prod_lead * 0
            usage_bauxite_lead = prod_lead * 0
            usage_iron_bauxite = prod_bauxite * 0
            usage_lead_bauxite = prod_bauxite * 0
            usage_bauxite_bauxite = prod_bauxite * 0
            usage_iron_oil = prod_oil * 0
            usage_lead_oil = prod_oil * 0
            usage_bauxite_oil = prod_oil * 0
            usage_iron_uranium = prod_uranium * 0
            usage_lead_uranium = prod_uranium * 0
            usage_bauxite_uranium = prod_uranium * 0
            usage_iron_food = prod_farm * 0
            usage_lead_food = prod_farm * 0
            usage_bauxite_food = prod_farm * 0
            usage_iron_aluminium = prod_aluminium * 0.2
            usage_lead_aluminium = prod_aluminium * 0.1
            usage_bauxite_aluminium = prod_aluminium * 1.2
            usage_iron_steel = prod_steel * 1.4
            usage_lead_steel = prod_steel * 0.3
            usage_bauxite_steel = prod_steel * 0.3
            usage_oil_gas = prod_gas * 2
            usage_lead_gas = prod_gas * 0
            usage_bauxite_gas = prod_gas * 0
            usage_iron_ammo = prod_ammo * 0.2
            usage_lead_ammo = prod_ammo * 1.1
            usage_bauxite_ammo = prod_ammo * 0
            usage_iron_concrete = prod_concrete * 0.5
            usage_lead_concrete = prod_concrete * 0
            usage_bauxite_concrete = prod_concrete * 0

            final_usage_iron = usage_iron_wood + usage_iron_coal + usage_iron_iron + usage_iron_lead + usage_iron_bauxite + usage_iron_oil + usage_iron_uranium + usage_iron_food + usage_iron_aluminium + usage_iron_steel + usage_iron_ammo + usage_iron_concrete
            final_usage_lead = usage_lead_wood + usage_lead_coal + usage_lead_iron + usage_lead_lead + usage_lead_bauxite + usage_lead_oil + usage_lead_uranium + usage_lead_food + usage_lead_aluminium + usage_lead_steel + usage_lead_ammo + usage_lead_concrete
            final_usage_bauxite = usage_bauxite_wood + usage_bauxite_coal + usage_bauxite_iron + usage_bauxite_lead + usage_bauxite_bauxite + usage_bauxite_oil + usage_bauxite_uranium + usage_bauxite_food + usage_bauxite_aluminium + usage_bauxite_steel + usage_bauxite_ammo + usage_bauxite_concrete

            final_prod_iron = prod_iron - final_usage_iron
            final_prod_lead = prod_lead - final_usage_lead
            final_prod_bauxite = prod_bauxite - final_usage_bauxite
            final_prod_oil = prod_oil - usage_oil_gas

            updating_emb = discord.Embed(
                title='Update',
                type='rich',
                description='Updating...',
                color=0x4CAF50
                )
            update_emb = await ctx.send(embed=updating_emb)


            # Update the resources table
            cursor.execute('''
                UPDATE resources SET
                wood = wood + ?,
                coal = coal + ?,
                iron = iron + ?,
                lead = lead + ?,
                bauxite = bauxite + ?,
                oil = oil + ?,
                uranium = uranium + ?,
                food = food + ?,
                aluminium = aluminium + ?,
                steel = steel + ?,
                gasoline = gasoline + ?,
                ammo = ammo + ?,
                concrete = concrete + ?
                WHERE name = ?
            ''', (prod_wood, prod_coal, final_prod_iron, final_prod_lead, final_prod_bauxite, final_prod_oil, prod_uranium,
                  prod_farm, prod_aluminium, prod_steel, prod_gas, prod_ammo, prod_concrete, nation_name))

            # Commit the changes to the database
            conn.commit()

            upd_done_emb = discord.Embed(
                title='Update',
                type='rich',
                description="Updating complete!",
                color=0x4CAF50
                )
            await update_emb.edit(embed=upd_done_emb)
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Cannot find stats.')
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                              description=f'You do not have a nation.{new_line}'
                                          f'To create one, type `$create`.')
        await ctx.send(embed=embed)



# Help Command
@bot.command()
async def help(ctx, cmd: str = ""):
    cmd = cmd.lower()

    match cmd:   # Description and syntax of each command
        case "create":
            embed = discord.Embed(colour=0xdd7878, title="Help: Create", type='rich',
                                  description=f'Syntax: `$create`{new_line}{new_line}'
                                              f'Creates a new nation if you don\'t have one already')
            await ctx.send(embed=embed)
        case "private":
            embed = discord.Embed(colour=0xdd7878, title="Help: Private", type='rich',
                                  description=f'Syntax: `$private`{new_line}{new_line}'
                                              f'Creates a private channel that will be deleted after 1 hour.')
            await ctx.send(embed=embed)
        case "infra":
            embed = discord.Embed(colour=0xdd7878, title="Help: Infra", type='rich',
                                  description=f'Syntax: `$infra`{new_line}{new_line}'
                                              f'Displays your infrastructure.')
            await ctx.send(embed=embed)
        case "mstats":
            embed = discord.Embed(colour=0xdd7878, title="Help: Mstats", type='rich',
                                  description=f'Syntax: `$mstats`{new_line}{new_line}'
                                              f'Displays your military statistics.')
            await ctx.send(embed=embed)
        case "rename":
            embed = discord.Embed(colour=0xdd7878, title="Help: Rename", type='rich',
                                  description=f'Syntax: `$rename [new name]`{new_line}{new_line}'
                                              f'Changes the name of your nation to the [new name].{new_line}'
                                              f'Mind that the name cannot be longer than 25 characters.')
            await ctx.send(embed=embed)

        case "stats":
            embed = discord.Embed(colour=0xdd7878, title="Help: Stats", type='rich',
                                  description=f'Syntax: `$stats`{new_line}{new_line}'
                                              f'Displays your nation\'s statistics.')
            await ctx.send(embed=embed)

        case "res":
            embed = discord.Embed(colour=0xdd7878, title="Help: Resource", type='rich',
                                  description=f'Syntax: `$res`{new_line}{new_line}'
                                              f'Displays your nation\'s production.')
            await ctx.send(embed=embed)

        case "reserve":
            embed = discord.Embed(colour=0xdd7878, title="Help: Reserve", type='rich',
                                  description=f'Syntax: `$reserve`{new_line}{new_line}'
                                              f'Displays your nation\'s national reserves.')
            await ctx.send(embed=embed)

        case "update":
            embed = discord.Embed(colour=0xdd7878, title="Help: Update", type='rich',
                                  description=f'Syntax: `$update`{new_line}{new_line}'
                                              f'Updates your nation\'s statistics.')
            await ctx.send(embed=embed)

        case _:   # Actual command list
            generating = discord.Embed(colour=0xdce0e8, title="Help", type='rich',
                                       description="Generating help pages...")

            gen_emb = discord.Embed(colour=0xea76cb, title="Help | General", type='rich')   # General Tab
            gen_emb.add_field(name="Statistic Visualization", value="Stats - Displays your stats.\n"
                                                                    "Mstats - Displays your military stats.\n"
                                                                    "Infra - Displays your infrastructure.\n"
                                                                    "Update - Updates your nation's statistics.",
                              inline=False)
            gen_emb.add_field(name="Other Features", value="Private - Creates a private channel.\n"
                                                           "Create - Creates a nation.",
                              inline=False)

            eco_emb = discord.Embed(colour=0xdf8e1d, title="Help | Economy", type='rich')   # Economy Tab
            eco_emb.add_field(name="Economy", value="Res - Displays your nation's production.\n"
                                                    "Reserve - Displays your nation's national reserves.",
                              inline=False)

            tec_emb = discord.Embed(colour=0x04a5e5, title="Help | Technology", type='rich')   # Technology Tab
            tec_emb.add_field(name="Category", value="Command - Description",
                              inline=False)

            cus_emb = discord.Embed(colour=0x7287fd, title="Help | Customization", type='rich')   # Customization Tab
            cus_emb.add_field(name="Name Changing", value="Rename - Changes your name to something else.",
                              inline=False)

            set_emb = discord.Embed(colour=0x7c7f93, title="Help | Settings", type='rich')   # Settings Tab
            set_emb.add_field(name="Category", value="Command - Description",
                              inline=False)

            mil_emb = discord.Embed(colour=0xe64553, title="Help | Military", type='rich')   # Military Tab
            mil_emb.add_field(name="Category", value="Command - Description",
                              inline=False)

            pol_emb = discord.Embed(colour=0x8839ef, title="Help | Politics", type='rich')   # Politics Tab
            pol_emb.add_field(name="Category", value="Command - Description",
                              inline=False)

            adm_emb = discord.Embed(colour=0x40a02b, title="Help | Administration", type='rich')   # Administration Tab
            adm_emb.add_field(name="Category", value="Command - Description",
                              inline=False)

            help_emb = await ctx.send(embed=generating)   # Prepares Embed
            await help_emb.add_reaction('📊')
            await help_emb.add_reaction('💶')
            await help_emb.add_reaction('🧪')
            await help_emb.add_reaction('🖍️')
            await help_emb.add_reaction('🔨')
            await help_emb.add_reaction('💥')
            await help_emb.add_reaction('📜')
            await help_emb.add_reaction('✒️')
            match cmd:   # Chooses first page depending on [cmd]
                case "eco" | "economy":
                    await help_emb.edit(embed=eco_emb)
                case "tec" | "tech" | "technology":
                    await help_emb.edit(embed=tec_emb)
                case "cus" | "custom" | "customization":
                    await help_emb.edit(embed=cus_emb)
                case "set" | "settings":
                    await help_emb.edit(embed=set_emb)
                case "mil" | "military":
                    await help_emb.edit(embed=mil_emb)
                case "pol" | "politics" | "politic":
                    await help_emb.edit(embed=pol_emb)
                case "adm" | "admin" | "pop" | "population" | "administration":
                    await help_emb.edit(embed=adm_emb)
                case _:
                    await help_emb.edit(embed=gen_emb)

            def chk(rec, usr):
                return usr == ctx.author and str(rec.emoji) in ['📊', '💶', '🧪', '🖍️', '🔨', '💥', '📜', '✒️']

            while True:
                try:
                    reaction, user = await bot.wait_for('reaction_add', timeout=60, check=chk)
                except TimeoutError:
                    break
                match(str(reaction.emoji)):   # Choosing Tab based on emoji
                    case '📊':
                        await help_emb.edit(embed=gen_emb)
                    case '💶':
                        await help_emb.edit(embed=eco_emb)
                    case '🧪':
                        await help_emb.edit(embed=tec_emb)
                    case '🖍️':
                        await help_emb.edit(embed=cus_emb)
                    case '🔨':
                        await help_emb.edit(embed=set_emb)
                    case '💥':
                        await help_emb.edit(embed=mil_emb)
                    case '📜':
                        await help_emb.edit(embed=pol_emb)
                    case '✒️':
                        await help_emb.edit(embed=adm_emb)
                    case _:
                        break
                await help_emb.remove_reaction(reaction.emoji, user)


@bot.command()   # Help command and command list made specifically for devs
async def devhelp(ctx, cmd: str = ""):
    if dev_check(ctx.author.id):
        global debug
        cmd = cmd.lower()
        match cmd:
            case "debug_mode" | "debugmode":
                embed = discord.Embed(colour=0xdc8a78, title="Dev Help | Debug Mode", type='rich',
                                      description=f'Syntax: `$debug_mode`{new_line}{new_line}'
                                                  f'Status: {debug}{new_line}{new_line}'
                                                  f'Switches the global variable \'debug\' from on to off and vice versa. {new_line}'
                                                  f'While on, this can do many things, but for now it only disables the error handler and prints the error to the console.{new_line}'
                                                  f'Debug mode is switched to off on boot.')
                await ctx.send(embed=embed)
            case "debug" | "debug_status" | "debugstatus" | "dstatus":
                embed = discord.Embed(colour=0xdc8a78, title="Dev Help | Debug Status", type='rich',
                                      description=f'Syntax: `$debug_status`{new_line}{new_line}'
                                                  f'Status: {debug}{new_line}{new_line}'
                                                  f'Shows whether debug mode is on or off')
                await ctx.send(embed=embed)
            case _:
                embed = discord.Embed(colour=0xdc8a78, title="Help | General", type='rich')  # General Tab
                embed.add_field(name="Debug", value="debug_mode - Turns debug mode on and off.\n"
                                                    "debug_status - Shows if debug mode is on or off.",
                                inline=False)
                await ctx.send(embed=embed)
    else:
        print(f'{ctx.author} attempted to enable debug')
        await ctx.send(f'Permission denied: You are not a developer.')


<<<<<<< HEAD
bot.run('TOKEN_HERE')
=======
bot.run('TOKEN_HERE')
>>>>>>> origin/main
