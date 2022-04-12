#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
from fastapi import APIRouter, Path, Query, HTTPException
from model.code import Code400
from service import picture_service
from fastapi.encoders import jsonable_encoder
from typing import Optional

# 构建api路由
router = APIRouter(
    prefix="/pic",
    tags=["Pic"],
)


@router.get("/get/briefinfo/{pic_id}", responses={400: {"model": Code400}})
async def get_picture_briefInfo(pic_id: int,
                  limit: Optional[int] = Query(None), skip: int = Query(0)):
    r"""
    获取指定ID的图片简略信息
    """
    try:
        result = picture_service.get_pic_briefInfo(pic_id,limit,skip)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
    return jsonable_encoder(result)

@router.get("/get/detailinfo/{pic_id}", responses={400: {"model": Code400}})
async def get_picture_detailInfo(pic_id: int,
                  limit: Optional[int] = Query(None), skip: int = Query(0)):
    r"""
    获取指定ID的图片简略信息
    """
    try:
        result = picture_service.get_pic_detailInfo(pic_id,limit,skip)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
    return jsonable_encoder(result)