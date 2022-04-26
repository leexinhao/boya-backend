#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import traceback
from fastapi import APIRouter, Body, Path, Query, HTTPException
from fastapi import File, WebSocket, WebSocketDisconnect
from regex import E, FULLCASE
from model.code import Code400
from service import pk_service,user_service
from fastapi.encoders import jsonable_encoder
from typing import Optional, List, Dict
import base64

# 构建api路由
router = APIRouter(
    prefix="/img",
    tags=["IMG"],
)

@router.post("/styletrans")
async def imgStyleTrans(contentFile: bytes = File(...)):
    r""" 输入内容图片和风格图片，模型训练完毕后返回目标图片url
    """
    url = "http://121.36.59.23/resources/pictures/transfer.png"
    return jsonable_encoder(url)
