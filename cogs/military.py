import sqlite3
import asyncio
import discord
from discord.ext import commands
from discord.utils import get

new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = sqlite3.connect('player_info.db')
cursor = conn.cursor()


class Military(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # Recruit Command
    @commands.command()
    async def recruit(self, ctx, amount: int):
        user_id = ctx.author.id

        if amount <= 0:
            await ctx.send("Invalid amount, please try a positive number.")
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

            # fetch user's military stats
            cursor.execute(
                'SELECT name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks FROM user_mil WHERE name_nation = ?',
                (nation_name,))
            mil_result = cursor.fetchone()

            if res_result:
                name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                inf_ammo = amount * 0.2
                inf_food = amount * 0.03
                inf_turns = amount * 0.00003 + 1
                inf_time = int(inf_turns)
                time_turns = inf_time * 3600

                if (ammo <= inf_ammo) and (food <= inf_food):
                    await ctx.send("You do not have enough resources to recruit.")
                    return

                else:
                    emb = discord.Embed(title='Recruitment', type='rich',
                                        description=f'{amount:,} will be recruited into {name}\'s military.{new_line}'
                                                    f'They will be ready within {inf_time} turns.')
                    await ctx.send(embed=emb)

                    await asyncio.sleep(time_turns)

                    cursor.execute('UPDATE user_mil SET troops = troops + ? WHERE name_nation = ?', (amount, nation_name))
                    conn.commit()
            else:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description=f'Cannot find stats.')
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    # LIST OF MIL COMMANDS (tank, artillery, plane, anti-air)

    # Tank Production Command
    @commands.command()
    async def allocate(self, ctx, mil_type: str, amount: int):
        mil_type = mil_type.lower()
        user_id = ctx.author.id

        if amount <= 0:
            await ctx.send("Invalid amount, please try a positive number.")
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
                'SELECT name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory FROM infra WHERE name = ?',
                (nation_name,))
            infra_result = cursor.fetchone()

            # fetch user's military stats
            cursor.execute(
                'SELECT name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory FROM user_mil WHERE name_nation = ?',
                (nation_name,))
            mil_result = cursor.fetchone()

            if mil_result and res_result and infra_result:
                name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result
                name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result
                infra_name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory = infra_result


                match mil_type:
                    case "tank":
                        if amount > militaryfactory: # If user doesn't have enough mil factories, the command exits.
                            await ctx.send("You do not have enough military factories.")
                            return

                        else:
                            allocating = discord.Embed(title='Allocation | Tank', type='rich',
                                                    description=f'Allocating {amount:,} to {mil_type}...')
                            allo_emb = await ctx.send(embed=allocating)

                            prod_tank = amount * militaryfactory // 42
                            usage_tank_steel = amount * 5
                            usage_tank_gas = amount * 1.25

                            # Update military factory count.
                            cursor.execute('UPDATE infra SET militaryfactory = militaryfactory - ? WHERE name = ?', (amount, nation_name))
                            conn.commit()

                            # Update factory count.
                            cursor.execute('UPDATE user_mil SET tank_factory = tank_factory + ? WHERE name_nation = ?', (amount, nation_name))
                            conn.commit()

                            # Update resources.
                            cursor.execute('UPDATE resources SET steel = steel - ?, gasoline = gasoline - ? WHERE name = ? ', (usage_tank_steel, usage_tank_gas, nation_name))
                            conn.commit()

                            # Update tank count.
                            cursor.execute('UPDATE user_mil SET tanks = tanks + ? WHERE name_nation = ?', (prod_tank, nation_name))
                            conn.commit()

                            allo_done = discord.Embed(title='Allocation | Tank', type='rich',
                                                    description=f'Allocation Complete! {amount:,} military factories have been allocated.')
                            await allo_emb.edit(embed=allo_done)

                    case "plane":
                        if amount > militaryfactory: # If user doesn't have enough mil factories, the command exits.
                            await ctx.send("You do not have enough military factories.")
                            return

                        else:
                            allocating = discord.Embed(title='Allocation | Plane', type='rich',
                                                    description=f'Allocating {amount:,} to {mil_type}...')
                            allo_emb = await ctx.send(embed=allocating)

                            prod_plane = amount * militaryfactory // 45
                            usage_plane_steel = amount * 5.75
                            usage_plane_gas = amount * 2

                            # Update military factory count.
                            cursor.execute('UPDATE infra SET militaryfactory = militaryfactory - ? WHERE name = ?', (amount, nation_name))
                            conn.commit()

                            # Update factory count.
                            cursor.execute('UPDATE user_mil SET plane_factory = plane_factory + ? WHERE name_nation = ?', (amount, nation_name))
                            conn.commit()

                            # Update resources.
                            cursor.execute('UPDATE resources SET steel = steel - ?, gasoline = gasoline - ? WHERE name = ? ', (usage_plane_steel, usage_plane_gas, nation_name))
                            conn.commit()

                            # Update tank count.
                            cursor.execute('UPDATE user_mil SET planes = planes + ? WHERE name_nation = ?', (prod_plane, nation_name))
                            conn.commit()

                            allo_done = discord.Embed(title='Allocation | Plane', type='rich',
                                                    description=f'Allocation Complete! {amount:,} military factories have been allocated.')
                            await allo_emb.edit(embed=allo_done)

                    case "artillery":
                        if amount > militaryfactory: # If user doesn't have enough mil factories, the command exits.
                            await ctx.send("You do not have enough military factories.")
                            return

                        else:
                            allocating = discord.Embed(title='Allocation | Artillery', type='rich',
                                                    description=f'Allocating {amount:,} to {mil_type}...')
                            allo_emb = await ctx.send(embed=allocating)

                            prod_arty = amount * militaryfactory // 42
                            usage_arty_steel = amount * 3
                            usage_arty_gas = amount * 0.75

                            # Update military factory count.
                            cursor.execute('UPDATE infra SET militaryfactory = militaryfactory - ? WHERE name = ?', (amount, nation_name))
                            conn.commit()

                            # Update factory count.
                            cursor.execute('UPDATE user_mil SET artillery_factory = artillery_factory + ? WHERE name_nation = ?', (amount, nation_name))
                            conn.commit()

                            # Update resources.
                            cursor.execute('UPDATE resources SET steel = steel - ?, gasoline = gasoline - ? WHERE name = ? ', (usage_arty_steel, usage_arty_gas, nation_name))
                            conn.commit()

                            # Update tank count.
                            cursor.execute('UPDATE user_mil SET artillery = artillery + ? WHERE name_nation = ?', (prod_arty, nation_name))
                            conn.commit()

                            allo_done = discord.Embed(title='Allocation | Artillery', type='rich',
                                                    description=f'Allocation Complete! {amount:,} military factories have been allocated.')
                            await allo_emb.edit(embed=allo_done)

                    case "anti-air":
                        if amount > militaryfactory: # If user doesn't have enough mil factories, the command exits.
                            await ctx.send("You do not have enough military factories.")
                            return

                        else:
                            allocating = discord.Embed(title='Allocation | Anti-air', type='rich',
                                                    description=f'Allocating {amount:,} to {mil_type}...')
                            allo_emb = await ctx.send(embed=allocating)

                            prod_aa = amount * militaryfactory // 42
                            usage_aa_steel = amount * 4
                            usage_aa_gas = amount * 1

                            # Update military factory count.
                            cursor.execute('UPDATE infra SET militaryfactory = militaryfactory - ? WHERE name = ?', (amount, nation_name))
                            conn.commit()

                            # Update factory count.
                            cursor.execute('UPDATE user_mil SET anti_air_factory = anti_air_factory + ? WHERE name_nation = ?', (amount, nation_name))
                            conn.commit()

                            # Update resources.
                            cursor.execute('UPDATE resources SET steel = steel - ?, gasoline = gasoline - ? WHERE name = ? ', (usage_aa_steel, usage_aa_gas, nation_name))
                            conn.commit()

                            # Update tank count.
                            cursor.execute('UPDATE user_mil SET anti_air = anti_air + ? WHERE name_nation = ?', (prod_aa, nation_name))
                            conn.commit()

                            allo_done = discord.Embed(title='Allocation | Anti-air', type='rich',
                                                    description=f'Allocation Complete! {amount:,} military factories have been allocated.')
                            await allo_emb.edit(embed=allo_done)
            else:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description=f'Cannot find stats.')
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    # Deallocate Command.
    @commands.command()
    async def deallocate(self, ctx, mil_type: str, amount: int):
        mil_type = mil_type.lower()
        user_id = ctx.author.id

        if amount <= 0:
            await ctx.send("Invalid amount, please try a positive number.")
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
                'SELECT name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory FROM infra WHERE name = ?',
                (nation_name,))
            infra_result = cursor.fetchone()

            # fetch user's military stats
            cursor.execute(
                'SELECT name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory FROM user_mil WHERE name_nation = ?',
                (nation_name,))
            mil_result = cursor.fetchone()

            if mil_result and res_result and infra_result:
                name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result
                name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result
                infra_name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory = infra_result


                match mil_type:
                    case "tank":
                        if amount > tank_factory: # If user doesn't have enough mil factories, the command exits.
                            await ctx.send("You cannot deallocate more than you have.")
                            return

                        else:
                            deallocating = discord.Embed(title='Deallocation | Tank', type='rich',
                                                    description=f'Deallocating {amount:,} tank factories back to Military factories...')
                            deallo_emb = await ctx.send(embed=deallocating)

                            # Update military factory count.
                            cursor.execute('UPDATE infra SET militaryfactory = militaryfactory + ? WHERE name = ?', (amount, nation_name))
                            conn.commit()

                            # Update factory count.
                            cursor.execute('UPDATE user_mil SET tank_factory = tank_factory - ? WHERE name_nation = ?', (amount, nation_name))
                            conn.commit()

                            deallo_done = discord.Embed(title='Deallocation | Tank', type='rich',
                                                    description=f'Deallocation Complete! {amount:,} military factories have been deallocated.')
                            await deallo_emb.edit(embed=deallo_done)

                    case "plane":
                        if amount > plane_factory: # If user doesn't have enough mil factories, the command exits.
                            await ctx.send("You cannot deallocate more than you have.")
                            return

                        else:
                            deallocating = discord.Embed(title='Deallocation | Plane', type='rich',
                                                    description=f'Deallocating {amount:,} plane factories back to Military factories...')
                            deallo_emb = await ctx.send(embed=deallocating)

                            # Update military factory count.
                            cursor.execute('UPDATE infra SET militaryfactory = militaryfactory + ? WHERE name = ?', (amount, nation_name))
                            conn.commit()

                            # Update factory count.
                            cursor.execute('UPDATE user_mil SET plane_factory = plane_factory - ? WHERE name_nation = ?', (amount, nation_name))
                            conn.commit()

                            deallo_done = discord.Embed(title='Deallocation | Plane', type='rich',
                                                    description=f'Deallocation Complete! {amount:,} military factories have been deallocated.')
                            await deallo_emb.edit(embed=deallo_done)

                    case "artillery":
                        if amount > artillery_factory: # If user doesn't have enough mil factories, the command exits.
                            await ctx.send("You cannot deallocate more than you have.")
                            return

                        else:
                            deallocating = discord.Embed(title='Deallocation | Artillery', type='rich',
                                                    description=f'Deallocating {amount:,} artillery factories back to Military factories...')
                            deallo_emb = await ctx.send(embed=deallocating)

                            # Update military factory count.
                            cursor.execute('UPDATE infra SET militaryfactory = militaryfactory + ? WHERE name = ?', (amount, nation_name))
                            conn.commit()

                            # Update factory count.
                            cursor.execute('UPDATE user_mil SET artillery_factory = artillery_factory - ? WHERE name_nation = ?', (amount, nation_name))
                            conn.commit()

                            deallo_done = discord.Embed(title='Deallocation | Artillery', type='rich',
                                                    description=f'Deallocation Complete! {amount:,} military factories have been deallocated.')
                            await deallo_emb.edit(embed=deallo_done)

                    case "anti-air":
                        if amount > anti_air_factory: # If user doesn't have enough mil factories, the command exits.
                            await ctx.send("You cannot deallocate more than you have.")
                            return

                        else:
                            deallocating = discord.Embed(title='Deallocation | Anti-air', type='rich',
                                                    description=f'Deallocating {amount:,} anti-air factories back to Military factories...')
                            deallo_emb = await ctx.send(embed=deallocating)

                            # Update military factory count.
                            cursor.execute('UPDATE infra SET militaryfactory = militaryfactory + ? WHERE name = ?', (amount, nation_name))
                            conn.commit()

                            # Update factory count.
                            cursor.execute('UPDATE user_mil SET anti_air_factory = anti_air_factory - ? WHERE name_nation = ?', (amount, nation_name))
                            conn.commit()

                            deallo_done = discord.Embed(title='Deallocation | Anti-air', type='rich',
                                                    description=f'Deallocation Complete! {amount:,} military factories have been deallocated.')
                            await deallo_emb.edit(embed=deallo_done)
            else:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description=f'Cannot find stats.')
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Military(bot))