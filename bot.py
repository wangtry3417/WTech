import discord
from discord import option
import psycopg2
import re,os
from requests import get

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

        # 處理 CREATE TABLE
        if "create table" in query:
            parts = query.split("->")
            if len(parts) == 2:
                table_name = parts[0].split()[2].strip()
                fields_str = parts[1].strip()
                pattern = r"\('([^']+)',\s*'([^']+)'\)"
                fields = re.findall(pattern, fields_str)

                if not fields:
                    await ctx.respond("字段格式不正確，應該是元組列表。")
                    return

                field_definitions = ", ".join([f"{field} {field_type}" for field, field_type in fields])
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({field_definitions})")
                conn.commit()
                await ctx.respond(f"資料表 '{table_name}' 已經建立。")

        # 處理 INSERT
        elif "insert" in query:
            parts = query.split("->")
            if len(parts) == 3:
                table_name = parts[0].split()[1].strip()
                fields = parts[1].strip().split(",")
                values = parts[2].strip().split(",")

                fields = [field.strip() for field in fields]
                values = [value.strip().strip("'") for value in values]

                cursor.execute(f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({', '.join(['%s' for _ in values])})", values)
                conn.commit()
                await ctx.respond("記錄已插入成功")

        # 處理 SELECT
        elif "using" in query:
            parts = query.split(",")
            if len(parts) == 2:
                table_name = parts[0].split()[1].strip()
                select_part = parts[1].strip()

                # 解析 SELECT 部分
                select_parts = select_part.split("where")
                fields_part = select_parts[0].replace("select", "").strip()
                condition_part = select_parts[1].strip() if len(select_parts) > 1 else None

                # 構建查詢
                if fields_part == "*":
                    cursor.execute(f"SELECT * FROM {table_name}")
                else:
                    fields = [field.strip() for field in fields_part.split(",")]
                    cursor.execute(f"SELECT {', '.join(fields)} FROM {table_name}")

                # 添加條件
                if condition_part:
                    cursor.execute(f"SELECT {', '.join(fields)} FROM {table_name} WHERE {condition_part}")

                # 獲取查詢結果
                results = cursor.fetchall()

                # 格式化結果
                output = [{fields[i]: row[i] for i in range(len(fields))} for row in results] if fields_part != "*" else [{column.name: row[i] for i, column in enumerate(cursor.description)} for row in results]

                await ctx.respond(output)

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
