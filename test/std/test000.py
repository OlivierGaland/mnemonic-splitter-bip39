import sys
import os

# Ajouter le chemin du répertoire src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from og_log import LOG,LEVEL

from src.mnemonic_manager import MnemonicSplitter,MnemonicMerger

MNEMONIC_000 = "seek service rib phone moon refuse chase cave rough annual total virus disagree knife truth math able dog online outer cram rent pull aerobic"
PKEY_000 = 0xc31886e3d1c8f968c9a926bc412f977a43ecf77a74480048126bcea3236cab50

def main():
    LOG.info("Start")
    LOG.level(LEVEL.info)

    splitter = MnemonicSplitter(mnemonic=MNEMONIC_000)
    splitter.split(6)
    shares = splitter.mnemonic_list

    LOG.info("Mnemonic to protect : "+splitter.master.mnemonic)
    LOG.info("Private key to protect : "+hex(splitter.master.key))

    LOG.info("Split result :")
    for s in shares:
        LOG.info("Share : "+s)

    try:
        splitter.verify()
    except Exception as e:
        LOG.error("Error : "+str(e))

if __name__ == '__main__':
    LOG.start()
    main()


