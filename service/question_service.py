#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dao import crud
from typing import Optional, List, Dict, Union
from service.utils import split_options


def get_question(id: Optional[int], limit: Optional[int], skip: int) -> List[Dict[str, Union[str, int, float]]]:
    r"""
    获取题目的信息，以题目id唯一指定，可以选择limit和skip
    """
    if id is None:
        results = crud.select_items('question_bank', columns=None,
                                 where=None, limit=limit, skip=skip)
    else:
        results = crud.select_items('question_bank', columns=None,
                                 where={'id': id}, limit=limit, skip=skip)
    return split_options(results) #分割选项

def get_questionID(limit: Optional[int], skip: int) -> List[Dict[str, Union[str, int, float]]]:
    r"""
    获取全体题目的ID
    """
    return crud.select_items('question_bank', columns=['id'],
                                 where=None, limit=limit, skip=skip)