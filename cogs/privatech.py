import asyncio
import discord
from discord.ext import commands
from discord.utils import get

new_line = '\n'

class Private(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Private Channel Command
    @commands.command()
    async def private(self, ctx):
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
            category = self.bot.get_channel()  # Private channel category DON'T FORGET TO INSERT THE ID OF THE CATEGORY YOU WANT THE PRIVATE CHANNELS TO BE IN
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


async def setup(bot):
    await bot.add_cog(Private(bot))