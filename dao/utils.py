#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import pymysql.cursors
from pymysql.converters import escape_string
from typing import List, Optional, Dict, Union
import json
import re

def open_database(db="boya"):
    r"""
    打开数据库连接，并返回connection, cursor
    """
    # 读取本地配置
    with open("dao/config.json") as f:
        db_configs = json.load(f)['database']
    # 打开数据库连接
    connection = pymysql.connect(**db_configs,
                                 db=db,
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection, connection.cursor()


def kv_to_update_set(update_set: Optional[Dict[str, Union[str, int, float]]]):
    r"""
    将键值对或空值转换为sql语句中的update_set条件语句
    Example:
    {"name":"周杰伦", "age":20} => `name`="周杰伦", `age`=20
    """
    if update_set is not None and len(update_set) != 0:
        update_set_choice = []
        for k in update_set.keys():
            if type(update_set[k]) is str:
                update_set_choice.append(
                    '`' + escape_string(k) + '`="' + escape_string(update_set[k]) + '"')
            else:
                update_set_choice.append(
                    '`' + escape_string(k) + '`=' + escape_string(str(update_set[k])) + '')
        update_set_choice = ", ".join(update_set_choice)
    else:
        update_set_choice = "1=1"
    return update_set_choice


def kv_to_where(where: Optional[Dict[str, Union[str, int, float]]], use_like=False):
    r"""
    将键值对或空值转换为sql语句中的where条件语句
    Example:
    use_like=False:
    {"name":"周杰伦", "age":20} => (`name`="周杰伦") AND (`age`=20)
    use_like=True:
    {"name":"周杰伦", "work":"歌手"} => (`name` LIKE "%周杰伦%") AND (`work` LIKE "%歌手%")
    """
    if where is not None and len(where) != 0:
        where_choice = []
        for k in where.keys():
            if type(where[k]) is str:
                if use_like:
                    where_choice.append(
                    '(`' + escape_string(k) + '` LIKE "%' + escape_string(where[k]) + '%")')
                else:
                    where_choice.append(
                        '(`' + escape_string(k) + '`="' + escape_string(where[k]) + '")')
            else:
                assert use_like == False
                where_choice.append(
                    '(`' + escape_string(k) + '`=' + escape_string(str(where[k])) + ')')
        if use_like:
            where_choice = " OR ".join(where_choice)
        else:
            where_choice = " AND ".join(where_choice)
    else:
        if use_like:
            where_choice = "1=0"
        else:
            where_choice = "1=1"
    return where_choice