import sqlite3
import asyncio
import discord
from discord.ext import commands
from discord.utils import get

new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = sqlite3.connect('player_info.db')
cursor = conn.cursor()


class Construct(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def construct(self, ctx, building: str, amount: int):
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
                    case "basichouse":
                        basichouse_amt = amount
                        basichouse_wood = basichouse_amt * 2
                        basichouse_concrete = basichouse_amt * 0.6
                        embed = discord.Embed(colour=0xdd7878, title="Construct: Basic House", type='rich',
                                                                description=f'{basichouse_amt:,} will be constructed.{new_line}{new_line}'
                                                                            f'The basic houses will cost: {basichouse_wood:,} Wood{new_line}'
                                                                            f'The basic houses will cost: {basichouse_concrete:,} Concrete')
                        await ctx.send(embed=embed)

                        try:
                            await ctx.send("Would you like to proceed? Respond with y/n.")

                            def check(message):
                                return message.content.lower() in ['y', 'n'] 

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)


                            if response_message.content.lower() == 'y':
                                constructing = discord.Embed(colour=0xdd7878, title='Construct', type='rich',
                                                                    description='Constructing...')
                                construct_msg = await ctx.send(embed=constructing)


                                if res_result:
                                    name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                                    # Check if user has enough wood and concrete
                                    if (wood >= basichouse_wood) and (concrete >= basichouse_concrete):

                                        # If user has enough woodand concrete then it proceeds normally.
                                        # Update the resources table
                                        cursor.execute('''
                                            UPDATE resources SET
                                            wood = wood - ?,
                                            concrete = concrete - ?
                                            WHERE name = ?
                                        ''', (basichouse_wood, basichouse_concrete, nation_name))

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

                    case "smallflat":
                        smallflat_amt = amount
                        smallflat_wood = smallflat_amt * 1
                        smallflat_concrete = smallflat_amt * 6
                        smallflat_steel = smallflat_amt * 0.5
                        embed = discord.Embed(colour=0xdd7878, title="Construct: Small Flat", type='rich',
                                                                description=f'{smallflat_amt:,} will be constructed.{new_line}{new_line}'
                                                                            f'The basic houses will cost: {smallflat_wood:,} Wood{new_line}'
                                                                            f'The basic houses will cost: {smallflat_concrete:,} Concrete{new_line}'
                                                                            f'The basic houses will cost: {smallflat_steel:,} Steel')
                        await ctx.send(embed=embed)

                        try:
                            await ctx.send("Would you like to proceed? Respond with y/n.")

                            def check(message):
                                return message.content.lower() in ['y', 'n'] 

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)


                            if response_message.content.lower() == 'y':
                                constructing = discord.Embed(colour=0xdd7878, title='Construct', type='rich',
                                                                    description='Constructing...')
                                construct_msg = await ctx.send(embed=constructing)


                                if res_result:
                                    name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                                    # Check if user has enough wood or concrete
                                    if (wood >= smallflat_wood) and (concrete >= smallflat_concrete) and (steel >= smallflat_steel):

                                        # If user has enough wood or concrete then it proceeds normally.
                                        # Update the resources table
                                        cursor.execute('''
                                            UPDATE resources SET
                                            wood = wood - ?,
                                            concrete = concrete - ?,
                                            steel = steel - ?
                                            WHERE name = ?
                                        ''', (smallflat_wood, smallflat_concrete, smallflat_steel, nation_name))

                                        cursor.execute('UPDATE infra SET small_flat = small_flat + ? WHERE name = ?', (smallflat_amt, nation_name))

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

                    case "aptcomplex":
                        aptcomplex_amt = amount
                        aptcomplex_wood = aptcomplex_amt * 1
                        aptcomplex_concrete = aptcomplex_amt * 7
                        aptcomplex_steel = aptcomplex_amt * 0.5
                        embed = discord.Embed(colour=0xdd7878, title="Construct: Apartment Complex", type='rich',
                                                                description=f'{aptcomplex_amt:,} will be constructed.{new_line}{new_line}'
                                                                            f'The basic houses will cost: {aptcomplex_wood:,} Wood{new_line}'
                                                                            f'The basic houses will cost: {aptcomplex_concrete:,} Concrete{new_line}'
                                                                            f'The basic houses will cost: {aptcomplex_steel:,} Steel')
                        await ctx.send(embed=embed)

                        try:
                            await ctx.send("Would you like to proceed? Respond with y/n.")

                            def check(message):
                                return message.content.lower() in ['y', 'n'] 

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)


                            if response_message.content.lower() == 'y':
                                constructing = discord.Embed(colour=0xdd7878, title='Construct', type='rich',
                                                                    description='Constructing...')
                                construct_msg = await ctx.send(embed=constructing)


                                if res_result:
                                    name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                                    # Check if user has enough wood or concrete
                                    if (wood >= aptcomplex_wood) and (concrete >= aptcomplex_concrete) and (steel >= aptcomplex_steel):

                                        # If user has enough wood or concrete then it proceeds normally.
                                        # Update the resources table
                                        cursor.execute('''
                                            UPDATE resources SET
                                            wood = wood - ?,
                                            concrete = concrete - ?,
                                            steel = steel - ?
                                            WHERE name = ?
                                        ''', (aptcomplex_wood, aptcomplex_concrete, aptcomplex_steel, nation_name))

                                        cursor.execute('UPDATE infra SET apt_complex = apt_complex + ? WHERE name = ?', (aptcomplex_amt, nation_name))

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

                    case "skyscraper":
                        skyscraper_amt = amount
                        skyscraper_wood = skyscraper_amt * 0
                        skyscraper_concrete = skyscraper_amt * 10
                        skyscraper_steel = skyscraper_amt * 2
                        embed = discord.Embed(colour=0xdd7878, title="Construct: Skyscraper", type='rich',
                                                                description=f'{skyscraper_amt:,} will be constructed.{new_line}{new_line}'
                                                                            f'The basic houses will cost: {skyscraper_wood:,} Wood{new_line}'
                                                                            f'The basic houses will cost: {skyscraper_concrete:,} Concrete{new_line}'
                                                                            f'The basic houses will cost: {skyscraper_steel:,} Steel')
                        await ctx.send(embed=embed)

                        try:
                            await ctx.send("Would you like to proceed? Respond with y/n.")

                            def check(message):
                                return message.content.lower() in ['y', 'n'] 

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)


                            if response_message.content.lower() == 'y':
                                constructing = discord.Embed(colour=0xdd7878, title='Construct', type='rich',
                                                                    description='Constructing...')
                                construct_msg = await ctx.send(embed=constructing)


                                if res_result:
                                    name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                                    # Check if user has enough wood or concrete
                                    if (wood >= skyscraper_wood) and (concrete >= skyscraper_concrete) and (steel >= skyscraper_steel):

                                        # If user has enough wood or concrete then it proceeds normally.
                                        # Update the resources table
                                        cursor.execute('''
                                            UPDATE resources SET
                                            wood = wood - ?,
                                            concrete = concrete - ?,
                                            steel = steel - ?
                                            WHERE name = ?
                                        ''', (skyscraper_wood, skyscraper_concrete, skyscraper_steel, nation_name))

                                        cursor.execute('UPDATE infra SET skyscraper = skyscraper + ? WHERE name = ?', (skyscraper_amt, nation_name))

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

                    case "lumbermill":
                        lumber_amt = amount
                        lumber_wood = lumber_amt * 0.4
                        lumber_concrete = lumber_amt * 0
                        lumber_steel = lumber_amt * 0
                        embed = discord.Embed(colour=0xdd7878, title="Construct: Lumber Mill", type='rich',
                                                                description=f'{lumber_amt:,} will be constructed.{new_line}{new_line}'
                                                                            f'The basic houses will cost: {lumber_wood:,} Wood{new_line}'
                                                                            f'The basic houses will cost: {lumber_concrete:,} Concrete{new_line}'
                                                                            f'The basic houses will cost: {lumber_steel:,} Steel')
                        await ctx.send(embed=embed)

                        try:
                            await ctx.send("Would you like to proceed? Respond with y/n.")

                            def check(message):
                                return message.content.lower() in ['y', 'n'] 

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)


                            if response_message.content.lower() == 'y':
                                constructing = discord.Embed(colour=0xdd7878, title='Construct', type='rich',
                                                                    description='Constructing...')
                                construct_msg = await ctx.send(embed=constructing)


                                if res_result:
                                    name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                                    # Check if user has enough wood or concrete
                                    if (wood >= lumber_wood) and (concrete >= lumber_concrete) and (steel >= lumber_steel):

                                        # If user has enough wood or concrete then it proceeds normally.
                                        # Update the resources table
                                        cursor.execute('''
                                            UPDATE resources SET
                                            wood = wood - ?,
                                            concrete = concrete - ?,
                                            steel = steel - ?
                                            WHERE name = ?
                                        ''', (lumber_wood, lumber_concrete, lumber_steel, nation_name))

                                        cursor.execute('UPDATE infra SET lumber_mill = lumber_mill + ? WHERE name = ?', (lumber_amt, nation_name))

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

                    case "coalmine":
                        coal_amt = amount
                        coal_wood = coal_amt * 2
                        coal_concrete = coal_amt * 0
                        coal_steel = coal_amt * 0
                        embed = discord.Embed(colour=0xdd7878, title="Construct: Coal Mine", type='rich',
                                                                description=f'{coal_amt:,} will be constructed.{new_line}{new_line}'
                                                                            f'The basic houses will cost: {coal_wood:,} Wood{new_line}'
                                                                            f'The basic houses will cost: {coal_concrete:,} Concrete{new_line}'
                                                                            f'The basic houses will cost: {coal_steel:,} Steel')
                        await ctx.send(embed=embed)

                        try:
                            await ctx.send("Would you like to proceed? Respond with y/n.")

                            def check(message):
                                return message.content.lower() in ['y', 'n'] 

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)


                            if response_message.content.lower() == 'y':
                                constructing = discord.Embed(colour=0xdd7878, title='Construct', type='rich',
                                                                    description='Constructing...')
                                construct_msg = await ctx.send(embed=constructing)


                                if res_result:
                                    name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                                    # Check if user has enough wood or concrete
                                    if (wood >= coal_wood) and (concrete >= coal_concrete) and (steel >= coal_steel):

                                        # If user has enough wood or concrete then it proceeds normally.
                                        # Update the resources table
                                        cursor.execute('''
                                            UPDATE resources SET
                                            wood = wood - ?,
                                            concrete = concrete - ?,
                                            steel = steel - ?
                                            WHERE name = ?
                                        ''', (coal_wood, coal_concrete, coal_steel, nation_name))

                                        cursor.execute('UPDATE infra SET coal_mine = coal_mine + ? WHERE name = ?', (coal_amt, nation_name))

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


                    case "ironmine":
                        iron_amt = amount
                        iron_wood = coal_amt * 2
                        iron_concrete = coal_amt * 0
                        iron_steel = coal_amt * 0
                        embed = discord.Embed(colour=0xdd7878, title="Construct: Iron Mine", type='rich',
                                                                description=f'{iron_amt:,} will be constructed.{new_line}{new_line}'
                                                                            f'The basic houses will cost: {iron_wood:,} Wood{new_line}'
                                                                            f'The basic houses will cost: {iron_concrete:,} Concrete{new_line}'
                                                                            f'The basic houses will cost: {iron_steel:,} Steel')
                        await ctx.send(embed=embed)

                        try:
                            await ctx.send("Would you like to proceed? Respond with y/n.")

                            def check(message):
                                return message.content.lower() in ['y', 'n'] 

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)


                            if response_message.content.lower() == 'y':
                                constructing = discord.Embed(colour=0xdd7878, title='Construct', type='rich',
                                                                    description='Constructing...')
                                construct_msg = await ctx.send(embed=constructing)


                                if res_result:
                                    name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                                    # Check if user has enough wood or concrete
                                    if (wood >= iron_wood) and (concrete >= iron_concrete) and (steel >= iron_steel):

                                        # If user has enough wood or concrete then it proceeds normally.
                                        # Update the resources table
                                        cursor.execute('''
                                            UPDATE resources SET
                                            wood = wood - ?,
                                            concrete = concrete - ?,
                                            steel = steel - ?
                                            WHERE name = ?
                                        ''', (iron_wood, iron_concrete, iron_steel, nation_name))

                                        cursor.execute('UPDATE infra SET iron_mine = iron_mine + ? WHERE name = ?', (iron_amt, nation_name))

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

                    case "leadmine":
                        lead_amt = amount
                        lead_wood = lead_amt * 2
                        lead_concrete = lead_amt * 0
                        lead_steel = lead_amt * 0
                        embed = discord.Embed(colour=0xdd7878, title="Construct: Lead Mine", type='rich',
                                                                description=f'{lead_amt:,} will be constructed.{new_line}{new_line}'
                                                                            f'The basic houses will cost: {lead_wood:,} Wood{new_line}'
                                                                            f'The basic houses will cost: {lead_concrete:,} Concrete{new_line}'
                                                                            f'The basic houses will cost: {lead_steel:,} Steel')
                        await ctx.send(embed=embed)

                        try:
                            await ctx.send("Would you like to proceed? Respond with y/n.")

                            def check(message):
                                return message.content.lower() in ['y', 'n'] 

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)


                            if response_message.content.lower() == 'y':
                                constructing = discord.Embed(colour=0xdd7878, title='Construct', type='rich',
                                                                    description='Constructing...')
                                construct_msg = await ctx.send(embed=constructing)


                                if res_result:
                                    name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                                    # Check if user has enough wood or concrete
                                    if (wood >= lead_wood)and (concrete >= lead_concrete)and (steel >= iron_steel):

                                        # If user has enough wood or concrete then it proceeds normally.
                                        # Update the resources table
                                        cursor.execute('''
                                            UPDATE resources SET
                                            wood = wood - ?,
                                            concrete = concrete - ?,
                                            steel = steel - ?
                                            WHERE name = ?
                                        ''', (lead_wood, lead_concrete, lead_steel, nation_name))

                                        cursor.execute('UPDATE infra SET lead_mine = lead_mine + ? WHERE name = ?', (lead_amt, nation_name))

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

                    case "bauxitemine":
                        bauxite_amt = amount
                        bauxite_wood = coal_amt * 2
                        bauxite_concrete = coal_amt * 0
                        bauxite_steel = coal_amt * 0
                        embed = discord.Embed(colour=0xdd7878, title="Construct: Bauxite Mine", type='rich',
                                                                description=f'{bauxite_amt:,} will be constructed.{new_line}{new_line}'
                                                                            f'The basic houses will cost: {bauxite_wood:,} Wood{new_line}'
                                                                            f'The basic houses will cost: {bauxite_concrete:,} Concrete{new_line}'
                                                                            f'The basic houses will cost: {bauxite_steel:,} Steel')
                        await ctx.send(embed=embed)

                        try:
                            await ctx.send("Would you like to proceed? Respond with y/n.")

                            def check(message):
                                return message.content.lower() in ['y', 'n'] 

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)


                            if response_message.content.lower() == 'y':
                                constructing = discord.Embed(colour=0xdd7878, title='Construct', type='rich',
                                                                    description='Constructing...')
                                construct_msg = await ctx.send(embed=constructing)


                                if res_result:
                                    name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                                    # Check if user has enough wood or concrete
                                    if (wood >= bauxite_wood)and (concrete >= bauxite_concrete)and (steel >= bauxite_steel):

                                        # If user has enough wood or concrete then it proceeds normally.
                                        # Update the resources table
                                        cursor.execute('''
                                            UPDATE resources SET
                                            wood = wood - ?,
                                            concrete = concrete - ?,
                                            steel = steel - ?
                                            WHERE name = ?
                                        ''', (bauxite_wood, bauxite_concrete, bauxite_steel, nation_name))

                                        cursor.execute('UPDATE infra SET bauxite_mine = bauxite_mine + ? WHERE name = ?', (bauxite_amt, nation_name))

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

                    case "oilderrick":
                        oil_amt = amount
                        oil_wood = oil_amt * 0
                        oil_concrete = oil_amt * 1
                        oil_steel = oil_amt * 3
                        embed = discord.Embed(colour=0xdd7878, title="Construct: Oil Derrick", type='rich',
                                                                description=f'{oil_amt:,} will be constructed.{new_line}{new_line}'
                                                                            f'The basic houses will cost: {oil_wood:,} Wood{new_line}'
                                                                            f'The basic houses will cost: {oil_concrete:,} Concrete{new_line}'
                                                                            f'The basic houses will cost: {oil_steel:,} Steel')
                        await ctx.send(embed=embed)

                        try:
                            await ctx.send("Would you like to proceed? Respond with y/n.")

                            def check(message):
                                return message.content.lower() in ['y', 'n'] 

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)


                            if response_message.content.lower() == 'y':
                                constructing = discord.Embed(colour=0xdd7878, title='Construct', type='rich',
                                                                    description='Constructing...')
                                construct_msg = await ctx.send(embed=constructing)


                                if res_result:
                                    name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                                    # Check if user has enough wood or concrete
                                    if (wood >= oil_wood)and (concrete >= oil_concrete)and (steel >= oil_steel):

                                        # If user has enough wood or concrete then it proceeds normally.
                                        # Update the resources table
                                        cursor.execute('''
                                            UPDATE resources SET
                                            wood = wood - ?,
                                            concrete = concrete - ?,
                                            steel = steel - ?
                                            WHERE name = ?
                                        ''', (oil_wood, oil_concrete, oil_steel, nation_name))

                                        cursor.execute('UPDATE infra SET oil_derrick = oil_derrick + ? WHERE name = ?', (oil_amt, nation_name))

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

                    case "uraniummine":
                        uranium_amt = amount
                        uranium_wood = uranium_amt * 5
                        uranium_concrete = uranium_amt * 0.5
                        uranium_steel = uranium_amt * 0.3
                        embed = discord.Embed(colour=0xdd7878, title="Construct: Uranium Mine", type='rich',
                                                                description=f'{uranium_amt:,} will be constructed.{new_line}{new_line}'
                                                                            f'The basic houses will cost: {uranium_wood:,} Wood{new_line}'
                                                                            f'The basic houses will cost: {uranium_concrete:,} Concrete{new_line}'
                                                                            f'The basic houses will cost: {uranium_steel:,} Steel')
                        await ctx.send(embed=embed)

                        try:
                            await ctx.send("Would you like to proceed? Respond with y/n.")

                            def check(message):
                                return message.content.lower() in ['y', 'n'] 

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)


                            if response_message.content.lower() == 'y':
                                constructing = discord.Embed(colour=0xdd7878, title='Construct', type='rich',
                                                                    description='Constructing...')
                                construct_msg = await ctx.send(embed=constructing)


                                if res_result:
                                    name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                                    # Check if user has enough wood or concrete
                                    if (wood >= uranium_wood)and (concrete >= uranium_concrete)and (steel >= uranium_steel):

                                        # If user has enough wood or concrete then it proceeds normally.
                                        # Update the resources table
                                        cursor.execute('''
                                            UPDATE resources SET
                                            wood = wood - ?,
                                            concrete = concrete - ?,
                                            steel = steel - ?,
                                            WHERE name = ?
                                        ''', (uranium_wood, uranium_concrete, uranium_steel,nation_name))

                                        cursor.execute('UPDATE infra SET uranium_mine = uranium_mine + ? WHERE name = ?', (uranium_amt, nation_name))

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

                    case "farm":
                        farm_amt = amount
                        farm_wood = farm_amt * 5
                        farm_concrete = farm_amt * 0.5
                        farm_steel = farm_amt * 0.2
                        embed = discord.Embed(colour=0xdd7878, title="Construct: Farm", type='rich',
                                                                description=f'{farm_amt:,} will be constructed.{new_line}{new_line}'
                                                                            f'The basic houses will cost: {farm_wood:,} Wood{new_line}'
                                                                            f'The basic houses will cost: {farm_concrete:,} Concrete{new_line}'
                                                                            f'The basic houses will cost: {farm_steel:,} Steel')
                        await ctx.send(embed=embed)

                        try:
                            await ctx.send("Would you like to proceed? Respond with y/n.")

                            def check(message):
                                return message.content.lower() in ['y', 'n'] 

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)


                            if response_message.content.lower() == 'y':
                                constructing = discord.Embed(colour=0xdd7878, title='Construct', type='rich',
                                                                    description='Constructing...')
                                construct_msg = await ctx.send(embed=constructing)


                                if res_result:
                                    name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                                    # Check if user has enough wood or concrete
                                    if (wood >= farm_wood)and (concrete >= farm_concrete)and (steel >= farm_steel):

                                        # If user has enough wood or concrete then it proceeds normally.
                                        # Update the resources table
                                        cursor.execute('''
                                            UPDATE resources SET
                                            wood = wood - ?,
                                            concrete = concrete - ?,
                                            steel = steel - ?
                                            WHERE name = ?
                                        ''', (farm_wood, farm_concrete, farm_steel,nation_name))

                                        cursor.execute('UPDATE infra SET farm = farm + ? WHERE name = ?', (farm_amt, nation_name))

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

                    case "aluminiumfactory":
                        aluminium_amt = amount
                        aluminium_wood = aluminium_amt * 0
                        aluminium_concrete = aluminium_amt * 4
                        aluminium_steel = aluminium_amt * 3
                        embed = discord.Embed(colour=0xdd7878, title="Construct: Aluminium Factory", type='rich',
                                                                description=f'{aluminium_amt:,} will be constructed.{new_line}{new_line}'
                                                                            f'The basic houses will cost: {aluminium_wood:,} Wood{new_line}'
                                                                            f'The basic houses will cost: {aluminium_concrete:,} Concrete{new_line}'
                                                                            f'The basic houses will cost: {aluminium_steel:,} Steel')
                        await ctx.send(embed=embed)

                        try:
                            await ctx.send("Would you like to proceed? Respond with y/n.")

                            def check(message):
                                return message.content.lower() in ['y', 'n'] 

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)


                            if response_message.content.lower() == 'y':
                                constructing = discord.Embed(colour=0xdd7878, title='Construct', type='rich',
                                                                    description='Constructing...')
                                construct_msg = await ctx.send(embed=constructing)


                                if res_result:
                                    name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                                    # Check if user has enough wood or concrete
                                    if (wood >= aluminium_wood)and (concrete >= aluminium_concrete) and (steel >= aluminium_steel):

                                        # If user has enough wood or concrete then it proceeds normally.
                                        # Update the resources table
                                        cursor.execute('''
                                            UPDATE resources SET
                                            wood = wood - ?,
                                            concrete = concrete - ?,
                                            steel = steel - ?
                                            WHERE name = ?
                                        ''', (aluminium_wood, aluminium_concrete, aluminium_steel, nation_name))

                                        cursor.execute('UPDATE infra SET aluminium_factory = aluminium_factory + ? WHERE name = ?', (aluminium_amt, nation_name))

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

                    case "steelfactory":
                        steel_amt = amount
                        steel_wood = steel_amt * 0
                        steel_concrete = steel_amt * 6
                        steel_steel = steel_amt * 4
                        embed = discord.Embed(colour=0xdd7878, title="Construct: Steel Factory", type='rich',
                                                                description=f'{steel_amt:,} will be constructed.{new_line}{new_line}'
                                                                            f'The basic houses will cost: {steel_wood:,} Wood{new_line}'
                                                                            f'The basic houses will cost: {steel_concrete:,} Concrete{new_line}'
                                                                            f'The basic houses will cost: {steel_steel:,} Steel')
                        await ctx.send(embed=embed)

                        try:
                            await ctx.send("Would you like to proceed? Respond with y/n.")

                            def check(message):
                                return message.content.lower() in ['y', 'n'] 

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)


                            if response_message.content.lower() == 'y':
                                constructing = discord.Embed(colour=0xdd7878, title='Construct', type='rich',
                                                                    description='Constructing...')
                                construct_msg = await ctx.send(embed=constructing)


                                if res_result:
                                    name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                                    # Check if user has enough wood or concrete
                                    if (wood >= steel_wood)and (concrete >= steel_concrete)and (steel >= steel_steel):

                                        # If user has enough wood or concrete then it proceeds normally.
                                        # Update the resources table
                                        cursor.execute('''
                                            UPDATE resources SET
                                            wood = wood - ?,
                                            concrete = concrete - ?,
                                            steel = steel - ?
                                            WHERE name = ?
                                        ''', (steel_wood, steel_concrete, steel_steel, nation_name))

                                        cursor.execute('UPDATE infra SET steel_factory = steel_factory + ? WHERE name = ?', (steel_amt, nation_name))

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

                    case "oilrefinery":
                        gas_amt = amount
                        gas_wood = gas_amt * 2
                        gas_concrete = gas_amt * 4
                        gas_steel = gas_amt * 4
                        embed = discord.Embed(colour=0xdd7878, title="Construct: Oil Refinery", type='rich',
                                                                description=f'{gas_amt:,} will be constructed.{new_line}{new_line}'
                                                                            f'The basic houses will cost: {gas_wood:,} Wood{new_line}'
                                                                            f'The basic houses will cost: {gas_concrete:,} Concrete{new_line}'
                                                                            f'The basic houses will cost: {gas_steel:,} Steel')
                        await ctx.send(embed=embed)

                        try:
                            await ctx.send("Would you like to proceed? Respond with y/n.")

                            def check(message):
                                return message.content.lower() in ['y', 'n'] 

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)


                            if response_message.content.lower() == 'y':
                                constructing = discord.Embed(colour=0xdd7878, title='Construct', type='rich',
                                                                    description='Constructing...')
                                construct_msg = await ctx.send(embed=constructing)


                                if res_result:
                                    name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                                    # Check if user has enough wood or concrete
                                    if (wood >= gas_wood)and (concrete >= gas_concrete)and (steel >= gas_steel):

                                        # If user has enough wood or concrete then it proceeds normally.
                                        # Update the resources table
                                        cursor.execute('''
                                            UPDATE resources SET
                                            wood = wood - ?,
                                            concrete = concrete - ?,
                                            steel = steel - ?
                                            WHERE name = ?
                                        ''', (gas_wood, gas_concrete, gas_steel, nation_name))

                                        cursor.execute('UPDATE infra SET oil_refinery = oil_refinery + ? WHERE name = ?', (oil_amt, nation_name))

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

                    case "ammofactory":
                        ammo_amt = amount
                        ammo_wood = ammo_amt * 0
                        ammo_concrete = ammo_amt * 1.2
                        ammo_steel = ammo_amt * 0.6
                        embed = discord.Embed(colour=0xdd7878, title="Construct: Munitions Factory", type='rich',
                                                                description=f'{ammo_amt:,} will be constructed.{new_line}{new_line}'
                                                                            f'The basic houses will cost: {ammo_wood:,} Wood{new_line}'
                                                                            f'The basic houses will cost: {ammo_concrete:,} Concrete{new_line}'
                                                                            f'The basic houses will cost: {ammo_steel:,} Steel')
                        await ctx.send(embed=embed)

                        try:
                            await ctx.send("Would you like to proceed? Respond with y/n.")

                            def check(message):
                                return message.content.lower() in ['y', 'n'] 

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)


                            if response_message.content.lower() == 'y':
                                constructing = discord.Embed(colour=0xdd7878, title='Construct', type='rich',
                                                                    description='Constructing...')
                                construct_msg = await ctx.send(embed=constructing)


                                if res_result:
                                    name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                                    # Check if user has enough wood or concrete
                                    if (wood >= ammo_wood)and (concrete >= ammo_concrete)and (steel >= ammo_steel):

                                        # If user has enough wood or concrete then it proceeds normally.
                                        # Update the resources table
                                        cursor.execute('''
                                            UPDATE resources SET
                                            wood = wood - ?,
                                            concrete = concrete - ?,
                                            steel = steel - ?
                                            WHERE name = ?
                                        ''', (ammo_wood, ammo_concrete, ammo_steel, nation_name))

                                        cursor.execute('UPDATE infra SET ammo_factory = ammo_factory + ? WHERE name = ?', (ammo_amt, nation_name))

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

                    case "concretefactory":
                        concrete_amt = amount
                        concrete_wood = concrete_amt * 2
                        concrete_concrete = concrete_amt * 6
                        concrete_steel = concrete_amt * 2
                        embed = discord.Embed(colour=0xdd7878, title="Construct: Concrete Factory", type='rich',
                                                                description=f'{concrete_amt:,} will be constructed.{new_line}{new_line}'
                                                                            f'The basic houses will cost: {concrete_wood:,} Wood{new_line}'
                                                                            f'The basic houses will cost: {concrete_concrete:,} Concrete{new_line}'
                                                                            f'The basic houses will cost: {concrete_steel:,} Steel')
                        await ctx.send(embed=embed)

                        try:
                            await ctx.send("Would you like to proceed? Respond with y/n.")

                            def check(message):
                                return message.content.lower() in ['y', 'n'] 

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)


                            if response_message.content.lower() == 'y':
                                constructing = discord.Embed(colour=0xdd7878, title='Construct', type='rich',
                                                                    description='Constructing...')
                                construct_msg = await ctx.send(embed=constructing)


                                if res_result:
                                    name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                                    # Check if user has enough wood or concrete
                                    if (wood >= concrete_wood)and (concrete >= concrete_concrete) and (steel >= concrete_steel):

                                        # If user has enough wood and concrete then it proceeds normally.
                                        # Update the resources table
                                        cursor.execute('''
                                            UPDATE resources SET
                                            wood = wood - ?,
                                            concrete = concrete - ?,
                                            steel = steel - ?
                                            WHERE name = ?
                                        ''', (concrete_wood, concrete_concrete, concrete_steel, nation_name))

                                        cursor.execute('UPDATE infra SET concrete_factory = concrete_factory + ? WHERE name = ?', (concrete_amt, nation_name))

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

                    case "barrack" | "barracks":
                        barrack_amt = amount
                        barrack_concrete = barrack_amt * 2
                        barrack_steel = barrack_amt * 3
                        embed = discord.Embed(colour=0xdd7878, title="Construct: Barrack", type='rich',
                                                                description=f'{barrack_amt:,} will be constructed.{new_line}{new_line}'
                                                                            f'The basic houses will cost: {barrack_concrete:,} Concrete{new_line}'
                                                                            f'The basic houses will cost: {barrack_steel:,} Steel')
                        await ctx.send(embed=embed)

                        try:
                            await ctx.send("Would you like to proceed? Respond with y/n.")

                            def check(message):
                                return message.content.lower() in ['y', 'n'] 

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)


                            if response_message.content.lower() == 'y':
                                constructing = discord.Embed(colour=0xdd7878, title='Construct', type='rich',
                                                                    description='Constructing...')
                                construct_msg = await ctx.send(embed=constructing)


                                if res_result:
                                    name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                                    # Check if user has enough wood or concrete
                                    if (concrete >= barrack_concrete) and (steel >= barrack_steel):

                                        # If user has enough wood and concrete then it proceeds normally.
                                        # Update the resources table
                                        cursor.execute('''
                                            UPDATE resources SET
                                            concrete = concrete - ?,
                                            steel = steel - ?
                                            WHERE name = ?
                                        ''', (barrack_concrete, barrack_steel, nation_name))

                                        cursor.execute('UPDATE user_mil SET barrack = barrack + ? WHERE name = ?', (barrack_amt, nation_name))

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

                    case "militaryfactory" | "milfactory":
                        milfactory_amt = amount
                        milfactory_concrete = milfactory_amt * 5
                        milfactory_steel = milfactory_amt * 2.75
                        embed = discord.Embed(colour=0xdd7878, title="Construct: Barrack", type='rich',
                                                                description=f'{milfactory_amt:,} will be constructed.{new_line}{new_line}'
                                                                            f'The basic houses will cost: {milfactory_concrete:,} Concrete{new_line}'
                                                                            f'The basic houses will cost: {milfactory_steel:,} Steel')
                        await ctx.send(embed=embed)

                        try:
                            await ctx.send("Would you like to proceed? Respond with y/n.")

                            def check(message):
                                return message.content.lower() in ['y', 'n'] 

                            response_message = await self.bot.wait_for('message', timeout=30, check=check)


                            if response_message.content.lower() == 'y':
                                constructing = discord.Embed(colour=0xdd7878, title='Construct', type='rich',
                                                                    description='Constructing...')
                                construct_msg = await ctx.send(embed=constructing)


                                if res_result:
                                    name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result

                                    # Check if user has enough wood or concrete
                                    if (concrete >= milfactory_concrete) and (steel >= milfactory_steel):

                                        # If user has enough wood and concrete then it proceeds normally.
                                        # Update the resources table
                                        cursor.execute('''
                                            UPDATE resources SET
                                            concrete = concrete - ?,
                                            steel = steel - ?
                                            WHERE name = ?
                                        ''', (milfactory_concrete, milfactory_steel, nation_name))

                                        cursor.execute('UPDATE infra SET militaryfactory = militaryfactory + ? WHERE name = ?', (milfactory_amt, nation_name))

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


async def setup(bot):
    await bot.add_cog(Construct(bot))