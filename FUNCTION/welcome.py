import random
from DATA.Brain_DATA.DLG_DATA.dlg import welcomedlg
from HEAD.mouth import speak


def welcome():
    welcome = random.choice(welcomedlg)
    speak(welcome)
    
