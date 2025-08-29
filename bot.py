import discord
from discord import option
import psycopg2
import re,os,datetime,asyncio
from requests import get,post
from datetime import datetime, timedelta
import random

# Discord Bot 設定
bot = discord.Bot()

# 連接到 PostgreSQL 資料庫
def get_db_connection():
    return psycopg2.connect(str(os.environ.get("dataurl")))

# 每個3分鐘開次獎
async def 開獎():
    conn = get_db_connection()
    cursor = conn.cursor()
    # 中獎名單
    cursor.execute("select username from wbankwallet where balance>=1000") # 此命令一定要有wbankwallet表
    results = cursor.fetchall()
    wcoins_users = []
    for row in results:
      if "w.gov" in row[0]: continue
      wcoins_users.append(row[0])
    if not wcoins_users: wcoins_users = ["wangtry", "wbank"]
    now_utc = datetime.utcnow()
    now_utc8 = now_utc + timedelta(seconds=8*60*60)
    wcoins_reward_user = random.choice(wcoins_users)
    wcoins_reward_amount = random.randint(100, 100000)
    message = {
           "embeds": [
           {
           "title": "WTech官方派幣",
           "description": "這個是wtech.wcoins樂透，每5分鐘開獎",
           "color": 3447003,
           "author": {
           "name": "wcoins/gift"
           },
           "fields": [
              {
                "name": "中獎者",
                "value": wcoins_reward_user
              },
              {
                "name": "wcoins提供者",
                "value": "wcs://wcoins.net/wbank"
              },
              {
                "name": "中獎金額",
                "value": str(wcoins_reward_amount)
              },
              {
                "name": "時間",
                "value":  now_utc8.strftime("%Y年 %m月 %d 日，%H:%M:%S")
           ]
           }
           ]
         }
    cursor.close()
    conn.close()
    return message, wcoins_reward_user, wcoins_reward_amount

# 模擬股票
async def 股票代號自動補全(ctx: discord.AutocompleteContext):
    return ["0050.TW", "2330.TW", "AAPL", "MSFT", "00941.HK", "BTC-USD"]

def 技術分析模擬(當前價, 歷史高, 歷史低):
    """基於價格位置的模擬技術分析"""
    位置比例 = (當前價 - 歷史低) / (歷史高 - 歷史低)
    
    if 位置比例 < 0.3:
        return "超賣區域", random.randint(70, 85)  # 買入機率
    elif 位置比例 > 0.7:
        return "超買區域", random.randint(15, 30)  # 買入機率
    else:
        return "中性區域", random.randint(40, 60)

def 生成買賣建議(買入機率):
    """根據機率生成建議"""
    if 買入機率 >= 70:
        return "🟢 強力買入", "當前價格處於有利位置，風險回報比佳"
    elif 買入機率 >= 55:
        return "🟡 考慮買入", "價格合理但需注意市場波動"
    elif 買入機率 >= 45:
        return "⚪ 保持觀望", "價格處於均衡區間，建議等待更明確信號"
    else:
        return "🔴 考慮減倉", "價格可能過高，注意回調風險。另外，如果持有，應考慮部分或全部減倉"

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
  url = f"https://wtechhk.com/wbank/auth/v1?url=/wbank/card/page/wbank/{amount}?url=/"
  try:
    await ctx.respond(f"你的付款url: {url}")
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
@option("role",description="為模型設定，讓它可以在你的文本的範圍內找")
async def ask_deepseek(ctx:discord.ApplicationContext, prompt:str, role:str):
    await ctx.defer()  # 這裡使用 defer() 來延遲響應
    try:
      req_headers = {
        "User-Agent": "cnGOV/5.0",
        "Content-type": "application/json",
        "Authorization": f"Bearer {os.environ.get('deepseekKey')}"
      }
      req_json = {
  "model": "deepseek-chat",
  "temperature": 0.7,
  "max_tokens": 1400,
  "messages": [
    {
      "role": "system",
      "content": role
    },
    {
      "role": "user",
      "content": prompt
    }
  ]
}
      resp = post(url="https://api.deepseek.com/v1/chat/completions", headers=req_headers, json=req_json)
      gen_answer = resp.json()["choices"][0]["message"]["content"]
      edited_answer = (
                gen_answer
                .replace("**", "") 
                .replace("### ", "**") 
                .replace("#### ", "**")  
                .replace("\n- ", "\n• ") 
                .replace("---", "") 
            )
      if len(edited_answer) >= 2000: edited_answer = edited_answer[:1997] + "..."
      await ctx.respond(edited_answer)
    except Exception as e:
      await ctx.respond(f"有錯誤： {e}", ephemeral=True)

# 股票分析指令
@bot.slash_command(name="股票分析", description="免API金鑰的股票分析與買賣建議")
@option("stock", description="股票代號（例：AAPL）", required=True)
async def 股票分析(
    ctx: discord.ApplicationContext,
    #代號: Option(str, "股票代號（例：AAPL）", required=True, autocomplete=股票代號自動補全)
    stock:str
):
    await ctx.defer()
    
    try:
        # 獲取公開市場數據
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stock}?interval=1d&range=3mo"
        req_headers = {
          "User-Agent": "Mozilla/5.0 (WOS) <Chrome> (<Chrome/1.2)"
        }
        data = get(url, headers=req_headers).json()["chart"]["result"][0]
        meta = data["meta"]
        指標 = data["indicators"]["quote"][0]
        
        # 提取關鍵數據
        當前價 = meta["regularMarketPrice"]
        歷史高 = meta["fiftyTwoWeekHigh"]
        歷史低 = meta["fiftyTwoWeekLow"]
        成交量 = sum(指標["volume"][-5:])/5  # 5日平均成交量
        
        # 模擬分析
        技術狀態, 買入機率 = 技術分析模擬(當前價, 歷史高, 歷史低)
        建議, 理由 = 生成買賣建議(買入機率)
        沽出機率 = 100 - 買入機率
        
        # 建立分析報告
        embed = discord.Embed(
            title=f"{stock} 分析報告",
            description=f"**{建議}**\n{理由}",
            color=0x109319 if 買入機率 >=55 else 0xeb4034 if 買入機率 <45 else 0xf5a623
        )
        
        embed.add_field(name="📈 當前價格", value=f"{當前價:.2f}", inline=True)
        embed.add_field(name="📊 52週範圍", value=f"{歷史低:.2f} ~ {歷史高:.2f}", inline=True)
        embed.add_field(name="🔄 近期成交量", value=f"{成交量:,.0f}", inline=True)
        
        embed.add_field(
            name="🤖 此Bot建議機率", 
            value=f"```diff\n+ 買入: {買入機率}%\n- 沽出: {沽出機率}%\n```", 
            inline=False
        )
        
        embed.add_field(
            name="📉 技術狀態", 
            value=f"```{技術狀態} ({(當前價-歷史低)/(歷史高-歷史低)*100:.1f}%區間)```", 
            inline=False
        )
        
        embed.set_footer(text="⚠️ 此為模擬分析，實際投資需自行判斷")
        
        await ctx.followup.send(embed=embed)
        
    except Exception as e:
        await ctx.followup.send(f"❌ 分析失敗：{str(e)} , Text: {get(url).content}")

