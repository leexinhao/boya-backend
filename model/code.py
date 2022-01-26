#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pydantic import BaseModel


class Code400(BaseModel):
    detail: str = "客户端运行错误，请检查输入内容或联系管理员！"


class Code403(BaseModel):
    detail: str = "客户端请求权限不足"
