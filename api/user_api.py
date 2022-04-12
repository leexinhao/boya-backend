#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
from fastapi import APIRouter, Body, Path, Query, HTTPException
from regex import E
from model.code import Code400
from service import user_service
from fastapi.encoders import jsonable_encoder
from typing import Optional

# 构建api路由
router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.post("/login",responses={400:{"model":Code400}})
async def user_logIn(uname:str=Body(...),avator_url:str=Body(...),openid:str=Body(...)):
    r"""
    用户登录，若用户未存在则插入数据库，已存在更新用户信息
    """
    try:
        result=user_service.login(uname,avator_url,openid)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400,detail="客户端运行错误，请检查输入内容或联系管理员！")
    return jsonable_encoder(result)
