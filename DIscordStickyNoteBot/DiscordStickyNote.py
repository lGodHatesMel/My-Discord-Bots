import discord
from discord.ext import commands

class StickyNoteBot(commands.Bot):
    def __init__(self, command_prefix='!'):
        super().__init__(command_prefix)
        self.sticky_notes = {}

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        channel = message.channel
        if channel.id in self.sticky_notes:
            sticky_msg = self.sticky_notes[channel.id]
            await sticky_msg.delete()
            await channel.send(sticky_msg)

        await self.process_commands(message)

    @commands.command()
    async def sticky(self, ctx, *, msg):
        channel = ctx.message.channel
        self.sticky_notes[channel.id] = msg
        await ctx.send(msg)

    @commands.command()
    async def removesticky(self, ctx):
        channel = ctx.message.channel
        if channel.id in self.sticky_notes:
            del self.sticky_notes[channel.id]
            await ctx.send("Sticky note has been removed.")
        else:
            await ctx.send("No sticky note found.")

    @commands.command()
    async def editsticky(self, ctx, *, msg):
        channel = ctx.message.channel
        if channel.id in self.sticky_notes:
            self.sticky_notes[channel.id] = msg
            await ctx.send("Sticky note has been edited.")
        else:
            await ctx.send("No sticky note found.")

    @commands.has_role('admin')
    async def checkstickies(self, ctx):
        if not self.sticky_notes:
            await ctx.send("No sticky notes found.")
            return

        response = "Sticky notes:\n"
        for channel_id, msg in self.sticky_notes.items():
            response += f"- Channel ID: {channel_id}, Message: {msg}\n"
        await ctx.send(response)

    @commands.has_role('admin')
    async def removestickybyid(self, ctx, channel_id: int):
        if channel_id in self.sticky_notes:
            del self.sticky_notes[channel_id]
            await ctx.send(f"Sticky note with ID {channel_id} has been removed.")
        else:
            await ctx.send(f"No sticky note found with ID {channel_id}.")


bot = StickyNoteBot()
bot.run('<DISCORD_BOT_TOKEN>')
