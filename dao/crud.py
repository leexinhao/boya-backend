#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymysql.converters import escape_string
from typing import Optional, List, Dict, Union
from dao.utils import kv_to_where, kv_to_update_set, open_database


def insert_items(table_name: str,
                 columns: List[str],
                 values:  List[List[Union[str, int, float]]]) -> str:
    r"""
    单表插入
    支持同时插入多条记录
    Args:
    table_name: 要插入的表名
    columns: 指明要插入的表属性，必须包含表中没有默认参数的属性，不允许为空列表
    values: 对应要插入的属性的值列表，列表里每个值要与colums对应
    Return:
    "success"
    Example:
    insert_items(table_name='person',
                columns=['name', 'age'],
                values=[['周杰伦', 30], ['马云', 35]])
    """
    assert len(columns) > 0 and len(values) > 0, "不允许使用空列表插入！"
    assert len(columns) == len(values[0]), "插入属性和值未对应！"
    connection, cursor = open_database()
    try:
        table_name = escape_string(table_name)
        col_choice = "(" + \
            ",".join(['`'+escape_string(c)+'`' for c in columns])+")"
        val_choice = []
        for value in values:
            val_choice.append("("+",".join(
                ['"'+escape_string(v)+'"' if (type(v) is str) else escape_string(str(v)) for v in value])+")")
        val_choice = ",".join(val_choice)

        sql = f"INSERT INTO {table_name} {col_choice} VALUES {val_choice};"
        print(sql)
        cursor.execute(sql)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
    return "success"


def delete_items(table_name: str,
                 where: Optional[Dict[str, Union[str, int, float]]] = None) -> str:
    r"""
    单表删除
    一次可以根据传入条件删除多条记录，注意传入where要小心，不然很容易误删
    如果指定的条件对应的记录不存在也会返回success
    Args:
    table_name: 要删除的表名
    where: 要删除的条件键值对，若为None或空字典删除整个表或所有指定的colums条目，目前只能使用=判断
    Return:
    {"code": 200, "message": "success"}
    Example:
    delete_items(table_name='person',
                 where={"name": "周杰伦", "age": 30})
    """
    connection, cursor = open_database()
    try:
        table_name = escape_string(table_name)
        where_choice = kv_to_where(where)

        sql = f"""
            DELETE
            FROM {table_name}
            WHERE {where_choice};
            """
        cursor.execute(sql)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
    return "success"


def select_items(table_name: str,
                 columns: Optional[List[str]] = None,
                 where: Optional[Dict[str, Union[str, int, float]]] = None,
                 limit: Optional[int] = None,
                 skip: int = 0,
                 use_like=False) -> List[Dict[str, Union[str, int, float]]]:
    r"""
    单表查询
    Args:
    table_name: 要查询的表名
    columns: 要查询的属性，若为None或空列表则返回全部属性
    where: 要查询的条件键值对，若为None或空字典返回整个表或所有指定的colums条目，目前只能使用=判断
    limit: 返回条目的最大数量，为None时全部返回
    skip: 返回条目的查询偏移
    Return:
    一个包含数个查询条目的列表
    Example:
    select_items(table_name='person',
                columns=['name', 'age'],
                where={'name':'周杰伦', 'age':20})
    """
    connection, cursor = open_database()
    try:
        table_name = escape_string(table_name)
        if columns is not None and len(columns) != 0:
            col_choice = ",".join(['`'+escape_string(c)+'`' for c in columns])
        else:
            col_choice = "*"
        where_choice = kv_to_where(where, use_like=use_like)
        assert (type(limit) is int and limit >=
                0) or limit is None, "limit不是非零整数或None!"
        assert type(skip) is int and skip >= 0, "skip不是非零整数!"
        sql = f"""
                SELECT {col_choice} 
                FROM {table_name} 
                WHERE {where_choice}
                """
        if limit is not None:
            sql += f"LIMIT {limit} OFFSET {skip}"
        print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        connection.close()
    return list(results)


def update_items(table_name: str,
                 items: Dict[str, Union[str, int, float]],
                 where: Optional[Dict[str, Union[str, int, float]]] = None) -> str:
    r"""
    单表更新
    Args:
    table_name: 要更新的表名
    items: 要更新的属性与值，若为None或者大小为0则不更新
    where: 要更新的条件键值对，若为None或空字典更新整个表或所有指定的colums条目，目前只能使用=判断
    Return:
    {"code": 200, "message": "success"}
    Example:
    update_items(table_name='person',
                 items={'name': 'Jay', 'age': 21},
                 where={'name': '周杰伦', 'age': 20})
    """
    connection, cursor = open_database()
    assert items is not None and len(items) > 0, "更新值不能为空！"
    try:
        table_name = escape_string(table_name)
        set_choice = kv_to_update_set(items)
        where_choice = kv_to_where(where)

        sql = f"""
            UPDATE {table_name}
            SET {set_choice}
            WHERE {where_choice};
            """
        cursor.execute(sql)
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
    return "success"



