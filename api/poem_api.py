#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
from fastapi import APIRouter, Path, Query, HTTPException
from model.code import Code400
from service import poem_service
from fastapi.encoders import jsonable_encoder
from typing import Optional

# 构建api路由
router = APIRouter(
    prefix="/poem",
    tags=["Poem"],
)


@router.get("/get-all", responses={400: {"model": Code400}})
async def get_all_poemID(limit: Optional[int] = Query(None), skip: int = Query(0)):
    r"""
    获取所有诗歌的标题和ID
    可以选择limit和skip
    """
    try:
        result = poem_service.get_poemID(limit, skip)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
    return jsonable_encoder(result)


@router.get("/get/{poem_id}", responses={400: {"model": Code400}})
async def get_poemInfo(poem_id: int,
                  limit: Optional[int] = Query(None), skip: int = Query(0)):
    r"""
    获取指定ID的诗歌信息
    """
    try:
        result = poem_service.get_poemInfo(poem_id, limit, skip)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
    return jsonable_encoder(result)
