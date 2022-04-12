from service.utils import generate_verification_code
def  gen_key_service(code_len=6):
    """
    随机生成六位验证码
    """
    return generate_verification_code(code_len)