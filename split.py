#from og_log import LOG,LEVEL
from bip39_splitter import Bip39Splitter


# INPUT PARAMETERS
PASSPHRASE = "seek service rib phone moon refuse chase cave rough annual total virus disagree knife truth math able dog online outer cram rent pull aerobic"
SPLIT_COUNT = 2


if __name__ == "__main__":

    #LOG.start()
    #LOG.level(LEVEL.warning)

    print("Splitting : "+PASSPHRASE)

    factory0 = Bip39Splitter(mnemonic=PASSPHRASE)
    l = factory0.split(SPLIT_COUNT)

    verify = []
    for i in range(0,SPLIT_COUNT):
        print(str(i)+": "+l[i])
        verify.append(l[i])

    factory1 = Bip39Splitter(mnemonic_list=verify)

    if factory0.key != factory1.key: raise Exception("ERROR: Verify error : "+hex(factory0.key)+", "+hex(factory1.key))
    print("Merge verify : OK")


