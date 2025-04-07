import secrets
from itertools import permutations

from og_log import LOG,LEVEL

from src.bip39 import Bip39Secret,Bip39SecretShare
from src.tools import validate_kwargs

class MnemonicSplitter():

    @property
    def mnemonic_list(self):
        return [share.mnemonic for share in self.shares]

    @property
    def key_list(self):
        return [share.key for share in self.shares]

    def __init__(self, **kwargs):
        self.shares = []
        self.master = Bip39Secret(**kwargs)

    def split(self, shares):
        LOG.info("Make "+str(shares)+" random shares")
        self.shares = []
        if shares < 2: raise Exception("ERROR: Wrong count : "+str(shares))

        k_list = []
        k = self.master.key
        while len(k_list) < shares - 1:
            r = secrets.randbelow(Bip39Secret.SECP256k1_ORDER-1)+1
            nk = (k-r) % Bip39Secret.SECP256k1_ORDER
            if nk == 0 or r in k_list: continue
            k_list.append(r)
            k = nk
        k_list.append(k)

        for item in k_list:
            self.shares.append(Bip39Secret(key=item,language=self.master.language))


    def verify(self):
        if len(self.shares) == 0: raise Exception("ERROR: No share found")

        all_permutations = list(permutations(self.mnemonic_list))
        all_permutations_as_lists = [list(p) for p in all_permutations]

        for permutation in all_permutations_as_lists:
            merger = MnemonicMerger(mnemonic_list=permutation,language=self.master.language)
            merger.merge()
            if merger.key != self.master.key or merger.mnemonic != self.master.mnemonic:
                raise Exception("ERROR: Wrong permutation : "+str(permutation))
            
        LOG.info("Verify mnemonic reconstruction : success !")


class MnemonicMerger():

    @property
    def key(self):
        if self._result is None: raise Exception("ERROR: Not merged yet")
        return self._result.key
    
    @property
    def mnemonic(self):
        if self._result is None: raise Exception("ERROR: Not merged yet")
        return self._result.mnemonic
    
    @property
    def language(self):
        return self._language

    @validate_kwargs({ 'mandatory' : [ 'language' ], 'exclusive' : [ 'mnemonic_list'] })
    def __init__(self, **kwargs):
        self._language = kwargs.pop('language')
        if 'mnemonic_list' in kwargs: self._init_from_mnemonic_list(kwargs.pop('mnemonic_list'))
        else: raise Exception("ERROR: Wrong parameters : "+str(kwargs))

    def _init_from_mnemonic_list(self,mnemonic_list):
        self.mnemonic_list = []
        for mnemonic in mnemonic_list:
            self.mnemonic_list.append(Bip39SecretShare(mnemonic=mnemonic,language=self.language))

    def merge(self):
        key = 0x0
        for item in self.mnemonic_list:
            key += item.key
            key = key % Bip39Secret.SECP256k1_ORDER
        self._result = Bip39Secret(key=key,language=self.language)










