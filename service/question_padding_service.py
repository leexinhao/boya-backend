#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dao import crud
from typing import Optional, List, Dict, Union
from service.utils import split_options


def get_all_paddingQueId(limit: Optional[int], skip: int) -> List[Dict[str, Union[str, int, float]]]:
    r"""
    获取所有填字题目的id
    """
    return crud.select_items('question_padding', columns=['id'],
                                 where=None, limit=limit, skip=skip)

def get_paddingQue(id:int,limit: Optional[int], skip: int) -> List[Dict[str, Union[str, int, float]]]:
    r"""
    获取指定ID的填字题目信息
    """
    return crud.select_items('question_padding', columns=None,
                                 where={'id':id}, limit=limit, skip=skip)

