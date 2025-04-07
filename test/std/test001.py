import sys
import os

# Ajouter le chemin du répertoire src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import random

from og_log import LOG,LEVEL

from src.mnemonic_manager import MnemonicSplitter,MnemonicMerger

MNEMONIC_000 = "seek service rib phone moon refuse chase cave rough annual total virus disagree knife truth math able dog online outer cram rent pull aerobic"
LANGUAGE_000 = "english"
PKEY_000 = 0xc31886e3d1c8f968c9a926bc412f977a43ecf77a74480048126bcea3236cab50

def main():
    LOG.info("Start")
    LOG.level(LEVEL.info)

    s = MnemonicSplitter(mnemonic=MNEMONIC_000,language=LANGUAGE_000)
    s.split(4)
    shares = s.mnemonic_list

    LOG.info("Mnemonic to protect : "+s.master.mnemonic)
    LOG.info("Private key to protect : "+hex(s.master.key))

    LOG.info("Split result :")
    for s in shares:
        LOG.info("Share : "+s)

    LOG.info("===> TEST 1 <===")
    count = 4
    LOG.info("Reconstructming Mnemonic with "+str(count)+" shares : ")
    shares_sample = random.sample(shares,count)

    for s in shares_sample:
        LOG.info("Using share : "+s)

    m = MnemonicMerger(mnemonic_list=shares_sample,language=LANGUAGE_000)
    m.merge()
    LOG.info("Merged mnemonic : "+m.mnemonic)
    LOG.info("Merged private key : "+hex(m.key))
    LOG.info("Success !" if m.mnemonic == MNEMONIC_000 else "Failure !")

    LOG.info("===> TEST 2 <===")
    count = 3
    LOG.info("Reconstructing Mnemonic with "+str(count)+" shares : ")
    shares_sample = random.sample(shares,count)

    for s in shares_sample:
        LOG.info("Using share : "+s)

    m = MnemonicMerger(mnemonic_list=shares_sample,language=LANGUAGE_000)
    m.merge()
    LOG.info("Merged mnemonic : "+m.mnemonic)
    LOG.info("Merged private key : "+hex(m.key))
    LOG.info("Success !" if m.mnemonic == MNEMONIC_000 else "Failure !")


if __name__ == '__main__':
    LOG.start()
    main()


