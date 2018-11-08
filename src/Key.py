#coding=utf-8
# 用列表处理二进制数
# 置换表下标从1开始
# PC_1置换表，56位
PC_1_table = [57,49,41,33,25,17,9,
        1,58,50,42,34,26,18,
        10,2,59,51,43,35,27,
        19,11,3,60,52,44,36,
        63,55,47,39,31,23,15,
        7,62,54,46,38,30,22,
        14,6,61,53,45,37,29,
        21,13,5,28,20,12,4]

# PC_2置换表，48位
PC_2_table = [14,17,11,24,1,5,
        3,28,15,6,21,10,
        23,19,12,4,26,8,
        16,7,27,20,13,2,
        41,52,31,37,47,55,
        30,40,51,45,33,48,
        44,49,39,56,34,53,
        46,42,50,36,29,32]

class Key(object):
    # 初始化
    def __init__(self, key_str):
        self.key = [0 for i in range(64)] # 存储最终的64为密匙，包含奇偶校验位
        self.subkey = [[0 for i in range(48)] for j in range(16)] # key的16个子key
        self.Cs = [[0 for i in range(28)] for j in range(17)]  # 存储C0-C16
        self.Ds = [[0 for i in range(28)] for j in range(17)] # 存储D0-D16
        
        self.generate_key(key_str) # 生成密匙
        self.generate_subkey() # 生成子密匙

    '''
        通过字符串key_str，进行encode，使其成为元素为0/1的列表
        self.key
    '''
    def generate_key(self, key_str): # 生成64位密匙
        key_bytes = key_str.encode('utf-8') # key从密码str转为bytes类型
        for i in range(len(key_bytes)): # 得到最终的64位key，len(key_bytes)=8
            key_binary = list(bin(key_bytes[i]))
            for j in range(7):
                if key_binary[j*(-1)]=='0': self.key[i*8+j] = 0
                else: self.key[i*8+j] = 1
            if sum(self.key[i*8:i*8+7])%2==1: self.key[i*8+7] = 0
            else: self.key[i*8+7] = 1


    ''' 
        对self.key进行PC-1置换
        然后进行16次迭代，生成Li和Di
    '''
    def generate_subkey(self): # 生成子密匙，并存储
        self.PC_1_substitution() # PC_1置换
        for i in range(1, 17): # 进行16次迭代T，对于每一次迭代
            self.Cs[i] = self.LS(i, self.Cs[i-1])
            self.Ds[i] = self.LS(i, self.Ds[i-1])
            self.PC_2_substitution(i-1, self.Cs[i]+self.Ds[i]) # 进行PC_2置换

            
    def PC_1_substitution(self): # 进行PC_1置换
        for i in range(len(PC_1_table)):
            if (i < 28): self.Cs[0][i] = self.key[PC_1_table[i]-1]
            else: self.Ds[0][i-28] = self.key[PC_1_table[i]-1]

    
    def PC_2_substitution(self, i, A): # 对56位的A列表进行PC_2置换，返回一个48位的列表K
        for j in range(len(self.subkey[i])):
            self.subkey[i][j] = A[PC_2_table[j]-1]
        
        
    def LS(self, i, A): #对二进制串左移，即对列表A(A长度为28)形式进行左移，若i=1、2、9、16则循环左移一位，否则循环左移2位
        res = A.copy();
        if i == 1 or i == 2 or i == 9 or i ==16: bit_lshift = 1 # 左移位数，1位
        else: bit_lshift = 2 # 左移2位
        for j in range(len(A)):
            if j < len(A)-bit_lshift: res[j] = A[j+bit_lshift]
            else: res[j] = A[j-28+bit_lshift]
        return res
    
    def get_subkey(self, i): # i取值为[1,16]
        return self.subkey[i-1]
    