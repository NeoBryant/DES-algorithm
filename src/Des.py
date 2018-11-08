#coding=utf-8
''' 
This is a encryption and decryption system exec file
English words only!
Attention: python3
'''
from src.SubDes import SubDes
from src.Key import Key

class Des(object):
    def __init__(self, text_str, key_str, mode_str):
        self.key = Key(key_str) # 密匙key_str为8位字节，key为密匙对象
        self.mode = mode_str # 模式为E->加密，D->解密
        self.text = text_str # 待处理的文本，若为加密模式，则text为字母或数字字符串，若为解密，则text为二进制字符串

        if (self.mode=='E'): # 加密时
            self.plaintext_process()
        else: #解密时
            self.ciphertext_process()

    def plaintext_process(self): # 对明文进行处理，转换为64位list
        #-----------------按PKCS#5规范进行填充
        plaintext_list = []
        # 在utf-8下，每个字母或数字为一个字节，这里不处理汉字
        num_byte_need = 8 - len(self.text)%8 # 需要填充的字节数
        bytes_text = self.text.encode('utf-8') #bytes类型 [int,int,int,...]
        for byte in bytes_text: #对每个byte
            plaintext_list.extend(self.byte2bytelist(byte))
        if num_byte_need==0: # 最后的分组够8个字节，填充8个08字节
            for i in range(8):
                plaintext_list.extend(['0','0','0','0','1','0','0','0'])
        else: #最后的分组不够8个字节，填充n个0n字节
            for i in range(num_byte_need):
                plaintext_list.extend(self.byte2bytelist(num_byte_need))
        
        #---------------分组进行处理-----------------
        C_bin_string = '' # 秘文二进制字符串
        for i in range(int(len(plaintext_list)/64)):
            sub_plaintext_list = plaintext_list[i*64:(i+1)*64]
            sub_string = ''.join(sub_plaintext_list)
            sub_des = SubDes(sub_string, self.key, self.mode).generate_C()
            C_bin_string += sub_des

        print("the binary ciphertext is : "+C_bin_string)
            
    def ciphertext_process(self): # 对密文进行处理，转换为64位list
        M_bin_string = '' # 明文二进制字符串
        for i in range(int(len(self.text)/64)):
            sub_text = self.text[i*64:(i+1)*64]
            sub_des = SubDes(sub_text, self.key, self.mode).generate_C()
            M_bin_string += sub_des

        #-----------将二进制码转化为可读字符串---------------
        m_string = self.binstr2str(M_bin_string) #明文
        print("The plaintext is : " + m_string)


    def byte2bytelist(self, byte): # byte为int类型
        bin_string = bin(byte)[2:] # bin的返回值位string，例：'0b1010111'，截断为'1010111'
        bin_string_list = list(bin_string) # 字符串列表，['1','0',...]
        while len(bin_string_list)!=8:
            bin_string_list.insert(0, '0')
        return bin_string_list


    def binstr2str(self, string): # 将二进制字符串转换为bytes类型，再decode
        bytes_list = []
        for i in range(int(len(string)/8)):
            sub_str = string[i*8:(i+1)*8]
            num = int(sub_str,2)
            if num <= 8: break
            bytes_list.append(num)
        bts = bytes(bytes_list)
        res = bts.decode('utf-8')
        return res