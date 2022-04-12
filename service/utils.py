from typing import List
import re
import random

# local_ip = "http://121.36.59.23"
local_ip = "http://127.0.0.1"
port = 8000
rsc = "/resources"

def get_url(path: str, file_type: str, id: str) -> str:
    r"""
    获取资源路径的url
    Example:
    {"path":"/audio/appreciation/", "file_type":"mp3","id":"1"} => "http://121.36.59.23/resources/audio/appreciation/1.mp3"
    """
    return local_ip+":"+str(port)+rsc+path+id+"."+file_type


def split_options(result: List[dict]) -> List[dict]:
    r"""
    将返回结果中的选项字符串拆开
    Examble:
    [
    {
        "id": 1,
        "type": "单选",
        "description": "关关雎鸠，在河之洲。窈窕淑女，君子好逑。参差荇菜，_______。窈窕淑女，________。",
        "option": "A. 左右采之；琴瑟友之 B. 左右流之；寤寐求之 C. 左右采之；寤寐求之 D. 左右流之；求之不得",
        "answer": "B",
        "explanation": "略",
        "theme": "诗句填空"
    }
    ]
    =>
    [
    {
        "id": 1,
        "type": "单选",
        "description": "关关雎鸠，在河之洲。窈窕淑女，君子好逑。参差荇菜，_______。窈窕淑女，________。",
        "option": ["左右采之；琴瑟友之",
                    "左右流之；寤寐求之",
                    "左右采之；寤寐求之",
                    "左右流之；求之不得"
                    ],
        "answer": "B",
        "explanation": "略",
        "theme": "诗句填空"
    }
    ]
    """
    alphas = "".join([chr(ord("A")+i)+"|" for i in range(26)])
    alphas = alphas[:-1]
    for que in result:
        options = que["option"]
        options = re.split(alphas, options)[1:]  # 去除第一个空字符
        for i in range(len(options)):
            options[i] = options[i].replace(".", "").replace("、", "").strip()
        que["option"] = options
    return result

code_list = [str(i) for i in range(10)]
code_list.extend([chr(i) for i in range(ord('A'),ord('Z')+1)])

def generate_verification_code(code_len=6):
    ''' 随机生成6位的验证码 '''
    myslice = random.sample(code_list,  code_len)   # 从list中随机获取6个元素，作为一个片断返回
    verification_code = ''.join(myslice)  # list to string
    return verification_code
