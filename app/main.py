# app/main.py
import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import uvicorn

from app.api.routes import user as user_router, file as file_router
from app.core.config import settings
from app.core.exceptions import http_exception_handler, generic_exception_handler
from app.core.database import engine, Base
from app.api.main import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
)

# 自动创建数据库表（首次启动时会根据 models 创建表）
Base.metadata.create_all(bind=engine)

# 配置 CORS（如有需要）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局异常处理器：HTTPException 与所有未捕获异常
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# 全局中间件：统一 JSON 输出格式
@app.middleware("http")
async def add_custom_response_format(request: Request, call_next):
    response = await call_next(request)
    # 针对 application/json 类型的响应包装统一格式
    if "application/json" in response.headers.get("content-type", ""):
        body = b""
        async for chunk in response.body_iterator:
            body += chunk
        try:
            original_data = json.loads(body)
        except Exception:
            original_data = body.decode()
        new_data = {
            "code": response.status_code,
            "message": "Success" if response.status_code == 200 else "",
            "data": original_data,
        }
        return JSONResponse(content=new_data, status_code=response.status_code)
    else:
        return response

# 引入用户与文件模块的路由
app.include_router(api_router, prefix=settings.API_ROUTE_PREFIX)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
