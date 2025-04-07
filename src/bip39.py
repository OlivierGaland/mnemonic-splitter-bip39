from typing import Tuple
import hashlib,secrets

from og_log import LOG

from src.tools import validate_kwargs
from src.mnemonic_words import MnemonicWords
import unicodedata


def generate_random_private_key():
    return secrets.randbelow(Bip39Secret.SECP256k1_ORDER-1)+1

class Bip39Secret():

    MNEMONIC_VALID_LENGTHS = [ 24 ]
    SECP256k1_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

    @staticmethod
    def _calculate_checksum(integer):
        #LOG.debug("calculate_checksum : Checksum : "+hex(integer))
        byte_string = integer.to_bytes((integer.bit_length() + 7) // 8, byteorder='big')
        sha256_hash = hashlib.sha256(byte_string).hexdigest()
        #LOG.debug("calculate_checksum : hash : "+sha256_hash+" : filtered hash : "+bin(int(sha256_hash[:2],16)))
        return int(sha256_hash[:2],16)

    @property
    def mnemonic(self):
        s = self._mnemonic.strip().split(" ")
        if len(s) in Bip39Secret.MNEMONIC_VALID_LENGTHS:
            if self._language == "korean": return unicodedata.normalize('NFC', self._mnemonic)
            return self._mnemonic
        raise Exception("ERROR: Wrong mnemonic length : "+str(len(s))+" : "+str(self._mnemonic))

    @property
    def key(self):
        return self._key

    @property
    def language(self):    
        return self._language
    
    @validate_kwargs({ 'mandatory' : [ 'language' ], 'exclusive' : [ 'mnemonic','key' ] })
    def __init__(self, **kwargs):
        self._language = kwargs.pop('language')
        if 'mnemonic' in kwargs: self._init_from_mnemonic(kwargs.pop('mnemonic'))
        elif 'key' in kwargs: self._init_from_key(kwargs.pop('key'))
        else: raise Exception("ERROR: Wrong parameters : "+str(kwargs))

    def _init_from_mnemonic(self,mnemonic):
        if self._language == "korean": mnemonic = unicodedata.normalize('NFD', mnemonic)
        s = mnemonic.strip().split(" ")
        if len(s) not in Bip39Secret.MNEMONIC_VALID_LENGTHS: raise Exception("ERROR: Wrong mnemonic length : "+str(len(s))+" : "+str(mnemonic))
        B = ""

        try:
            for word in s: B += f"{MnemonicWords.instance().index(self.language,word):#0{13}b}"[2:]
        except Exception as e:
            raise Exception("ERROR: Invalid mnemonic : "+str(self.language)+" ? "+str(mnemonic))   
        if len(B) != 264: raise Exception("ERROR: Wrong length : "+str(len(B)))

        P = "0b"
        for i in range(0,32): P+=B[i*8:i*8+8]
        C = "0b"+B[256:264]
        P = int(P, 2)
        C = int(C, 2)
        if Bip39Secret._calculate_checksum(P) != C: raise Exception("ERROR: Wrong checksum")

        self._mnemonic = mnemonic



        self._key = P
        LOG.debug("Init from mnemonic : "+self.mnemonic+", key : "+hex(self.key))        

    def _init_from_key(self,key):
        if key < 1 and key > Bip39Secret.SECP256k1_ORDER-1: raise Exception("ERROR: Wrong key : "+hex(key))
        self._key = key
        binary_string = bin(self.key)[2:].zfill(256)

        mnemonic = ""
        for i in range(0,23):
            s = binary_string[i*11:i*11+11]
            LOG.debug(str(i) + " : " + str(s) + " : " + str(int(s,2)) + " : " + str(MnemonicWords.instance().word(self.language,int(s,2))))
            mnemonic += MnemonicWords.instance().word(self.language,int(s,2)) + " "

        s = binary_string[253:256]+bin(Bip39Secret._calculate_checksum(self.key))[2:].zfill(8)
        LOG.debug("23 : " + str(s) + " : " + str(int(s,2)) + " : " + str(MnemonicWords.instance().word(self.language,int(s,2))))

        mnemonic += MnemonicWords.instance().word(self.language,int(s,2))
        self._mnemonic = mnemonic
        LOG.debug("Init from key : "+hex(self.key)+", mnemonic : "+self.mnemonic)



class Bip39SecretSSSShare(Bip39Secret):

    @property
    def index(self):
        if self._index is None: raise Exception("ERROR: No index")
        return self._index

    @validate_kwargs({ 'mandatory' : [ 'language' ], 'exclusive' : [ 'mnemonic','key' ] })
    def __init__(self, **kwargs):
        self._index = None
        self._language = kwargs.pop('language')
        if 'mnemonic' in kwargs: self._init_from_mnemonic_with_idx(kwargs.pop('mnemonic'))
        elif 'key' in kwargs and 'index' in kwargs: self._init_from_key_with_idx(kwargs.pop('key'),kwargs.pop('index'))
        else: raise Exception("ERROR: Wrong parameters : "+str(kwargs))

    def _init_from_mnemonic_with_idx(self,mnemonic):   
        s = mnemonic.strip().split(" ")
        if len(s)-1 not in Bip39Secret.MNEMONIC_VALID_LENGTHS: raise Exception("ERROR: Wrong mnemonic length : "+str(len(s))+" : "+str(mnemonic))
        index = int(s[-1])
        mnemonic = ' '.join(s[:-1])  
        if index < 1000 or index > 9999: raise Exception("ERROR: Wrong index : "+str(index))
        self._index = index
        LOG.debug("Init from mnemonic index : "+str(mnemonic))
        self._init_from_mnemonic(mnemonic)

    def _init_from_key_with_idx(self,key,index): 
        if index < 1000 or index > 9999: raise Exception("ERROR: Wrong index : "+str(index))
        self._index = index
        LOG.debug("Init from key index : "+str(index))
        self._init_from_key(key)




class Bip39SecretShare(Bip39Secret):
    pass

