#from og_log import LOG,LEVEL
from bip39_splitter import Bip39Splitter
import secrets

if __name__ == "__main__":

    #LOG.start()
    #LOG.level(LEVEL.warning)

    COUNT = 10000

    for i in range(0,COUNT):
        s = secrets.randbelow(2**256)
        f0 = Bip39Splitter(key=s)
        m = f0.mnemonic
        f1 = Bip39Splitter(mnemonic=m)
        if f0.key != f1.key: raise Exception("ERROR: Wrong key : "+hex(f0.key)+", "+hex(f1.key))

    print(str(COUNT)+" checked : OK")

