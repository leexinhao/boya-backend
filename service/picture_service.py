#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dao import crud
from typing import Optional, List, Dict, Union
from service.utils import get_url

def get_pic_briefInfo(pic_id:int,limit:Optional[int]=None,skip:int=0) -> Dict[str,Union[str,int,float]]:
    r"""
    获取指定图片ID的简略信息
    """
    pic_Info =  crud.select_items(table_name='picture',columns=['title','abstract'],where={'picture_id':pic_id}, limit=limit, skip=skip)[0]
    pic_Info['picture_url']=get_url(path="/pictures/pic/",file_type="png",filename=f"{pic_id}_1")
    pic_Info['pinyin_url']=get_url(path="/pictures/pinyin/",file_type="png",filename=f"{pic_id}_2")
    return pic_Info

def get_pic_detailInfo(pic_id:int,limit:Optional[int]=None,skip:int=0) -> Dict[str,Union[str,int,float]]:
    r"""
    获取指定图片ID的详细信息
    """
    pic_Info =  crud.select_items(table_name='picture',columns=['title','abstract','annotation'],where={'picture_id':pic_id}, limit=limit, skip=skip)[0]
    pic_Info['picture_url']=get_url(path="/pictures/pic/",file_type="png",filename=f"{pic_id}_1")
    pic_Info['pinyin_url']=get_url(path="/pictures/pinyin/",file_type="png",filename=f"{pic_id}_2")
    return pic_Info