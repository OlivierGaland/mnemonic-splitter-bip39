#from og_log import LOG,LEVEL
from bip39_splitter import Bip39Splitter
import secrets
from random import shuffle


if __name__ == "__main__":

    #LOG.start()
    #LOG.level(LEVEL.warning)

    COUNT = 1000

    for i in range(0,COUNT):
        
        s = secrets.randbelow(2**256)
        f0 = Bip39Splitter(key=s)
        m = f0.mnemonic
        f1 = Bip39Splitter(mnemonic=m)
        if f0.key != f1.key: raise Exception("ERROR: Wrong key : "+hex(f0.key)+", "+hex(f1.key))

        c = secrets.randbelow(9)+2
        print("\nMenemonic ======> " + f0.mnemonic)
        l = f0.split(c)
        for item in l: print(item)
        shuffle(l)

        f2 = Bip39Splitter(mnemonic_list=l)
        if f0.key != f2.key: raise Exception("ERROR: Wrong key (splitted) : "+hex(f0.key)+", "+hex(f2.key))

    print("\n"+str(COUNT)+" checked : OK")

