from random import randint

def generateCode():
    code = ''.join(str(randint(0, 9)) for _ in range(6))
    return code



