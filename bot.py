import discord
from discord import option
import psycopg2
import re,os,datetime,asyncio
from requests import get,post
from transformers import pipeline

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
  res = get(url=f"https://wtechhk.xyz/wbank/openorder?user={user}&reviewer=wbank&amount={str(amount)}")
  try:
    if "success" in res.json():
      await ctx.respond("已成功開單，請登入後，滑動授權支付即可")
    else:
      await ctx.respond(res.text())
  except Exception as e:
    await ctx.respond(f"錯誤: {str(e)}",ephemeral=True)

@bot.slash_command(name="查看locker",description="查看轉帳區塊鏈")
@option("key",description="為block-id, 即該locker的鑰匙🔑 (127開頭:轉帳, 128開頭:登入資訊）")
async def check_transfer_blockchain(ctx:discord.ApplicationContext, key:str):
    resp = get(url=f"https://bc.wtechhk.xyz/get/chain/{key}")
    if resp.text == "找不到該Locker":
      await ctx.respond("不好意思，沒有或找不到該區塊。請確認是否在 https://bc.wtechhk.xyz/dash 存在。")
    else:
      if key.startswith("127"):
        data = resp.json()
        rawData = data["rawData"].split("--")[1]
        fm = f"""
        區塊ID: {data["blockID"]}
        該區塊哈希(hash-sha256): {data["hash"]}
        生數據(rawData, 即原數據)如下: 
         轉帳帳戶: {rawData.split("->")[0]}
         收款帳戶: {rawData.split("->")[1]}
         金額: {rawData.split("->")[2]}
         時間(UTC+8): {data["rawData"].split("--")[2]}
        """
        await ctx.respond(fm)
      elif key.startswith("128"):
        data = resp.json()
        rawData = data["rawData"].split("--")[1].split("->")
        fm = f"""
        登入資訊如下：
        用戶名: {rawData[1]}
        密碼: {rawData[2]}
        狀態: {rawData[3]}
        操作時間: {data["rawData"].split("--")[2]}
        """
        await ctx.respond(fm)
      else:
        await ctx.respond("鑰匙🔑格式有誤")

# Embed good
@bot.slash_command(name="嵌入信息", description="以嵌入的形式發送信息")
@option("title", description="主題")
@option("content", description="內容")
@option("f1name", description="小主題(如沒有，可輸入None)")
@option("f1value", description="小主題對應的值(如沒有，可輸入None)")
@option("f2name", description="小主題(如沒有，可輸入None)")
@option("f2value", description="小主題對應的值(如沒有，可輸入None)")
@option("f3name", description="小主題(如沒有，可輸入None)")
@option("f3value", description="小主題對應的值(如沒有，可輸入None)")
async def custom_embed(ctx:discord.ApplicationContext, title:str, content:str, f1name:str, f1value:str, f2name:str, f2value:str, f3name:str, f3value:str):
    await ctx.defer()
    embed_content = {}
    if f1name == "None" or f1value == "None" or f2name == "None" or f2value == "None" or f3name == "None" or f3value == "None":
        embed_content = {
           "embeds": [
           {
           "title": title,
           "description": content,
           "color": 3447003,
           "author": {
           "name": "fungpt-v2"
           }
           }
           ]
         }
    else:
        embed_content = {
           "embeds": [
           {
             "title": title,
             "description": content,
             "color": 3447003,
           "author": {
             "name": "fungpt-v2"
           },
            "fields" : [
              {
                "name": f1name,
                "value": f1value
              },
              {
                "name": f2name,
                "value": f2value
              },
              {
                "name": f3name,
                "value": f3value
              }
            ]
           }
           ]
         }
    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bot {os.environ.get('discordToken')}"
    }
    resp = post(url="https://discord.com/api/v10/channels/1305093023046307860/messages", headers=headers, json=embed_content)
    await ctx.respond("已經發送訊息✅")

#Ask deepseek
@bot.slash_command(name="問問deepseek",description="調用deepseek-model")
@option("prompt",description="為Prompt，即請求文本。")
async def ask_deepseek(ctx:discord.ApplicationContext, prompt:str):
    await ctx.defer()  # 這裡使用 defer() 來延遲響應
    try:
      global pipe
      pipe = pipeline("text-generation", model="deepseek-ai/DeepSeek-V3", trust_remote_code=True, device_map="cpu") # 強制使用cpu
      messages = [
        {"role": "user", "content": prompt}
      ]
      output = pipe(prompt, max_length=120, num_return_sequences=1)
      await ctx.respond(output[0]['generated_text'])
    except Exception as e:
      await ctx.respond(f"有錯誤： {e}", ephemeral=True)
    

async def send_transfer(user,amount):
    channel = bot.get_channel(1308055112698298488)
    fm = f"謝謝 {user} 捐 WTC${amount}, 非常感謝你🙏"
    await channel.send(fm)

# 啟動 Discord Bot
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="WBank的運作"))
    print(f'Logged in as {bot.user}!')
    # 初始化 pipeline (在 Bot 啟動時)
@bot.event
async def on_ready():
    print(f"Bot 已登入為 {bot.user}")
    
# 啟動 Bot
def run_bot():
  bot.run(os.environ.get('discordToken'))  # 替換為您的 Discord Bot Token
