#coding=utf-8
from src.Key import Key

#IP初始置换表，64位
IP_table = [58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,
            62,54,46,38,30,22,14,6,64,56,48,40,32,24,16,8,
            57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,
            61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7]

#IP逆置换表，64位
IP_reverse_table = [40,8,48,16,56,24,64,32,39,7,47,15,55,23,63,31,
                    38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,
                    36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,
                    34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25]
#E扩展置换表，48位
E_table = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,
            12,13,12,13,14,15,16,17,16,17,18,19,20,21,20,21,
            22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1]

#P置换表，32位
P_table = [16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,
            2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25]

#S盒表，每个盒子为4*16
S_box = [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7, # S1_box
        0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8,
        4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0,
        15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13],
        [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10, # S2_box
        3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5,
        0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15,
        13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9],
        [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8, # S3_box
        13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1,
        13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7,
        1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12],
        [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15, # S4_box
        13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9,
        10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4,
        3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14],
        [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9, # S5_box
        14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6,
        4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14,
        11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3],
        [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11, # S6_box
        10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8,
        9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6,
        4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13],
        [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1, # S7_box
        13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6,
        1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2,
        6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12],
        [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7, # S8_box
        1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2,
        7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8,
        2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]

class SubDes(object):
    def __init__(self, m_str, K, mode): # m_str为64位二进制字符串，K为Key对象，mode为加密或解密
        self.M = [int(i) for i in list(m_str)] # 64位明文块M
        self.K = K # K为Key对象
        self.mode = mode # 加密或解密，E/D
        self.Ls = [[0 for i in range(32)] for j in range(17)]
        self.Rs = [[0 for i in range(32)] for j in range(17)]


    def generate_C(self):
        self.IP_init_substitution() # 初始置换IP 
        r_itr = self.iterate_16_T() # 16轮迭代T
        r_IP_rev = self.IP_reverse_substitution(r_itr) # 逆置换IP^-1
        # list 转换为 二进制字符串
        list2liststring = [str(i) for i in r_IP_rev]
        string = ''.join(list2liststring)
        return string


    def IP_init_substitution(self): # 初始置换IP
        temp = []
        for i in range(len(IP_table)):
            temp.append(self.M[IP_table[i]-1])
        self.Ls[0]=temp[:32]
        self.Rs[0]=temp[32:]
        

    def iterate_16_T(self): #16轮迭代T，mode取值E/D，表示加密还是解密
        if self.mode=='E': # 加密
            for i in range(1, 17): # i取[1,16]
                self.Ls[i] = self.Rs[i-1].copy()
                self.Rs[i] = self.xor_list(self.Ls[i-1], self.feistel_round_function(self.Rs[i-1], self.K.get_subkey(i)))
        else:  # 解密
            for i in range(1, 17): # i取[16,1]
                self.Ls[i] = self.Rs[i-1].copy()
                self.Rs[i] = self.xor_list(self.Ls[i-1], self.feistel_round_function(self.Rs[i-1], self.K.get_subkey(17-i)))
        return self.Rs[16]+self.Ls[16]


    def xor_list(self, list1, list2): #list的异或操作
        res = []
        for i in range(len(list1)):
            res.append(1) if list1[i]!=list2[i] else res.append(0)
        return res


    def feistel_round_function(self, R, K): # feistel轮函数，R为32位，K为48位
        ER = self.E_extend(R) # 1 首先对R做E扩展
        R_xor = self.xor_list(ER, K) # 2 使ER和K做异或运算
        R_S_box = [] # 3 将R_xor分为8组，每组6位，R_S用来存储S盒转换后的值
        for i in range(8): 
            temp_R = R_xor[i*6:i*6+6] # 6位的分组
            res_R = self.S_box_transition(temp_R, i+1) # S-box处理后的4位串
            R_S_box.extend(res_R) #循环后是32位 串
        return self.P_substitution(R_S_box)


    def E_extend(self, R): # E-扩展，R为32位扩展位48位的ER
        ER = []
        for i in range(len(E_table)):
            ER.append(R[E_table[i]-1])
        return ER

    def S_box_transition(self, R, i): # S盒6-4转化，R为6位的串，转换为4位
        n = R[0]*2+R[5]  # 行号,0-3
        m = R[1]*8+R[2]*4+R[3]*2+R[4] # 列号,0-15
        num = S_box[i-1][n*16+m]  # Si-box, 第n行，第m列
        res = [0 for i in range(4)] # 4位二进制数
        for i in range(4): # 转化为二进制数列表
            res[i] = int(num/(2**(3-i)))
            num %= (2**(3-i))
        return res


    def P_substitution(self, R): # P-置换
        res = []
        for i in range(len(P_table)):
            res.append(R[P_table[i]-1])
        return res


    def IP_reverse_substitution(self, R): # 初始置换IP
        res = []
        for i in range(len(IP_reverse_table)):
            res.append(R[IP_reverse_table[i]-1])
        return res