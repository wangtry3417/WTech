import torch
import torch.nn as nn
import numpy as np
import json
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from collections import defaultdict
import re

# 1. 數據預處理系統
class 貸款數據預處理器:
    """貸款數據智能處理器"""
    def __init__(self):
        # 特徵配置
        self.數值特徵 = ['年齡', '收入', '支出', '資產', '負債', '信用分數']
        self.分類特徵 = ['職業', '教育程度', '婚姻狀況']
        self.數值標準化器 = StandardScaler()
        self.分類編碼器 = OneHotEncoder(handle_unknown='ignore', sparse=False)
        
    def 載入數據(self, json檔案路徑):
        """從JSON檔案加載並處理數據"""
        with open(json檔案路徑, 'r', encoding='utf-8') as f:
            原始數據 = json.load(f)
        
        # 提取數值特徵
        數值數據 = np.array([
            [float(個案[特徵]) for 特徵 in self.數值特徵]
            for 個案 in 原始數據
        ], dtype=np.float32)
        
        # 提取分類特徵
        分類數據 = np.array([
            [個案[特徵] for 特徵 in self.分類特徵]
            for 個案 in 原始數據
        ])
        
        # 訓練預處理器
        self.數值標準化器.fit(數值數據)
        self.分類編碼器.fit(分類數據)
    
    def 解析輸入(self, 文字輸入):
        """解析文字格式輸入"""
        數據 = {}
        for 項目 in 文字輸入.split(';'):
            if ':' in 項目:
                鍵, 值 = 項目.split(':', 1)
                鍵 = 鍵.strip().lower()
                值 = 值.strip()
                # 數值類型轉換
                if 鍵 in self.數值特徵:
                    值 = float(re.sub(r'[^\d.]', '', 值))
                數據[鍵] = 值
        return 數據
    
    def 轉換數據(self, 原始數據):
        """將輸入數據轉換為模型可讀格式"""
        if isinstance(原始數據, str):
            原始數據 = self.解析輸入(原始數據)
        
        # 填充缺失值
        for 特徵 in self.數值特徵:
            if 特徵 not in 原始數據:
                原始數據[特徵] = 0.0
        for 特徵 in self.分類特徵:
            if 特徵 not in 原始數據:
                原始數據[特徵] = '未知'
        
        # 準備特徵矩陣
        數值特徵 = np.array([
            原始數據[特徵] for 特徵 in self.數值特徵
        ], dtype=np.float32).reshape(1, -1)
        
        分類特徵 = np.array([
            [原始數據[特徵] for 特徵 in self.分類特徵]
        ], dtype=object).reshape(1, -1)
        
        # 特徵工程
        標準化數值 = self.數值標準化器.transform(數值特徵)
        編碼分類 = self.分類編碼器.transform(分類特徵)
        
        return torch.FloatTensor(np.hstack([標準化數值, 編碼分類]))

