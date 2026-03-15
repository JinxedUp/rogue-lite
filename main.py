import discord
from discord.ext import commands
from colorama import Fore, Style, init
import json
import os
import random
import string
import sys

init(autoreset=True)
from datetime import datetime
START_TIME = datetime.utcnow()

# ── config ─────────────────────────────────────────────────────────────────────

def load_config():
    if not os.path.exists("config.json"):
        print(f"\n  {Fore.RED}{Style.BRIGHT}[!]{Style.RESET_ALL} {Fore.WHITE}config.json not found. create it first.\n")
        sys.exit(1)
    try:
        with open("config.json", "r") as f:
            cfg = json.load(f)
    except json.JSONDecodeError:
        print(f"\n  {Fore.RED}{Style.BRIGHT}[!]{Style.RESET_ALL} {Fore.WHITE}config.json is malformed. check your json syntax.\n")
        sys.exit(1)

    token = cfg.get("token", "").strip()
    prefix = cfg.get("prefix", ".").strip() or "."

    if not token or token == "YOUR_TOKEN_HERE":
        print(f"\n  {Fore.RED}{Style.BRIGHT}[!]{Style.RESET_ALL} {Fore.WHITE}no token set in config.json. add your token and try again.\n")
        sys.exit(1)

    return token, prefix

TOKEN, PREFIX = load_config()

# ── client ─────────────────────────────────────────────────────────────────────

intents = discord.Intents.default()
intents.messages = True

client = commands.Bot(
    command_prefix=PREFIX,
    self_bot=True,
    help_command=None,
    intents=intents,
)

PROMO = f"-# buy full version of rogue from https://discord.gg/6nfxXzsZxt"

# ── helpers ────────────────────────────────────────────────────────────────────

def log_error(label, err):
    print(
        f"  {Fore.RED}{Style.BRIGHT}[err]{Style.RESET_ALL} "
        f"{Fore.YELLOW}{label}{Style.RESET_ALL} "
        f"{Fore.WHITE}{Style.DIM}{err}{Style.RESET_ALL}"
    )

def log_cmd(name):
    print(
        f"  {Fore.MAGENTA}{Style.BRIGHT}[cmd]{Style.RESET_ALL} "
        f"{Fore.CYAN}{PREFIX}{name}{Style.RESET_ALL}"
    )

def fake_nitro_link():
    code = "".join(random.choices(string.ascii_letters + string.digits, k=16))
    return f"https://discord.gift/{code}"

# ── decorator ──────────────────────────────────────────────────────────────────

def rogue(func=None, *, name=None):
    if func is not None:
        if func.__name__ == "on_ready":
            return client.event(func)
        if func.__name__ == "on_command_error":
            return client.event(func)
        return client.command(name=name or func.__name__)(func)
    def wrapper(f):
        if f.__name__ in ("on_ready", "on_command_error"):
            return client.event(f)
        return client.command(name=name or f.__name__)(f)
    return wrapper

# ── banner ─────────────────────────────────────────────────────────────────────

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    sys.stdout.write("\033]0;rogue lite — buy full version @ discord.gg/6nfxXzsZxt\007")
    sys.stdout.flush()
    r = Fore.RED
    m = Fore.MAGENTA
    c = Fore.CYAN
    w = Fore.WHITE
    d = Style.DIM
    b = Style.BRIGHT
    rs = Style.RESET_ALL

    lines = [
        f"{b}{r}                                                                                                  ",
        f"{b}{r}▄▄▄▄   ▄▄▄   ▄▄▄▄ ▄▄ ▄▄ ▄▄▄▄▄    {m}▄▄▄▄ ▄▄▄▄▄ ▄▄    ▄▄▄▄▄ ▄▄▄▄   ▄▄▄ ▄▄▄▄▄▄   ▄▄    ▄▄ ▄▄▄▄▄▄ ▄▄▄▄▄ ",
        f"{b}{r}██▄█▄ ██▀██ ██ ▄▄ ██ ██ ██▄▄    {m}███▄▄ ██▄▄  ██    ██▄▄  ██▄██ ██▀██  ██     ██    ██   ██   ██▄▄  ",
        f"{b}{r}██ ██ ▀███▀ ▀███▀ ▀███▀ ██▄▄▄   {m}▄▄██▀ ██▄▄▄ ██▄▄▄ ██    ██▄█▀ ▀███▀  ██     ██▄▄▄ ██   ██   ██▄▄▄ ",
        f"                                                                                                  {rs}",
    ]
    for line in lines:
        print(line)

    print()
    print(f"  {b}{m}made by {r}jinx{rs}    {d}{w}discord.gg/6nfxXzsZxt{rs}")
    print(f"  {d}{c}buy full version of rogue  »  {b}{w}https://discord.gg/6nfxXzsZxt{rs}")
    print()
    print(f"  {d}{w}prefix set to {b}{Fore.CYAN}{PREFIX}{rs}    {d}{w}loading...{rs}")
    print(f"  {d}{w}{'─' * 70}{rs}")
    print()

