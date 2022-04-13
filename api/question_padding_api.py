#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
from fastapi import APIRouter, Body, Path, Query, HTTPException
from fastapi import File
from regex import E
from model.code import Code400
from service import question_padding_service
from fastapi.encoders import jsonable_encoder
from typing import Optional
import base64

# 构建api路由
router = APIRouter(
    prefix="/paddingQue",
    tags=["paddingQue"],
)


@router.get("/get-all-id", responses={400: {"model": Code400}})
async def get_all_paddingQueId(limit: Optional[int] = Query(None), skip: int = Query(0)):
    r"""
    获取所有填字题目的id
    可以选择limit和skip
    """
    try:
        result = question_padding_service.get_all_paddingQueId(limit, skip)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
    return jsonable_encoder(result)


@router.get("/get/{id}", responses={400: {"model": Code400}})
async def get_question(id: int,
                  limit: Optional[int] = Query(None), skip: int = Query(0)):
    r"""
    获取指定ID的填字题目的信息
    """
    try:
        result = question_padding_service.get_paddingQue(id, limit, skip)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
    return jsonable_encoder(result)

@router.post("/get-recognition-result",responses={400: {"model": Code400}})
async def recog_img(imgstr: str):
    """
        获取图片文字的识别信息
    """
    # 解码过程
    
    #TODO 识别图片文字
    return "暂未实现"
