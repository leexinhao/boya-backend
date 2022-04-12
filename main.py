#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uvicorn
from fastapi import FastAPI
from api import question_api,user_api,poem_api,picture_api,question_padding_api,pk_api
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


# 声明fastapi的实例
app = FastAPI(title='文档说明', description='整体描述')
# 配置静态资源的存放路径以及请求的路径
app.mount("/resources", StaticFiles(directory="assets/public"), name="assets/public")

# 跨域配置
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])


# 注册api模块
app.include_router(question_api.router, prefix='/api')
app.include_router(user_api.router, prefix='/api')
app.include_router(poem_api.router, prefix='/api')
app.include_router(picture_api.router, prefix='/api')
app.include_router(question_padding_api.router, prefix='/api')
app.include_router(pk_api.router, prefix='/api')

# 配置容器启动相应的实例
if __name__ == '__main__':
    uvicorn.run(app='main:app', port=80, reload=True)