banner()

# ── events ─────────────────────────────────────────────────────────────────────

@rogue
async def on_ready():
    import asyncio
    print(
        f"  {Fore.GREEN}{Style.BRIGHT}[+]{Style.RESET_ALL} "
        f"logged in as {Fore.CYAN}{client.user}{Style.RESET_ALL} "
        f"({Fore.MAGENTA}{client.user.id}{Style.RESET_ALL})"
    )
    print(f"  {Style.DIM}{Fore.WHITE}{'─' * 70}{Style.RESET_ALL}\n")

    warnings = [
        "token stored in plaintext — upgrade to rogue for encrypted token storage",
        "no rate limit protection detected — commands may trigger discord flags",
        "selfbot activity is unmasked — rogue includes built-in request spoofing",
        "command locked — buy rogue for 400+ commands",
        "running on demo mode. no gui, no safety, no QoL, no full commands",
    ]

    for w in warnings:
        await asyncio.sleep(0.4)
        print(
            f"  {Fore.YELLOW}{Style.BRIGHT}⚠ WARNING:{Style.RESET_ALL} "
            f"{Fore.WHITE}{Style.DIM}{w}{Style.RESET_ALL}"
        )

    await asyncio.sleep(0.4)
    print(f"\n  {Fore.RED}{Style.BRIGHT}→{Style.RESET_ALL} {Fore.WHITE}get the full version at {Fore.CYAN}{Style.BRIGHT}discord.gg/6nfxXzsZxt{Style.RESET_ALL}\n")

@rogue
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        log_error(ctx.command.name, f"missing argument: {error.param.name}")
        try:
            await ctx.message.delete()
        except Exception:
            pass
        await ctx.send(f"⚠️ missing argument: `{error.param.name}`\n{PROMO}")
        return
    if isinstance(error, commands.BadArgument):
        log_error(ctx.command.name, f"bad argument: {error}")
        try:
            await ctx.message.delete()
        except Exception:
            pass
        await ctx.send(f"⚠️ bad argument — check what you typed.\n{PROMO}")
        return
    if isinstance(error, commands.CommandInvokeError):
        log_error(ctx.command.name if ctx.command else "unknown", error.original)
        return
    log_error(ctx.command.name if ctx.command else "unknown", error)

# ── commands ───────────────────────────────────────────────────────────────────

@rogue
async def ping(ctx):
    log_cmd("ping")
    await ctx.message.delete()
    await ctx.send(f"🏓 Pong! Latency: **{round(client.latency * 1000)}ms**\n{PROMO}")

@rogue
async def info(ctx):
    log_cmd("info")
    await ctx.message.delete()
    delta = datetime.utcnow() - START_TIME
    h, rem = divmod(int(delta.total_seconds()), 3600)
    m, s = divmod(rem, 60)
    uptime = f"{h}h {m}m {s}s"
    await ctx.send(
        f"ℹ️ **Rogue Selfbot**\n"
        f"Prefix: `{PREFIX}`\n"
        f"Commands: `{len(client.commands)}`\n"
        f"Uptime: `{uptime}`\n"
        f"Latency: `{round(client.latency * 1000)}ms`\n"
        f"Version: `1.0 (demo)`\n"
        f"{PROMO}"
    )

@rogue
async def help(ctx):
    log_cmd("help")
    await ctx.message.delete()
    cmds = [
        f"{PREFIX}ping", f"{PREFIX}info", f"{PREFIX}help", f"{PREFIX}avatar",
        f"{PREFIX}say", f"{PREFIX}serverinfo", f"{PREFIX}userinfo",
        f"{PREFIX}nitro", f"{PREFIX}aesthetic", f"{PREFIX}mock"
    ]
    cmd_list = "\n".join(f"• `{c}`" for c in cmds)
    await ctx.send(f"📋 **Rogue Commands (demo)**\n{cmd_list}\n{PROMO}")

