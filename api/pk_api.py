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
    prefix="/pk",
    tags=["PK"],
)

# 长连接管理类
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {}
        self.users_flag={}#记录是否已发送对战双方个人信息

    async def connect(self, websocket: WebSocket, token: str, openid: str):
        # 连接
        await websocket.accept()
        if not (token in manager.active_connections.keys()):
            await websocket.send_text("无效的token")
            await websocket.close()
            return False

        elif len(manager.active_connections[token]) == 2:
            await websocket.send_text("房间人数已满")
            await websocket.close()
            return False

        if self.active_connections.get(token,None) is None or len(self.active_connections.get(token,None))==0:
            self.active_connections[token]={}  
            self.users_flag[token]=False

        self.active_connections[token][openid] = websocket
        return True

    def disconnect(self, token: str, openid: str):
        # 断开连接
        del self.active_connections[token][openid]
        del self.users_flag[token]

    async def send_personal_message(self, message: str, websocket: WebSocket,type="text"):
        if type=="text":
            await websocket.send_text(message)
        else:
            await websocket.send_json(message)

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
                manager.users_flag[result]=False
                break
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="客户端运行错误，请检查输入内容或联系管理员！")
    return jsonable_encoder({"token":result})


@router.websocket("/ws1/{token}/{openid}")
async def websocket_endpoint(websocket: WebSocket, token: str, openid: str):
    # 1、用户与服务器建立连接
    print("connect",token, openid)
    r = await manager.connect(websocket, token, openid)
    if not r:
        return

    # TODO 对战实现

    # 2、广播某个用户进入了房间
    await manager.broadcast(f"{openid} 进入了房间", token)
    try:
        while True:
            if len(manager.active_connections[token]) == 2 and (not manager.users_flag[token]):
                manager.users_flag[token]=True
                await manager.broadcast("ok",token)

            data = await websocket.receive_text()
            print("接受信息",data)
            if str(data)=='1':
                # TODO 3、返回两个用户的信息
                user1_info=user_service.get_userInfo(openid)
                
                ids = list(manager.active_connections[token].keys())
                if openid==ids[0]:
                    another_id=ids[1]
                else:
                    another_id=ids[0]
                
                user2_info=user_service.get_userInfo(another_id)
                user_info = {"type":1,\
                    # "uname":[user1_info["uname"],user2_info['uname']],\
                    "avator_url":[user1_info["avator_url"],user2_info["avator_url"]]}
                print('abcd1234')
                await manager.broadcast(user_info,token,"json")

                ##4、发送题目信息
                # await manager.broadcast("水",token)

            # 5、服务器接受客户消息
            ## FIXME 或许是接受json?
            if data!='1':
                #TODO 6、判断答案是否正确
                print(data)
                isright= '水' in data
                if isright:
                    # TODO 7、音频转文字以及根据正确性与否发送消息
                    await manager.broadcast({"type":2,"data":data},token,"json")
                else:
                    await manager.send_personal_message({"type":3,"data":"回答错误"},websocket,"json")

    except WebSocketDisconnect:
        # 5、客户断开联系，进行广播
        print("duanle", token, openid)
        manager.disconnect(token, openid)
        await manager.broadcast({"type":4,"data":f"{openid} 离开了房间"},token,"json")


@router.websocket("/ws2/{token}/{openid}")
async def websocket_endpoint2(websocket: WebSocket, token: str, openid: str):
    # 1、用户与服务器建立连接
    print("connect",token, openid)
    r = await manager.connect(websocket, token, openid)
    if not r:
        return

    # TODO 对战实现

    # 2、广播某个用户进入了房间
    await manager.broadcast(f"{openid} 进入了房间", token)
    another_id=None
    try:
        while True:
            if len(manager.active_connections[token]) == 2 and (not manager.users_flag[token]):
                manager.users_flag[token]=True
                await manager.broadcast("ok",token)

            data = await websocket.receive_text()
            print("接受信息",data)
            if str(data)=='0':
                # TODO 3、返回两个用户的信息
                user1_info=user_service.get_userInfo(openid)
                
                ids = list(manager.active_connections[token].keys())
                if openid==ids[0]:
                    another_id=ids[1]
                else:
                    another_id=ids[0]
                
                user2_info=user_service.get_userInfo(another_id)
                user_info = {"type":1,\
                    # "uname":[user1_info["uname"],user2_info['uname']],\
                    "avator_url":[user1_info["avator_url"],user2_info["avator_url"]]}
                print('abcd1234')
                await manager.broadcast(user_info,token,"json")

            # 4、将接收到的消息发送给另外一方
            if data!='0':
                another_ws = manager.active_connections[token][another_id]
                await manager.send_personal_message({"type":2,"data":data},another_ws,"json")

    except WebSocketDisconnect:
        # 5、客户断开联系，进行广播
        print("duanle", token, openid)
        manager.disconnect(token, openid)
        await manager.broadcast({"type":4,"data":f"{openid} 离开了房间"},token,"json")
