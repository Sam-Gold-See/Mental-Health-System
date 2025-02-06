import os

import dotenv

# 加载环境变量
if os.getenv("ENV", "dev") == "dev":
    print("Loading development environment variables")
    dotenv.load_dotenv(".env.development")
elif os.getenv("ENV", "dev") == "prod":
    print("Loading production environment variables")
    dotenv.load_dotenv(".env.production")

# 数据库连接字符串
SQL_URL = os.getenv("DATABASE_URL")

