import sqlite3
import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents, case_insensitive=True)

# MUST READ NOTES:
# nation_score, gdp and population have no logic behind them, meaning it's worthless for now
# there is no way to recruit troops
# there are no weapons
# you can't make planes
# you can't make tanks
# you can't make barracks
# you can't make AA
# you can't make artillery
# you can only view infra, not make it
# you can't view info about infra
# there aren't emojis for infra because i am too lazy (deal with it)
# good luck making most of that stuff rev (hehe)

# Connect to the sqlite DB (it will create a new DB if it doesnt exit)
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
        weapon TEXT,
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



@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


@bot.command()
async def create(ctx, nation_name: str):
    user_id = ctx.author.id

    # Check if the user already has an account
    cursor.execute('SELECT 1 FROM user_info WHERE user_id = ?', (user_id,))
    existing_record = cursor.fetchone()

    if existing_record:
        await ctx.send("You have already created a nation.")
        return

    if len(nation_name) > 25:
        await ctx.send("You cannot have more than 25 characters.")
        return

    embed=discord.Embed(
        title='Nation Creation',
        description=f'This is the glorious start of **{nation_name}**! We wish you a successful journey in leading your people to greatness.',
        color=discord.Color.blurple()
        )
    await ctx.send(embed=embed)

    # insert data into the table
    cursor.execute('INSERT INTO user_info (user_id, nation_name) VALUES (?, ?)', (user_id, nation_name))
    conn.commit()

    print(f"successfully added {user_id}({nation_name})")
    
    # add base stats to the user
    cursor.execute('INSERT INTO user_stats (name, nation_score, gdp, population) VALUES (?, ?, ?, ?)',
        (nation_name, 0,0,100000))
    conn.commit()

    # add base mil stats to the user
    cursor.execute('INSERT INTO user_mil (name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (nation_name,0,0,'none',0,0,0,0))
    conn.commit()

    print(f"successfully add stats to {user_id}({nation_name})")

    #add base infra infra to the user
    cursor.execute('INSERT INTO infra (name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
        (nation_name,12500,1000,834,0,10,100,10,10,10,10,0,2500,0,0,0,0,0)) # the values came from ice cube's game sheet so just use that as a reference
    conn.commit()

    print(f"successfully add infra to {user_id}({nation_name})")


@bot.command()
async def rename(ctx, new_name: str):
    user_id = ctx.author.id

    if len(new_name) > 25:
        await ctx.send("You cannot have more than 25 characters.")
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

        embed=discord.Embed(
            title='Nation Rename',
            description=f'You have successfully changed your name to **{new_name}**!',
            color=discord.Color.blurple()
            )
        await ctx.send(embed=embed)
    else:
        await ctx.send("You do not have a nation, use`$create` to create one.")

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

            embed=discord.Embed(
                title=f"📊 {name}'s Stats",
                description=f'Name: {name}',
                color=discord.Color.blue()
                )
            embed.add_field(name='🫅 Ruler', value=f"<@{user_id}>", inline=False)
            embed.add_field(name='', value='',inline=False)
            embed.add_field(name='🏆 Nation Score', value=f'{nation_score}', inline=False)
            embed.add_field(name='', value='',inline=False)
            embed.add_field(name='📈 Gross Domestic Product', value=f'{gdp}',inline=False)
            embed.add_field(name='', value='',inline=False)
            embed.add_field(name='👪 Population', value=f'{population}',inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("No stats found.")
    else:
        await ctx.send("You do not have a nation, use `$create` to create one.")


@bot.command()
async def mstats(ctx):
    user_id = ctx.author.id

    # fetch user nation_name
    cursor.execute('SELECT nation_name FROM user_info WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        nation_name = result[0]

        # fetch user's mil stats
        cursor.execute('SELECT name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks FROM user_mil WHERE name_nation = ?', (nation_name,))
        mil_result = cursor.fetchone()

        if mil_result:
            name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks = mil_result

            embed=discord.Embed(
                title=f"⚔ {name_nation}'s Military Stats",
                description='',
                color=discord.Color.red()
                )
            embed.add_field(name='🪖 Troops', value=f'{troops}', inline=False)
            embed.add_field(name='', value='',inline=False)
            embed.add_field(name='⛟ Tanks', value=f'{tanks}',inline=False)
            embed.add_field(name='', value='',inline=False)
            embed.add_field(name='💥 Artillery', value=f'{artillery}',inline=False)
            embed.add_field(name='', value='',inline=False)
            embed.add_field(name='💥 Anti-Air', value=f'{anti_air}',inline=False)
            embed.add_field(name='', value='',inline=False)
            embed.add_field(name='🛫 Planes', value=f'{planes}',inline=False)
            embed.add_field(name='', value='',inline=False)
            embed.add_field(name='🎖 Barracks', value=f'{barracks}',inline=False)
            embed.add_field(name='', value='',inline=False)
            embed.add_field(name='🔫 Weapon', value=f'{weapon}',inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("No military stats found.")
    else:
        await ctx.send("You do not have a nation, use `$create` to create one.")


@bot.command()
async def infra(ctx):
    user_id = ctx.author.id

    # fetch user nation_name
    cursor.execute('SELECT nation_name FROM user_info WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        nation_name = result[0]

        # fetch user's infra
        cursor.execute('SELECT name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory FROM infra WHERE name = ?', (nation_name,))
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

            # paginate (if thats a word) the fields
            pages = []
            current_page = 0
            fields_per_page = 10

            while current_page < len(fields):
                embed = discord.Embed(title=f"{name}'s Infrastructure", color=discord.Color.blurple())

                for field_name, field_value in fields[current_page:current_page + fields_per_page]:
                    embed.add_field(name=field_name, value=field_value, inline=False)

                pages.append(embed)
                current_page += fields_per_page

            # Send the first page and add reactions for navigation
            message = await ctx.send(embed=pages[0])
            await message.add_reaction('⬅️')
            await message.add_reaction('➡️')

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ['⬅️', '➡️']

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
            await ctx.send("No infra stats found.")
    else:
        await ctx.send("You do not have a nation, use `$create` to create one.")



bot.run('TOKEN_HERE')