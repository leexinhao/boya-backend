#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional
from pydantic import BaseModel, Field

class Question(BaseModel):
    r"""
    题库中的题目描述
    """
    name: int # 题目名字（编号）
    type: str = Field(..., min_length=1, max_length=20) # 题目类型
    description: str = Field(..., min_length=1, max_length=255) # 题干
    option: Optional[str] = Field(None, min_length=1, max_length=255) # 题目选项
    answer: Optional[str] = Field(..., min_length=1, max_length=255) # 题目答案
    explanation: Optional[str] = Field(
        None, min_length=1, max_length=255)  # 题目答案
