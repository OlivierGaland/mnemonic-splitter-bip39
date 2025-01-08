import sys
import os

# Ajouter le chemin du répertoire src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from og_log import LOG,LEVEL

from src.mnemonic_sss_manager import MnemonicSSSSplitter
from src.bip39 import generate_random_private_key

NB_SHARES = 5
NB_MINIMAL_SHARES = 3
COUNT = 100              # 1.5 tps (5,3)

def main():

    LOG.info("Start stress test for MnemonicSplitter and MnemonicMerger : n = "+str(NB_SHARES)+" , m = "+str(NB_MINIMAL_SHARES)+" , count = "+str(COUNT))
    LOG.level(LEVEL.info)

    try:
        for i in range(COUNT):
            LOG.stop()
            s = MnemonicSSSSplitter(key=generate_random_private_key())
            s.split(NB_SHARES,NB_MINIMAL_SHARES)
            s.verify(NB_SHARES,NB_MINIMAL_SHARES)
            LOG.start()
        LOG.info("Count "+str(i+1)+" : Success, split in "+str(NB_SHARES)+" shares")
    except Exception as e:
        LOG.start()
        LOG.error("Error : "+str(e))


if __name__ == '__main__':
    LOG.start()
    main()