async def send_transfer(user,amount):
    channel = bot.get_channel(1308055112698298488)
    fm = f"謝謝 {user} 捐 WTC${amount}, 非常感謝你🙏"
    await channel.send(fm)

# 啟動 Discord Bot
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="WBank的運作", url="https://wtechhk.com", start=datetime(1993, 6, 18, 16, 18)))
    print(f'Logged in as {bot.user}!')
    # 初始化 pipeline (在 Bot 啟動時)
    #print(f"Bot 已登入為 {bot.user}")
    await run_rewards()

async def run_rewards():
    while True:
        msg, user, amount = await 開獎()
        channel = bot.get_channel(1305093023046307860)
        get(url="https://wtechhk.com/wbank/hash/transfer", headers={"user":"wbank","reviewer":"wbank","amount":str(amount)})
        get(url="https://wtechhk.com/wbank/hash/transfer", headers={"user":"wbank","reviewer":user,"amount":str(amount)})
        headers = {
          "Content-Type": "application/json",
          "Authorization": f"Bot {os.environ.get('discordToken')}"
        }
        post(url="https://discord.com/api/v10/channels/1305093023046307860/messages", headers=headers, json=msg)
        await asyncio.sleep(3*60)
    
# 啟動 Bot
def run_bot():
  bot.run(os.environ.get('discordToken'))  # 替換為您的 Discord Bot Token
