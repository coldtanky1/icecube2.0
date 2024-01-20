import sqlite3
import asyncio
import os
import time
import discord
from discord.ext import commands
from discord.utils import get

# Importing game functions.
from game_functions.PopGrowth import *

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents, case_insensitive=True)

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()
<<<<<<< HEAD
    await bot.start('TOKEN_HERE
=======
    await bot.start('TOKEN_HERE')
>>>>>>> origin/main


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
        child INTEGER,
        teen INTEGER,
        adult INTEGER,
        elder INTEGER,
        balance INTEGER
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
        barracks INTEGER,
        tank_factory INTEGER,
        plane_factory INTEGER,
        artillery_factory INTEGER,
        anti_air_factory INTEGER
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
        concrete_factory INTEGER,
        militaryfactory INTEGER
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


# Update Command
user_last_update = {}

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def update(ctx):
    user_id = ctx.author.id

    # Check if the user has a record in the dictionary
    if user_id not in user_last_update:
        user_last_update[user_id] = time.time()
        turns_accumulated = 0
    else:
        current_time = time.time()
        last_update_time = user_last_update[user_id]
        elapsed_time = current_time - last_update_time

        # Calculate the number of turns accumulated during the elapsed time
        turns_accumulated = int(elapsed_time / 10)

        # Update the last update time
        user_last_update[user_id] = current_time

    # fetch user nation_name
    cursor.execute('SELECT nation_name FROM user_info WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        nation_name = result[0]

        popgrowth(user_id)

        # fetch user's production infra
        cursor.execute(
            'SELECT name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory FROM infra WHERE name = ?',
            (nation_name,))
        infra_result = cursor.fetchone()

        # fetch user's military stats
        cursor.execute(
            'SELECT name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory FROM user_mil WHERE name_nation = ?',
            (nation_name,))
        mil_result = cursor.fetchone()

        # fetch user's resources
        cursor.execute(
            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
            (nation_name,))
        res_result = cursor.fetchone()

        # Function to update Pop.


        if infra_result and mil_result and res_result:
            name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory = infra_result
            name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result
            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result


            # The production of each resource
            prod_wood = lumber_mill * 2 * turns_accumulated
            prod_coal = coal_mine * 1.2 * turns_accumulated
            prod_iron = iron_mine * 1 * turns_accumulated
            prod_lead = lead_mine * 0.8 * turns_accumulated
            prod_bauxite = bauxite_mine * 0.6 * turns_accumulated
            prod_oil = oil_derrick * 1 * turns_accumulated
            prod_uranium = uranium_mine * 0.05 * turns_accumulated
            prod_farm = farm * 10 * turns_accumulated
            prod_aluminium = aluminium_factory * 0.4 * turns_accumulated
            prod_steel = steel_factory * 0.3 * turns_accumulated
            prod_gas = oil_refinery * 0.2 * turns_accumulated
            prod_ammo = ammo_factory * 0.5 * turns_accumulated
            prod_concrete = concrete_factory * 0.6 * turns_accumulated


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

            final_usage_iron = usage_iron_wood + usage_iron_coal + usage_iron_iron + usage_iron_lead + usage_iron_bauxite + usage_iron_oil + usage_iron_uranium + usage_iron_food + usage_iron_aluminium + usage_iron_steel + usage_iron_ammo + usage_iron_concrete  * turns_accumulated
            final_usage_lead = usage_lead_wood + usage_lead_coal + usage_lead_iron + usage_lead_lead + usage_lead_bauxite + usage_lead_oil + usage_lead_uranium + usage_lead_food + usage_lead_aluminium + usage_lead_steel + usage_lead_ammo + usage_lead_concrete  * turns_accumulated
            final_usage_bauxite = usage_bauxite_wood + usage_bauxite_coal + usage_bauxite_iron + usage_bauxite_lead + usage_bauxite_bauxite + usage_bauxite_oil + usage_bauxite_uranium + usage_bauxite_food + usage_bauxite_aluminium + usage_bauxite_steel + usage_bauxite_ammo + usage_bauxite_concrete  * turns_accumulated

            final_prod_iron = prod_iron - final_usage_iron
            final_prod_lead = prod_lead - final_usage_lead
            final_prod_bauxite = prod_bauxite - final_usage_bauxite
            final_prod_oil = prod_oil - usage_oil_gas

            updating_emb = discord.Embed(
                title='Update',
                type='rich',
                description=f'Updating {turns_accumulated}...',
                color=0x4CAF50
                )
            update_emb = await ctx.send(embed=updating_emb)

            # Update Military.

            prod_aa = anti_air_factory * militaryfactory // 42
            usage_aa_steel = anti_air_factory * 4
            usage_aa_gas = anti_air_factory * 1
            prod_arty = artillery_factory * militaryfactory // 42
            usage_arty_steel = artillery_factory * 3
            usage_arty_gas = artillery_factory * 0.75
            prod_plane = plane_factory * militaryfactory // 45
            usage_plane_steel = plane_factory * 5.75
            usage_plane_gas = plane_factory * 2
            prod_tank = tank_factory * militaryfactory // 42
            usage_tank_steel = tank_factory * 5
            usage_tank_gas = tank_factory * 1.25

            # Update Tanks.
            # Update resources.
            cursor.execute('UPDATE resources SET steel = steel - ?, gasoline = gasoline - ? WHERE name = ? ', (usage_tank_steel, usage_tank_gas, nation_name))
            conn.commit()

            # Update tank count.
            cursor.execute('UPDATE user_mil SET tanks = tanks + ? WHERE name_nation = ?', (prod_tank, nation_name))
            conn.commit()

            # Update Planes.
            # Update resources.
            cursor.execute('UPDATE resources SET steel = steel - ?, gasoline = gasoline - ? WHERE name = ? ', (usage_plane_steel, usage_plane_gas, nation_name))
            conn.commit()

            # Update plane count.
            cursor.execute('UPDATE user_mil SET planes = planes + ? WHERE name_nation = ?', (prod_plane, nation_name))
            conn.commit()

            # Update Artillery.
            # Update resources.
            cursor.execute('UPDATE resources SET steel = steel - ?, gasoline = gasoline - ? WHERE name = ? ', (usage_arty_steel, usage_arty_gas, nation_name))
            conn.commit()

            # Update artillery count.
            cursor.execute('UPDATE user_mil SET artillery = artillery + ? WHERE name_nation = ?', (prod_arty, nation_name))
            conn.commit()

            # Update Anti-Air.
            # Update resources.
            cursor.execute('UPDATE resources SET steel = steel - ?, gasoline = gasoline - ? WHERE name = ? ', (usage_aa_steel, usage_aa_gas, nation_name))
            conn.commit()

            # Update anti-air count.
            cursor.execute('UPDATE user_mil SET anti_air = anti_air + ? WHERE name_nation = ?', (prod_aa, nation_name))
            conn.commit()


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
                description=f"Updated {turns_accumulated}!",
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


asyncio.run(main())
