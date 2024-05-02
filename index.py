import os


def GetIndexUser():
    os.system("cls" or "clear")
    quest = str(input("""
        ____________________
        |   REGISTRER  [1] |
        |     LOGIN    [2] |          
        |     EXIT     [3] |
        --------------------
:"""))
    while quest not in "123":
        os.system("cls" or "clear")
        quest = str(input("""
        ____________________
        |   REGISTRER  [1] |
        |     LOGIN    [2] |          
        |     EXIT     [3] |
        --------------------
:"""))  

GetIndexUser()