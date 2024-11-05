# 使用官方 Python 映像作為基礎映像
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /

# 複製 requirements.txt 並安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式代碼
COPY . .

# 開放應用的端口
EXPOSE 5000

# 設定環境變數
ENV FLASK_APP=main.py  # 替換為主應用程式文件名
ENV FLASK_RUN_HOST=0.0.0.0  # 設定 Flask 服務在所有可用的 IP 上運行

# 啟動 Flask 應用
CMD ["flask", "run"]
