import os
import random

class BlackBox(object):
    
    def __init__(self):
        len_ = random.randint(100, 1000)
        self._passwd = os.urandom(len_)

    def check(self, user_passwd):
        if len(user_passwd) != len(self._passwd):
            return "Error:len"
        for i in range(len(user_passwd)):
            if user_passwd[i] != self._passwd[i]:
                return "Error:idx:%d" % i
        return "OK"
    
class SecureBlackBox(object):
    
    def __init__(self):
        len_ = random.randint(100, 1000)
        self._passwd = os.urandom(len_)
        self.count_flag = 0

    def check(self, user_passwd):
        if self.count_flag > 5:
            print("Incorrect password entered 5 times. Account locked.")
            exit(1)
        
        if len(user_passwd) != len(self._passwd):
            self.count_flag += 1
            return "Error:len"
        for i in range(len(user_passwd)):
            if user_passwd[i] != self._passwd[i]:
                self.count_flag += 1
                return "Error:idx:%d" % i
        return "OK"
    
if __name__ == "__main__":
    
    LEN_ERROR = "Error:len"
    CHAR_ERROR = "Error:idx:"
    OK_STATUS = "OK"
    
    passwd_len = -1
    user_passwd = b""
    
    blackbox = BlackBox()
    
    ## Checking length of password
    for i in range(100, 1001):
        user_passwd = int("0").to_bytes(1, 'little') * i
        status = blackbox.check(user_passwd)
        if status != LEN_ERROR:
            passwd_len = i
            print(f"Length of password: {passwd_len}")
            break
    
    ## Cracking the actual password
    curr_idx = 0
    byte_arr_user_passwd = bytearray(user_passwd)
    
    while curr_idx < passwd_len:
        for i in range(0,256):
            byte_arr_user_passwd[curr_idx] = i
            user_passwd = bytes(byte_arr_user_passwd)       
            
            status = blackbox.check(user_passwd)
            
            if CHAR_ERROR in status:            
                err_idx = int(status.lstrip(CHAR_ERROR))

                if err_idx > curr_idx:
                    curr_idx = err_idx                    
                    break
                
            if status == OK_STATUS:
                curr_idx += 1
                break            
            
    print(f"Password: {user_passwd}")