import discord
from discord import option
import sqlite3
import re,os
from requests import get

if not os.path.exists("main.db"):
  open("main.db","a").close()

# Discord Bot 設定
bot = discord.Bot()

# 資料庫連接
conn = sqlite3.connect('main.db')
cursor = conn.cursor()

# 創建基本的資料表
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER
)
''')
conn.commit()

@bot.slash_command(name="trydb", description="執行 tryDB 指令")
@option("query",description="查詢Query")
async def trydb(
    ctx:discord.ApplicationContext,
    query: str
):
    try:
        if "create table" in query:
            parts = query.split("->")
            if len(parts) == 2:
                table_name = parts[0].split()[2].strip()
                fields_str = parts[1].strip()

                pattern = r"\('([^']+)',\s*'([^']+)'\)"
                fields = re.findall(pattern, fields_str)

                if not fields:
                    await ctx.respond("字段格式不正確，應該是元組列表。", ephemeral=True)
                    return

                # 創建資料表
                field_definitions = ", ".join([f"{field} {field_type}" for field, field_type in fields])
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({field_definitions})")
                conn.commit()
                await ctx.respond(f"資料表 '{table_name}' 已經建立。", ephemeral=True)

        elif "insert" in query:
            parts = query.split("->")
            if len(parts) == 3:
                table_name = parts[0].split()[1].strip()
                fields = parts[1].strip().split(",")
                values = parts[2].strip().split(",")

                fields = [field.strip() for field in fields]
                values = [value.strip().strip("'") for value in values]

                # 插入資料
                cursor.execute(f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({', '.join(['?' for _ in values])})", values)
                conn.commit()
                await ctx.respond("記錄已插入成功", ephemeral=True)

    except Exception as e:
        await ctx.respond(f"錯誤: {str(e)}", ephemeral=True)

@bot.slash_command(name='捐錢',description='請支持WTech/WBank')
@option("user",description="WBank用戶名 (請確保已開啟paymode)")
@option("amount",description="金額 (最少是WTC$100)",min_value=10)
async def donate(ctx:discord.ApplicationContext,user:str,amount:int):
  res = get(url="https://sites.wtechhk.xyz/wbank/hash/transfer",headers={"username":user,"reviewer":"wbank","amount":str(amount)})
  try:
    if not res.json["Error-hint"]:
      await ctx.respond(res.json())
    else:
      await ctx.respond(res.json()["Error-hint"])
  except Exception as e:
    await ctx.respond(f"錯誤: {str(e)}")

# 啟動 Discord Bot
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

# 啟動 Bot
def run_bot():
  bot.run(os.environ.get('discordToken'))  # 替換為您的 Discord Bot Token
