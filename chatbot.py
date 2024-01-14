import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class AIModules:
  def __init__(self,text):
    self.text = text
  def think(self):
    tokens = word_tokenize(self.text)  # 分词
        tokens = [token.lower() for token in tokens]  # 转换为小写
        tokens = [token for token in tokens if token.isalpha()]  # 仅保留字母字符
        tokens = [token for token in tokens if token not in stopwords.words("english")]  # 去除停用词

        response = " ".join(tokens)
        return response
