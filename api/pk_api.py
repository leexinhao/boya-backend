#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
from fastapi import APIRouter, Body, Path, Query, HTTPException
from fastapi import File, WebSocket, WebSocketDisconnect
from regex import E
from model.code import Code400
from service import pk_service,user_service
from fastapi.encoders import jsonable_encoder
from typing import Optional, List, Dict
import base64

# 构建api路由
router = APIRouter(
    prefix="/pk",
    tags=["PK"],
)

# 长连接管理类
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, token: str, openid: str):
        # 连接
        await websocket.accept()
        if self.active_connections.get(token,None) is None or len(self.active_connections.get(token,None))==0:
            self.active_connections[token]={}
        self.active_connections[token][openid] = websocket

    def disconnect(self, token: str, openid: str):
        # 断开连接
        del self.active_connections[token][openid]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, token: str,type="text"):
        # 向指定token的房间发送广播
        for connection in self.active_connections[token].values():
            if type=="text":
                await connection.send_text(message)
            else:
                await connection.send_json(message)

manager = ConnectionManager()

@router.get("/gen-key", responses={400: {"model": Code400}})
async def generate_token():
    r"""
    生成六位对战密令
    """
    try:
        while True:
            result = pk_service.gen_key_service()
            if manager.active_connections.get(result, None) is None:  # 防止生成重复的密令
                manager.active_connections[result] = {}
                break
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
    return jsonable_encoder({"token":result})


@router.websocket("/ws/{token}/{openid}")
async def websocket_endpoint(websocket: WebSocket, token: str, openid: str):
    # 1、用户与服务器建立连接
    await manager.connect(websocket, token, openid)
    if token not in manager.active_connections.keys():
        websocket.send_text("无效的token")
        websocket.close()
    elif len(manager.active_connections[token]) == 2:
        websocket.send_text("房间人数已满")
        websocket.close()
    # TODO 对战实现

    # 2、广播某个用户进入了房间
    await manager.broadcast(f"{openid} 进入了房间", token)
    flag = False

    try:
        while True:
            if len(manager.active_connections[token]) == 2 and not flag:
                # TODO 3、返回两个用户的信息
                flag = True
                user1_info=user_service.get_userInfo(openid)
                
                ids = manager.active_connections[token].keys()
                if openid==ids[0]:
                    another_id=ids[1]
                else:
                    another_id=ids[0]
                
                user2_info=user_service.get_userInfo(another_id)
                user_info = {"uname":[user1_info["name"],user2_info['name']],\
                    "avator_url":[user1_info["avator_url"],user2_info["avator_url"]]}

                manager.broadcast(user_info,token,"json")

                ##4、发送题目信息
                manager.broadcast("水",token)

            # 5、服务器接受客户消息
            ## FIXME 或许是接受json?
            data = await websocket.receive_text()

            #TODO 6、判断答案是否正确
            # isright=

            # TODO 7、音频转文字以及根据正确性与否发送消息
            await manager.broadcast(f"{openid} 发送信息：{data}")

    except WebSocketDisconnect:
        # 5、客户断开联系，进行广播
        manager.disconnect(token, openid)
        await manager.broadcast(f"{openid} 离开了房间",token)
