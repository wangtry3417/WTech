import discord
from discord import option
import psycopg2
import re,os
from requests import get

if not os.path.exists("main.db"):
  open("main.db","a").close()

# Discord Bot 設定
bot = discord.Bot()

# 連接到 PostgreSQL 資料庫
def get_db_connection():
    return psycopg2.connect("postgres://default:Gd2MsST3QYWF@ep-hidden-salad-a1a7pob9.ap-southeast-1.aws.neon.tech:5432/verceldb?sslmode=require")

@bot.slash_command(name="trydb", description="執行 tryDB 指令")
@option("query", description="查詢Query")
async def trydb(
    ctx: discord.ApplicationContext,
    query: str
):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

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
                cursor.execute(f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({', '.join(['%s' for _ in values])})", values)
                conn.commit()
                await ctx.respond("記錄已插入成功", ephemeral=True)

        cursor.close()
        conn.close()

    except Exception as e:
        await ctx.respond(f"錯誤: {str(e)}", ephemeral=True)

@bot.slash_command(name='捐錢',description='請支持WTech/WBank')
@option("user",description="WBank用戶名 (請確保已開啟paymode)")
@option("amount",description="金額 (最少是WTC$100)",min_value=100)
async def donate(ctx:discord.ApplicationContext,user:str,amount:int):
  res = get(url="https://sites.wtechhk.xyz/wbank/hash/transfer",headers={"username":user,"reviewer":"wbank","amount":str(amount)})
  try:
    if "Error-hint" in res.json():
      if res.json()["Error-hint"] == "轉賬方尚未開啟支付模式":
        await ctx.respond("你尚未開啟支付模式，請登入WBank後，按我的->按設定開啟交易功能->確保值為true即可。")
      else:
        await ctx.respond(res.json()["Error-hint"])
    else:
      await ctx.respond(res.json())
  except Exception as e:
    await ctx.respond(f"錯誤: {str(e)}",ephemeral=True)

# 啟動 Discord Bot
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

# 啟動 Bot
def run_bot():
  bot.run(os.environ.get('discordToken'))  # 替換為您的 Discord Bot Token