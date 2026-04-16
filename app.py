import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

from app import create_app

# 初始化 Flask 實體
app = create_app()

if __name__ == '__main__':
    # 啟動開發伺服器
    app.run(debug=True, port=5000)