@rogue
async def avatar(ctx, user: discord.User = None):
    log_cmd("avatar")
    await ctx.message.delete()
    target = user or ctx.author
    url = str(target.avatar_url)
    await ctx.send(f"🖼️ **{target.name}'s avatar**\n{url}\n{PROMO}")

@rogue
async def say(ctx, *, text: str = None):
    log_cmd("say")
    await ctx.message.delete()
    if not text:
        await ctx.send(f"⚠️ provide some text to say.\n{PROMO}")
        return
    await ctx.send(f"{text}\n{PROMO}")

@rogue
async def serverinfo(ctx):
    log_cmd("serverinfo")
    await ctx.message.delete()
    guild = ctx.guild
    if not guild:
        await ctx.send(f"⚠️ this command only works in a server.\n{PROMO}")
        return
    owner = str(guild.owner) if guild.owner else "unknown"
    created = guild.created_at.strftime("%d %b %Y")
    await ctx.send(
        f"🏠 **{guild.name}**\n"
        f"ID: `{guild.id}`\n"
        f"Owner: **{owner}**\n"
        f"Members: `{guild.member_count}`\n"
        f"Channels: `{len(guild.channels)}`\n"
        f"Roles: `{len(guild.roles)}`\n"
        f"Created: `{created}`\n"
        f"{PROMO}"
    )

@rogue
async def userinfo(ctx, user: discord.Member = None):
    log_cmd("userinfo")
    await ctx.message.delete()
    target = user or ctx.author
    created = target.created_at.strftime("%d %b %Y")
    joined = target.joined_at.strftime("%d %b %Y") if hasattr(target, "joined_at") and target.joined_at else "N/A"
    roles = [r.name for r in target.roles[1:]] if hasattr(target, "roles") else []
    roles_str = ", ".join(roles[-5:]) if roles else "none"
    await ctx.send(
        f"👤 **{target}**\n"
        f"ID: `{target.id}`\n"
        f"Created: `{created}`\n"
        f"Joined: `{joined}`\n"
        f"Top roles: `{roles_str}`\n"
        f"Bot: `{target.bot}`\n"
        f"{PROMO}"
    )

@rogue
async def nitro(ctx, amount: int = 1):
    log_cmd("nitro")
    await ctx.message.delete()
    if amount < 1 or amount > 5:
        await ctx.send(f"⚠️ amount must be between `1` and `5`.\n{PROMO}")
        return
    links = "\n".join(f"`{fake_nitro_link()}`" for _ in range(amount))
    await ctx.send(
        f"🎁 **Nitro Gift{'s' if amount > 1 else ''}** *(demo)*\n"
        f"{links}\n"
        f"{PROMO}"
    )

@rogue
async def aesthetic(ctx, *, text: str = None):
    log_cmd("aesthetic")
    await ctx.message.delete()
    if not text:
        await ctx.send(f"⚠️ provide some text.\n{PROMO}")
        return
    result = " ".join(chr(ord(c) + 0xFEE0) if c.isalnum() else c for c in text)
    await ctx.send(f"{result}\n{PROMO}")

@rogue
async def mock(ctx, *, text: str = None):
    log_cmd("mock")
    await ctx.message.delete()
    if not text:
        await ctx.send(f"⚠️ provide some text.\n{PROMO}")
        return
    mocked = "".join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(text))
    await ctx.send(f"{mocked}\n{PROMO}")

# ── run ────────────────────────────────────────────────────────────────────────

try:
    client.run(TOKEN, bot=False)
except discord.LoginFailure:
    print(f"\n  {Fore.RED}{Style.BRIGHT}[!]{Style.RESET_ALL} {Fore.WHITE}invalid token. check config.json and try again.\n")
    sys.exit(1)
except discord.HTTPException as e:
    print(f"\n  {Fore.RED}{Style.BRIGHT}[!]{Style.RESET_ALL} {Fore.WHITE}http error: {e}\n")
    sys.exit(1)
except KeyboardInterrupt:
    print(f"\n  {Fore.YELLOW}{Style.BRIGHT}[~]{Style.RESET_ALL} {Fore.WHITE}shutting down. bye.\n")
    sys.exit(0)
