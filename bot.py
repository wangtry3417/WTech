import discord
from discord import option
import psycopg2
import re,os
from requests import get

# Discord Bot 設定
bot = discord.Bot()

# 連接到 PostgreSQL 資料庫
def get_db_connection():
    return psycopg2.connect(str(os.environ.get("dataurl")))

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
            fields = [field.strip() for field in fields_part.split(",")]

            if fields_part == "*":
              cursor.execute(f"SELECT * FROM {table_name}")
            else:
              # 生成查詢語句
              query_str = f"SELECT {', '.join(fields)} FROM {table_name}"
              if condition_part:
                condition_part = condition_part.replace("‘", "'").replace("’", "'")
                query_str += f" WHERE {condition_part}"

              # 執行查詢
              cursor.execute(query_str)

            # 獲取查詢結果
            results = cursor.fetchall()

            # 格式化結果
            output = [{fields[i]: row[i] for i in range(len(fields))} for row in results]

            # 將輸出格式化為字符串
            output_str = "\n".join(str(o) for o in output)
            await ctx.respond(output_str)
        # 處理 UPDATE
        if "using" in query:
            parts = query.split("->")
            if len(parts) == 2:
                table_name = parts[0].split()[1].strip()
                action_part = parts[1].strip()

                if "with" in action_part:
                    set_part, condition_part = action_part.split("with")
                    set_field, set_value = set_part.split("=")
                    set_field = set_field.strip()
                    set_value = set_value.strip().strip("'")
                    condition_field, condition_value = condition_part.split("=")  # 改為單等號
                    condition_field = condition_field.strip()
                    condition_value = condition_value.strip().strip("'")

                    # 更新操作
                    update_query = f"UPDATE {table_name} SET {set_field} = %s WHERE {condition_field} = %s"
                    cursor.execute(update_query, (set_value, condition_value))
                    conn.commit()

                    if cursor.rowcount > 0:
                        await ctx.respond(f"資料表 '{table_name}' 中滿足條件的記錄已被更新。")
                    else:
                        await ctx.respond("沒有找到滿足條件的記錄。")

        cursor.close()
        conn.close()

    except Exception as e:
        await ctx.respond(f"錯誤: {str(e)}", ephemeral=True)

@bot.slash_command(name='捐錢',description='請支持WTech/WBank')
@option("user",description="WBank用戶名 (請確保已開啟paymode)")
@option("amount",description="金額 (最少是WTC$100)",min_value=100)
async def donate(ctx:discord.ApplicationContext,user:str,amount:int):
  #res = get(url="https://sites.wtechhk.xyz/wbank/hash/transfer",headers={"username":user,"reviewer":"wbank","amount":str(amount)})
  res = get(url=f"https://sites.wtechhk.xyz/wbank/openorder?user={user}&reviewer=wbank&amount={str(amount)}")
  try:
    if "success" in res.json():
      await ctx.respond("已成功開單，請登入後，滑動授權支付即可")
    else:
      await ctx.respond(res.text())
  except Exception as e:
    await ctx.respond(f"錯誤: {str(e)}",ephemeral=True)

@bot.slash_command(name="查看Locker",description="查看轉帳區塊鏈")
@option("key",description="為blockID, 即該locker的鑰匙🔑 (一定是127開頭）")
async def check_transfer_blockchain(ctx:discord.ApplicationContext, key:str):
    resp = get(url=f"https://bc.wtechhk.xyz/get/chain/{key}")
    if resp.text() == "找不到該Locker":
      await ctx.respond("不好意思，沒有或找不到該區塊")
    else:
      data = resp.json()
      rawData = data["rawData"].split("--")[1]
      fm = f"""
      區塊ID: {data["blockID"]}
      該區塊哈希(hash-sha256): {data["hash"]}
      生數據(rawData, 即原數據)如下: 
         轉帳帳戶: {rawData.split("->")[0]}
         收款帳戶: {rawData.split("->")[1]}
         金額: {rawData.split("->")[2]}
      """
      await ctx.respond(fm)

# 啟動 Discord Bot
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="WBank的運作"))
    print(f'Logged in as {bot.user}!')

# 啟動 Bot
def run_bot():
  bot.run(os.environ.get('discordToken'))  # 替換為您的 Discord Bot Token
