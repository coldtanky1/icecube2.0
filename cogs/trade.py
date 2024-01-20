import sqlite3
import asyncio
import discord
from discord.ext import commands
from discord.utils import get


print("Loading trade cog...")
new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = sqlite3.connect('player_info.db')
cursor = conn.cursor()


class Trade(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def trade(self, ctx, target_user: discord.User, material: str, amount: int):
        # Access the user who invoked the command
        sender_id = ctx.author.id
        receiver_id = target_user.id
        material = material.lower()

        # fetch sender nation_name
        cursor.execute('SELECT nation_name FROM user_info WHERE user_id = ?', (sender_id,))
        sender_result = cursor.fetchone()

        # fetch target user nation_name
        cursor.execute('SELECT nation_name FROM user_info WHERE user_id = ?', (receiver_id,))
        target_result = cursor.fetchone()

        if sender_result and target_result:
            sender_nation_name = sender_result[0]
            target_nation_name = target_result[0]

            # Check if the user is not the sender
            if receiver_id != sender_id:

                match material:
                    case "wood":
                        # fetch sender's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (sender_nation_name,))
                        sender_res_result = cursor.fetchone()

                        # fetch target user's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (target_nation_name,))
                        target_res_result = cursor.fetchone()

                        if sender_res_result and target_res_result:
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = sender_res_result
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = target_res_result

                            # Check if user has enough of resource specified.
                            if amount > wood:
                                await ctx.send("You do not have enough of the specified resource.")
                                return

                            # Update sender's resources
                            cursor.execute('UPDATE resources SET wood = wood - ? WHERE name = ?', (amount, sender_nation_name))
                            conn.commit()

                            # Update target user's resources
                            cursor.execute('UPDATE resources SET wood = wood + ? WHERE name = ?', (amount, target_nation_name))
                            conn.commit()

                            await ctx.send("Trade completed!")
                    case "coal":
                        # fetch sender's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (sender_nation_name,))
                        sender_res_result = cursor.fetchone()

                        # fetch target user's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (target_nation_name,))
                        target_res_result = cursor.fetchone()

                        if sender_res_result and target_res_result:
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = sender_res_result
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = target_res_result

                            # Check if user has enough of resource specified.
                            if amount > coal:
                                await ctx.send("You do not have enough of the specified resource.")
                                return

                            # Update sender's resources
                            cursor.execute('UPDATE resources SET coal = coal - ? WHERE name = ?', (amount, sender_nation_name))
                            conn.commit()

                            # Update target user's resources
                            cursor.execute('UPDATE resources SET coal = coal + ? WHERE name = ?', (amount, target_nation_name))
                            conn.commit()

                            await ctx.send("Trade completed!")
                    case "iron":
                        # fetch sender's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (sender_nation_name,))
                        sender_res_result = cursor.fetchone()

                        # fetch target user's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (target_nation_name,))
                        target_res_result = cursor.fetchone()

                        if sender_res_result and target_res_result:
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = sender_res_result
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = target_res_result

                            # Check if user has enough of resource specified.
                            if amount > iron:
                                await ctx.send("You do not have enough of the specified resource.")
                                return

                            # Update sender's resources
                            cursor.execute('UPDATE resources SET iron = iron - ? WHERE name = ?', (amount, sender_nation_name))
                            conn.commit()

                            # Update target user's resources
                            cursor.execute('UPDATE resources SET iron = iron + ? WHERE name = ?', (amount, target_nation_name))
                            conn.commit()

                            await ctx.send("Trade completed!")
                    case "lead":
                        # fetch sender's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (sender_nation_name,))
                        sender_res_result = cursor.fetchone()

                        # fetch target user's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (target_nation_name,))
                        target_res_result = cursor.fetchone()

                        if sender_res_result and target_res_result:
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = sender_res_result
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = target_res_result

                            # Check if user has enough of resource specified.
                            if amount > lead:
                                await ctx.send("You do not have enough of the specified resource.")
                                return

                            # Update sender's resources
                            cursor.execute('UPDATE resources SET lead = lead - ? WHERE name = ?', (amount, sender_nation_name))
                            conn.commit()

                            # Update target user's resources
                            cursor.execute('UPDATE resources SET lead = lead + ? WHERE name = ?', (amount, target_nation_name))
                            conn.commit()

                            await ctx.send("Trade completed!")
                    case "bauxite":
                        # fetch sender's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (sender_nation_name,))
                        sender_res_result = cursor.fetchone()

                        # fetch target user's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (target_nation_name,))
                        target_res_result = cursor.fetchone()

                        if sender_res_result and target_res_result:
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = sender_res_result
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = target_res_result

                            # Check if user has enough of resource specified.
                            if amount > bauxite:
                                await ctx.send("You do not have enough of the specified resource.")
                                return

                            # Update sender's resources
                            cursor.execute('UPDATE resources SET bauxite = bauxite - ? WHERE name = ?', (amount, sender_nation_name))
                            conn.commit()

                            # Update target user's resources
                            cursor.execute('UPDATE resources SET bauxite = bauxite + ? WHERE name = ?', (amount, target_nation_name))
                            conn.commit()

                            await ctx.send("Trade completed!")
                    case "oil":
                        # fetch sender's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (sender_nation_name,))
                        sender_res_result = cursor.fetchone()

                        # fetch target user's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (target_nation_name,))
                        target_res_result = cursor.fetchone()

                        if sender_res_result and target_res_result:
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = sender_res_result
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = target_res_result

                            # Check if user has enough of resource specified.
                            if amount > oil:
                                await ctx.send("You do not have enough of the specified resource.")
                                return

                            # Update sender's resources
                            cursor.execute('UPDATE resources SET oil = oil - ? WHERE name = ?', (amount, sender_nation_name))
                            conn.commit()

                            # Update target user's resources
                            cursor.execute('UPDATE resources SET oil = oil + ? WHERE name = ?', (amount, target_nation_name))
                            conn.commit()

                            await ctx.send("Trade completed!")
                    case "uranium":
                        # fetch sender's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (sender_nation_name,))
                        sender_res_result = cursor.fetchone()

                        # fetch target user's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (target_nation_name,))
                        target_res_result = cursor.fetchone()

                        if sender_res_result and target_res_result:
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = sender_res_result
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = target_res_result

                            # Check if user has enough of resource specified.
                            if amount > uranium:
                                await ctx.send("You do not have enough of the specified resource.")
                                return

                            # Update sender's resources
                            cursor.execute('UPDATE resources SET uranium = uranium - ? WHERE name = ?', (amount, sender_nation_name))
                            conn.commit()

                            # Update target user's resources
                            cursor.execute('UPDATE resources SET uranium = uranium + ? WHERE name = ?', (amount, target_nation_name))
                            conn.commit()

                            await ctx.send("Trade completed!")
                    case "food":
                        # fetch sender's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (sender_nation_name,))
                        sender_res_result = cursor.fetchone()

                        # fetch target user's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (target_nation_name,))
                        target_res_result = cursor.fetchone()

                        if sender_res_result and target_res_result:
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = sender_res_result
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = target_res_result

                            # Check if user has enough of resource specified.
                            if amount > food:
                                await ctx.send("You do not have enough of the specified resource.")
                                return

                            # Update sender's resources
                            cursor.execute('UPDATE resources SET food = food - ? WHERE name = ?', (amount, sender_nation_name))
                            conn.commit()

                            # Update target user's resources
                            cursor.execute('UPDATE resources SET food = food + ? WHERE name = ?', (amount, target_nation_name))
                            conn.commit()

                            await ctx.send("Trade completed!")
                    case "steel":
                        # fetch sender's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (sender_nation_name,))
                        sender_res_result = cursor.fetchone()

                        # fetch target user's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (target_nation_name,))
                        target_res_result = cursor.fetchone()

                        if sender_res_result and target_res_result:
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = sender_res_result
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = target_res_result

                            # Check if user has enough of resource specified.
                            if amount > steel:
                                await ctx.send("You do not have enough of the specified resource.")
                                return

                            # Update sender's resources
                            cursor.execute('UPDATE resources SET steel = steel - ? WHERE name = ?', (amount, sender_nation_name))
                            conn.commit()

                            # Update target user's resources
                            cursor.execute('UPDATE resources SET steel = steel + ? WHERE name = ?', (amount, target_nation_name))
                            conn.commit()

                            await ctx.send("Trade completed!")
                    case "aluminium":
                        # fetch sender's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (sender_nation_name,))
                        sender_res_result = cursor.fetchone()

                        # fetch target user's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (target_nation_name,))
                        target_res_result = cursor.fetchone()

                        if sender_res_result and target_res_result:
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = sender_res_result
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = target_res_result

                            # Check if user has enough of resource specified.
                            if amount > aluminium:
                                await ctx.send("You do not have enough of the specified resource.")
                                return

                            # Update sender's resources
                            cursor.execute('UPDATE resources SET aluminium = aluminium - ? WHERE name = ?', (amount, sender_nation_name))
                            conn.commit()

                            # Update target user's resources
                            cursor.execute('UPDATE resources SET aluminium = aluminium + ? WHERE name = ?', (amount, target_nation_name))
                            conn.commit()

                            await ctx.send("Trade completed!")
                    case "gasoline":
                        # fetch sender's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (sender_nation_name,))
                        sender_res_result = cursor.fetchone()

                        # fetch target user's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (target_nation_name,))
                        target_res_result = cursor.fetchone()

                        if sender_res_result and target_res_result:
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = sender_res_result
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = target_res_result

                            # Check if user has enough of resource specified.
                            if amount > gasoline:
                                await ctx.send("You do not have enough of the specified resource.")
                                return

                            # Update sender's resources
                            cursor.execute('UPDATE resources SET gasoline = gasoline - ? WHERE name = ?', (amount, sender_nation_name))
                            conn.commit()

                            # Update target user's resources
                            cursor.execute('UPDATE resources SET gasoline = gasoline + ? WHERE name = ?', (amount, target_nation_name))
                            conn.commit()

                            await ctx.send("Trade completed!")
                    case "ammo":
                        # fetch sender's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (sender_nation_name,))
                        sender_res_result = cursor.fetchone()

                        # fetch target user's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (target_nation_name,))
                        target_res_result = cursor.fetchone()

                        if sender_res_result and target_res_result:
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = sender_res_result
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = target_res_result

                            # Check if user has enough of resource specified.
                            if amount > ammo:
                                await ctx.send("You do not have enough of the specified resource.")
                                return

                            # Update sender's resources
                            cursor.execute('UPDATE resources SET ammo = ammo - ? WHERE name = ?', (amount, sender_nation_name))
                            conn.commit()

                            # Update target user's resources
                            cursor.execute('UPDATE resources SET ammo = ammo + ? WHERE name = ?', (amount, target_nation_name))
                            conn.commit()

                            await ctx.send("Trade completed!")
                    case "concrete":
                        # fetch sender's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (sender_nation_name,))
                        sender_res_result = cursor.fetchone()

                        # fetch target user's resources
                        cursor.execute(
                            'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                            (target_nation_name,))
                        target_res_result = cursor.fetchone()

                        if sender_res_result and target_res_result:
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = sender_res_result
                            name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = target_res_result

                            # Check if user has enough of resource specified.
                            if amount > concrete:
                                await ctx.send("You do not have enough of the specified resource.")
                                return

                            # Update sender's resources
                            cursor.execute('UPDATE resources SET concrete = concrete - ? WHERE name = ?', (amount, sender_nation_name))
                            conn.commit()

                            # Update target user's resources
                            cursor.execute('UPDATE resources SET concrete = concrete + ? WHERE name = ?', (amount, target_nation_name))
                            conn.commit()

                            await ctx.send("Trade completed!")
                        else:
                            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                                  description=f'Cannot find stats.')
                            await ctx.send(embed=embed)
                            return
            else:
                await ctx.send("You can't trade with yourself!")
                return
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)
            return

async def setup(bot):
    await bot.add_cog(Trade(bot))