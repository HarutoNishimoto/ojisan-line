

def transReply(utterance, user_name):

    Ulist = utterance.split("|")

    for i, val in enumerate(Ulist):
        if val == "NAME":
            Ulist[i] = user_name
        if "0x" in val:
            Ulist[i] = chr(int(val, 16))

    Ulist = ''.join(Ulist)

    return Ulist

if __name__ == '__main__':

    pass

