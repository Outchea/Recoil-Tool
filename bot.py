
import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from flask import Flask, request, jsonify
import threading, json, os, random, string
from datetime import datetime

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN environment variable not set.")

GUILD_ID = 1399546963267031120
PRO_ROLE_ID = 1399816671841222846
PLUS_ROLE_ID = 1399816586055122944
BETA_ROLE_ID = 1399842324770721934
ADMIN_ID = 1185849692395929611

KEY_FILE = "keys.json"
LOG_FILE = "key_log.txt"

app = Flask(__name__)

def load_keys():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_keys(keys):
    with open(KEY_FILE, "w") as f:
        json.dump(keys, f, indent=4)

def generate_key(length=16):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@app.route("/verify", methods=["GET"])
def verify_key():
    key = request.args.get("key")
    discord_id = request.args.get("discord_id")
    edition = request.args.get("edition")
    keys = load_keys()
    if key in keys:
        data = keys[key]
        if data["discord_id"] == discord_id and data["edition"] == edition:
            return jsonify({"status": "valid"})
    return jsonify({"status": "invalid"})

def run_flask():
    app.run(host="0.0.0.0", port=5000)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

@slash_command(guild_ids=[GUILD_ID], description="Generate a license key for a user.")
async def genkey(ctx: discord.ApplicationContext, user: Option(discord.User, "User to bind the key to")):
    member = ctx.guild.get_member(ctx.user.id)
    if not member:
        await ctx.respond("❌ Could not identify your roles.", ephemeral=True)
        return

    roles = [role.id for role in member.roles]
    if PRO_ROLE_ID in roles:
        edition = "pro"
    elif PLUS_ROLE_ID in roles:
        edition = "plus"
    elif BETA_ROLE_ID in roles:
        edition = "beta"
    else:
        await ctx.respond("❌ You don't have permission to generate keys.", ephemeral=True)
        return

    key = generate_key()
    keys = load_keys()
    keys[key] = {"discord_id": str(user.id), "edition": edition}
    save_keys(keys)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} | {ctx.user} → {user} ({edition}) : {key}\n")

    await ctx.respond(f"✅ Generated `{edition.upper()}` key `{key}` for {user.mention}.", ephemeral=True)

@slash_command(guild_ids=[GUILD_ID], description="List all license keys (admin only).")
async def listkeys(ctx: discord.ApplicationContext):
    if ctx.user.id != ADMIN_ID:
        await ctx.respond("❌ You are not authorized to view keys.", ephemeral=True)
        return

    keys = load_keys()
    if not keys:
        await ctx.respond("📭 No license keys found.", ephemeral=True)
        return

    lines = [f"`{k}` → {v['discord_id']} ({v['edition']})" for k, v in keys.items()]
    chunks = [lines[i:i+20] for i in range(0, len(lines), 20)]

    await ctx.respond("📋 Listing keys...", ephemeral=True)
    for chunk in chunks:
        await ctx.send("\n".join(chunk), ephemeral=True)

@slash_command(guild_ids=[GUILD_ID], description="Revoke a license key (admin only).")
async def revokekey(ctx: discord.ApplicationContext, key: Option(str, "The license key to revoke")):
    if ctx.user.id != ADMIN_ID:
        await ctx.respond("❌ You are not authorized to revoke keys.", ephemeral=True)
        return

    keys = load_keys()
    if key in keys:
        del keys[key]
        save_keys(keys)
        await ctx.respond(f"✅ Key `{key}` has been revoked.", ephemeral=True)
    else:
        await ctx.respond("❌ Key not found.", ephemeral=True)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    bot.run(TOKEN)
