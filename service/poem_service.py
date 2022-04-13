#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dao import crud
from typing import Optional, List, Dict, Union
from service.utils import get_url


def get_poemID(limit: Optional[int], skip: int) -> Dict[str, Dict[str, Union[str, int, float]]]:
    r"""
    获取所有诗歌的标题和ID
    可以选择limit和skip
    """
    result = {"feng":[],"ya":[],"song":[]}
    class_map = {"国风": "feng", "小雅": "ya", "大雅": "ya",
                 "周颂": "song", "鲁颂": "song", "商颂": "song"}

    poem_list = crud.select_items("poem", columns=['poem_id', 'title'], where=None,
                                  limit=limit, skip=skip)
    for poem in poem_list:
        title_sects = poem['title'].split('·')
        title_first=title_sects[0]
        poem_class = class_map[title_first]
        poem_id={"poem_id": poem['poem_id'], "title": "·".join(title_sects[1:])}
        result[poem_class].append(poem_id)
    return result

def get_poemInfo(poem_id: int, limit: Optional[int], skip: int) -> Dict[str, Union[str, int, float]]:
    r"""
    获取指定ID诗歌的信息
    """
    poem_Info=crud.select_items('poem', columns=None,
                                where={'poem_id': poem_id}, limit=limit, skip=skip)[0]
    poem_Info['recite_url']=get_url(path="/audio/recite/",file_type="mp3",filename=str(poem_id))
    poem_Info['appreciation_url']=get_url(path="/audio/appreciation/",file_type="mp3",filename=str(poem_id))
    poem_Info['title']="·".join(poem_Info['title'].split("·")[-1:])
    return poem_Info

