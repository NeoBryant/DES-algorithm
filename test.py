#coding=utf-8
# 测试文件
from src.Des import Des

text = input("the text is : ") # 输入要进行加密或者解密的文本
password = input("the password is : ") # 输入8位的密码
mode = input("the mode is (E/D): ") # 输入加密或者解密状态，E->加密，D->解密
Des(text, password, mode)


