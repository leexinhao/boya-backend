#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dao import crud
from typing import Optional, List, Dict, Union

def login(uname: str, avator_url: str, openid: str) -> str:
    r"""
    用户登录，若用户未存在则插入数据库，已存在则更新用户信息
    """
    user_info = crud.select_items(table_name='user', columns=None,
                                  where={'openid': openid})
    if user_info is None or len(user_info) == 0:
        return crud.insert_items(table_name='user', columns=['uname', 'avator_url', 'openid'],
                                 values=[[uname, avator_url, openid]])
    else:
        return crud.update_items(table_name='user', items={'uname': uname, 'avator_url': avator_url, 'openid': openid},
                                 where={'id': user_info[0]['id']})

def get_userInfo(openid:str)->str:
    r"""
    获取指定openid的用户信息
    """
    return crud.select_items("user",columns=None,where={"openid":openid})[0]