# 2. 核心預測模型
class 貸款預測模型(nn.Module):
    """貸款風險評估神經網絡"""
    def __init__(self, 輸入尺寸):
        super().__init__()
        self.特徵網絡 = nn.Sequential(
            nn.Linear(輸入尺寸, 64),
            nn.ReLU(),
            nn.Dropout(0.3)
        )
        
        # 雙任務輸出層
        self.貸款概率頭 = nn.Sequential(
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
        
        self.原因分析頭 = nn.Sequential(
            nn.Linear(64, 32),
            nn.Linear(32, 輸入尺寸),  # 每個特徵的重要性權重
            nn.Sigmoid()
        )
    
    def forward(self, x):
        特徵 = self.特徵網絡(x)
        貸款概率 = self.貸款概率頭(特徵)
        原因權重 = self.原因分析頭(特徵)
        return 貸款概率, 原因權重

# 3. 解釋引擎
class 貸款決策解釋器:
    """生成可理解的貸款決策解釋"""
    def __init__(self, 預處理器):
        self.數值特徵 = 預處理器.數值特徵
        self.分類特徵 = 預處理器.分類特徵
        self.特徵名稱 = self.數值特徵 + \
                      [f"{特徵}_{類別}" for i, 特徵 in enumerate(self.分類特徵)
                           for 類別 in 預處理器.分類編碼器.categories_[i]]
    
    def 生成報告(self, 概率, 權重, 原始輸入):
        """生成完整解釋報告"""
        # 關鍵因素分析
        前3名索引 = torch.topk(權重, k=3).indices.tolist()
        原因分析 = []
        for 索引 in 前3名索引:
            特徵名稱 = self.特徵名稱[索引]
            重要性 = 權重[索引].item()
            # 關聯原始值
            if 特徵名稱 in self.數值特徵:
                原始值 = 原始輸入[特徵名稱]
            else:
                原始特徵 = 特徵名稱.split('_')[0]
                原始值 = 原始輸入[原始特徵]
            原因分析.append({
                "因素": 特徵名稱,
                "重要性": f"{重要性*100:.1f}%",
                "您的數值": 原始值
            })
        
        return {
            "貸款批准概率": f"{概率.item()*100:.1f}%",
            "關鍵因素": 原因分析,
            "風險等級": self._獲取風險等級(概率.item())
        }
    
    def _獲取風險等級(self, 概率):
        if 概率 < 0.3:
            return "高風險 (建議拒絕)"
        elif 概率 < 0.7:
            return "中等風險 (需人工審核)"
        else:
            return "低風險 (建議通過)"

# 4. 完整貸款分析系統
class 貸款分析大腦:
    """整合式貸款決策AI系統"""
    def __init__(self, 模型路徑="models/貸款模型.pth", 數據路徑="data/訓練數據.json"):
        # 初始化組件
        self.預處理器 = 貸款數據預處理器()
        self.預處理器.載入數據(數據路徑)
        
        # 建立模型
        輸入尺寸 = len(self.預處理器.數值特徵) + \
                  len(self.預處理器.分類編碼器.get_feature_names_out())
        self.模型 = 貸款預測模型(輸入尺寸)
        
        # 加載預訓練權重
        self.模型.load_state_dict(torch.load(模型路徑))
        self.模型.eval()
        
        # 解釋引擎
        self.解釋器 = 貸款決策解釋器(self.預處理器)
    
    def 分析(self, 輸入數據):
        """執行完整分析流程"""
        # 數據預處理
        張量數據 = self.預處理器.轉換數據(輸入數據)
        
        # 模型預測
        with torch.no_grad():
            概率, 權重 = self.模型(張量數據)
        
        # 生成解釋報告
        if isinstance(輸入數據, str):
            原始輸入 = self.預處理器.解析輸入(輸入數據)
        else:
            原始輸入 = 輸入數據
        
        return self.解釋器.生成報告(概率, 權重[0], 原始輸入)

# 示例JSON數據格式 (data/訓練數據.json)
"""
[
  {
    "年齡": 35,
    "收入": 85000,
    "支出": 45000,
    "資產": 300000,
    "負債": 150000,
    "信用分數": 720,
    "職業": "工程師",
    "教育程度": "碩士",
    "婚姻狀況": "已婚",
    "是否批准": 1
  },
  {
    "年齡": 28,
    "收入": 50000,
    "支出": 38000,
    "資產": 80000,
    "負債": 90000,
    "信用分數": 650,
    "職業": "教師",
    "教育程度": "學士",
    "婚姻狀況": "單身",
    "是否批准": 0
  }
]
"""

if __name__ == "__main__":
    # 初始化AI大腦
    大腦 = 貸款分析大腦()
    
    # 案例1: 文字輸入
    文字輸入 = "姓名: 陳大文; 年齡: 30; 收入: 80000; 支出: 45000; 資產: 200000; 負債: 100000; 信用分數: 680; 職業: 工程師; 教育程度: 碩士; 婚姻狀況: 已婚"
    結果 = 大腦.分析(文字輸入)
    print("\n貸款分析結果:")
    print(json.dumps(結果, indent=2, ensure_ascii=False))
    
    # 案例2: 字典輸入
    字典輸入 = {
        "年齡": 45,
        "收入": 120000,
        "支出": 60000,
        "資產": 500000,
        "負債": 200000,
        "信用分數": 750,
        "職業": "醫生",
        "教育程度": "博士",
        "婚姻狀況": "已婚"
    }
    結果 = 大腦.分析(字典輸入)
    print("\n貸款分析結果:")
    print(json.dumps(結果, indent=2, ensure_ascii=False))