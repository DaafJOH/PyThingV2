
import sys
sys.tracebacklimit = 2
def init(kaas: int):
    try:
        kaas * kaas
    except: 
        raise TypeError

init("kaas=1")