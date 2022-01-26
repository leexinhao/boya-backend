#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dao import crud
from typing import Optional, List, Dict, Union



def get_question(id: Optional[int], limit: Optional[int], skip: int) -> List[Dict[str, Union[str, int, float]]]:
    r"""
    获取题目的信息，以题目id唯一指定，可以选择limit和skip
    """
    if id is None:
        return crud.select_items('question_bank', columns=None,
                                 where=None, limit=limit, skip=skip)
    else:
        return crud.select_items('question_bank', columns=None,
                                 where={'id': id}, limit=limit, skip=skip)



