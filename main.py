import discord
from discord.ext import commands
import mysql.connector
import hashlib

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="username",
        password="pass",
        database="discord_bot",
        auth_plugin='mysql_native_password',
    )
    mycursor = mydb.cursor()
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")
    exit(1)

def generate_auth_token(server_id):
    try:
        server_id_bytes = str(server_id).encode('utf-8')
        sha256_hash = hashlib.sha256(server_id_bytes)
        auth_token = sha256_hash.hexdigest()
        return auth_token
    except Exception as e:
        print(f"Error generating auth token: {e}")

@bot.command()
async def hello(ctx):
    try:
        auth_token = generate_auth_token(ctx.guild.id)
        mycursor.execute("SELECT name FROM auth WHERE token = %s", (auth_token,))
        result = mycursor.fetchone()

        if result is None:
            await ctx.send("Please authenticate the bot by typing !auth ")
        else:
            await ctx.send(f"Hello World {ctx.guild.name}")

    except mysql.connector.Error as err:
        print(f"Error executing SQL query: {err}")
        await ctx.send("An error occurred while processing the command.")

@bot.command()
async def auth(ctx):
    try:
        server_name = ctx.guild.name
        token = generate_auth_token(ctx.guild.id)
        mycursor.execute("INSERT INTO auth (name, token) VALUES (%s, %s)", (server_name, token))
        mydb.commit()
        await ctx.send(f"The bot is authenticated for {server_name}")

    except mysql.connector.Error as err:
        print(f"Error executing SQL query: {err}")
        await ctx.send("An error occurred while processing the command.")

# Run the bot with the token
bot.run("your_token")
