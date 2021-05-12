#这个用于处理matplotlib所需要的中文宋体，英文Times New Roman，不要修改
def is_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True

def zhSimsun_enTNR(string):
    str_=''
    judge=0 #0表示上一个是中文
    for num in range(len(string)):
        char = string[num]
        if is_chinese(char)==True:
            if judge==0:
                str_ += char
            if judge==1:
                str_ += "}$"
                str_ += char
            judge=0
        if is_chinese(char)==False:
            if judge==0:
                str_ += "$\mathrm{"
                if char.isspace()==True:
                    str_ += "\;"
                if char.isspace()==False:
                    if char=='\u2103':
                        str_ += '^{o}C'
                    elif char=="%":
                        str_ += '\%'
                    else:
                        str_ += char
            if judge==1:
                if char.isspace()==True:
                    str_ += "\;"
                if char.isspace()==False:
                    if char=='\u2103':
                        str_ += '^{o}C'
                    elif char=="%":
                        str_ += '\%'
                    else:
                        str_ += char
            if num==len(string)-1:
                str_ += "}$"
            judge=1
    return str_