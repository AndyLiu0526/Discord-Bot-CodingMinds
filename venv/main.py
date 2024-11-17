from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from datetime import datetime, timedelta

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
ROBOTEVENTS_TOKEN: Final[str] = os.getenv("ROBOTEVENTS_TOKEN")

# Create intents
intents = discord.Intents.default()
intents.messages = True  # Enable message-related events
intents.guilds = True    # Enable guild-related events
intents.message_content = True  # Enable message content intent

# Set up the bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Store events in a dictionary (global scope)
events = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

    # Automatically create an event when the bot starts
    await create_event('AutoEvent', 2, 'This is an automatically created event.', 'Voice Channel')  # Creates an event named 'AutoEvent' in 2 hours

async def create_event(event_name: str, hours: int, description: str, location: str, ctx=None):
    """Create an event that users can join."""
    global events  # Ensure we are using the global events dictionary

    if event_name in events:
        print(f'Event "{event_name}" already exists.')
        if ctx:
            await ctx.send(f'Event "{event_name}" already exists.')
        return

    start_time = datetime.now() + timedelta(hours=hours)
    end_time = datetime.now() + timedelta(hours=hours)
    event_info = {
        'name': event_name,
        'start_time': start_time,
        'end_time': end_time,
        'description': description,
        'location': location,
        'participants': []
    }

    events[event_name] = event_info
    print(f"{event_name}")
    print(f"Start time: {start_time.strftime("%Y-%m-%d %H:%M:%S")}")
    print(f"End time: {end_time.strftime("%Y-%m-%d %H:%M:%S")}")
    print(f"{location}")
    print(f"{description}")
    if ctx:
        await ctx.send(f'"{event_name}" created from {start_time.strftime("%Y-%m-%d %H:%M:%S")} to {end_time.strftime("%Y-%m-%d %H:%M:%S")} at {description} has been added. \nLocation: {location}')

@bot.command()
async def join_event(ctx, event_name: str):
    """Join an existing event."""
    if event_name in events:
        if ctx.author.name not in events[event_name]['participants']:
            events[event_name]['participants'].append(ctx.author.name)
            await ctx.send(f'{ctx.author.name} joined the event "{event_name}".')
        else:
            await ctx.send(f'{ctx.author.name}, you have already joined "{event_name}".')
    else:
        await ctx.send(f'Event "{event_name}" does not exist.')

@bot.command()
async def event_info(ctx, event_name: str):
    """Get information about an event."""
    if event_name in events:
        event = events[event_name]
        participants = ', '.join(event['participants']) if event['participants'] else 'No participants yet.'
        await ctx.send(f'Event: {event["name"]}\nTime: {event["time"].strftime("%Y-%m-%d %H:%M:%S")}\nDescription: {event["description"]}\nLocation: {event["location"]}\nParticipants: {participants}')
    else:
        await ctx.send(f'Event "{event_name}" does not exist.')

@bot.command()
async def list_events(ctx):
    """List all events."""
    if events:
        event_list = '\n'.join([f'{event["name"]} - {event["time"].strftime("%Y-%m-%d %H:%M:%S")} - {event["description"]} - Location: {event["location"]}' for event in events.values()])
        await ctx.send(f'Events:\n{event_list}')
    else:
        await ctx.send('No events found.')

@bot.command()
async def create_event_cmd(ctx, event_name: str, hours: int, description: str, location: str):
    """Create a new event with a name, duration, description, and location."""
    await create_event(event_name, hours, description, location, ctx)


bot.run(TOKEN)
