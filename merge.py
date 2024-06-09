#from og_log import LOG,LEVEL
from bip39_splitter import Bip39Splitter

# INPUT PARAMETERS
PASSPHRASE_LIST = [
    "mandate praise limit school ritual deputy evil jeans width high hidden tide jacket cool drip glow tuition giraffe breeze pear island fault spare letter",
    "despair boy dad tired steak jungle suffer public scrap over kidney bargain sick episode pluck cement bid taxi leg will rookie girl system matrix"
]

if __name__ == "__main__":

    #LOG.start()
    #LOG.level(LEVEL.warning)

    print("Merging : ")

    for i in range(0,len(PASSPHRASE_LIST)):
        print(str(i)+": "+PASSPHRASE_LIST[i])

    factory0 = Bip39Splitter(mnemonic_list=PASSPHRASE_LIST)

    print("Merged : "+factory0.mnemonic)

