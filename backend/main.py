import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from utils.database import init_db, close_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时初始化数据库
    init_db()
    yield
    # 应用关闭时关闭数据库
    close_db()

# Import all the Routers
# 创建了一个 FastAPI 应用实例，所有的api路由将以/api/v1为前缀
app = FastAPI(root_path='/api/v1',lifespan=lifespan)

#app = FastAPI(root_path='/api',lifespan=lifespan)

# 导入系统管理和用户注册相关路由
from routers.systemManager import (systemManager)
from routers.user import (user)
from routers.dataRequest import (dataRequest)
from fastapi.middleware.cors import CORSMiddleware

# 包含路由
app.include_router(systemManager, tags=["Manager for our System"])
app.include_router(user, tags=["Register function for our system"])
app.include_router(dataRequest, tags=["Deal with data request"])

# 这里添加 CORS 中间件，允许所有来源（在生产环境中应更加严格）
# CORS 中间件用于处理跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名，对于生产环境应该更加具体
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法，包括 OPTIONS
    allow_headers=["*"],  # 允许所有头部
)


# @app.get("/api/v1")
# def read_root():
#     return {"Hello": "World"}

# 运行应用程序
if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)