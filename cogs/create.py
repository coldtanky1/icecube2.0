import sqlite3
import asyncio
import discord
from discord.ext import commands
from discord.utils import get

new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = sqlite3.connect('player_info.db')
cursor = conn.cursor()


class Create(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def create(self, ctx):
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
            nt_name = await self.bot.wait_for('message', check=msgchk, timeout=30.0)
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
        cursor.execute('INSERT INTO user_stats (name, nation_score, gdp, child, teen, adult, elder, balance) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                       (nat_name, 0, 0, 100000, 100000, 450000, 50000, 1000000))
        conn.commit()

        # add base mil stats to the user
        cursor.execute(
            'INSERT INTO user_mil (name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (nat_name, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        conn.commit()

        # Add base resources to the user
        cursor.execute(
            'INSERT INTO resources (name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (nat_name, 500, 300, 50, 50, 0, 50, 0, 10000, 50, 50, 100, 1000, 0))
        conn.commit()

        print(f"Successfully added stats to {user_id}({nat_name})")

        # Add base infra stats to the user
        cursor.execute(
            'INSERT INTO infra (name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
            (nat_name, 12500, 1000, 834, 0, 10, 100, 10, 10, 10, 10, 0, 2500, 0, 0, 0, 0,
             0,0))  # the values came from ice cube's game sheet so just use that as a reference
        conn.commit()

        print(f"Successfully added infra to {user_id}({nat_name})")

async def setup(bot):
    await bot.add_cog(Create(bot))