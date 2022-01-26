#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
from fastapi import APIRouter, Path, Query, HTTPException
from model.code import Code400
from service import question_service
from fastapi.encoders import jsonable_encoder
from typing import Optional

# 构建api路由
router = APIRouter(
    prefix="/question",
    tags=["Question"],
)


@router.get("/get-all", responses={400: {"model": Code400}})
async def get_all_questions(limit: Optional[int] = Query(None), skip: int = Query(0)):
    r"""
    获取所有题目的信息
    可以选择limit和skip
    """
    try:
        result = question_service.get_question(None, limit, skip)
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
    获取题目的信息，以路径参数id唯一指定，可以选择limit和skip
    """
    try:
        result = question_service.get_question(id, limit, skip)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
    return jsonable_encoder(result)
