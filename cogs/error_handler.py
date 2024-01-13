import discord
from discord.ext import commands
from discord.utils import get


debug = False
new_line = '\n'

def dev_check(usid):
    return usid == 837257162223910912 or usid == 669517694751604738


class Errorhandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        global debug
        if debug is False:   # Checks if bot is in debug mode
            if hasattr(ctx.command, 'on_error'):
                return
            error = getattr(error, 'original', error)
            if isinstance(error, commands.CommandNotFound):
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description="Command not found.")
                embed.set_footer(text="Check the help command")
                await ctx.send(embed=embed)
            elif isinstance(error, commands.CommandOnCooldown):
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description="**Still on cooldown**, please try again in {:.2f}s".format(error.retry_after))
                embed.set_footer(text="Patience, boy!")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description="An unspecified error has occurred.")
                embed.set_footer(text="Ping a dev so they can look into it")
                await ctx.send(embed=embed)
        else:
            print(error)

    @commands.command()   # Debug mode status
    async def debug_status(self, ctx):
        if dev_check(ctx.author.id):
            global debug
            await ctx.send(f'Debug Status: {debug}')
        else:
            print(f'{ctx.author} attempted to enable debug')
            await ctx.send(f'Permission denied: You are not a developer.')

    @commands.command()   # Debug mode switcher
    async def debug_mode(self, ctx):
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

async def setup(bot):
    await bot.add_cog(Errorhandler(bot))