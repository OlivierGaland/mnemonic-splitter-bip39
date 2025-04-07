import secrets
from itertools import permutations

from og_log import LOG,LEVEL

from src.bip39 import Bip39Secret,Bip39SecretSSSShare
from src.tools import validate_kwargs

class MnemonicSSSSplitter():

    @property
    def mnemonic_list(self):
        return [share.mnemonic for share in self.shares]
    
    @property
    def mnemonic_with_index_list(self):
        return [(str(share.mnemonic)+" "+str(share.index)) for share in self.shares]

    @property
    def key_list(self):
        return [share.key for share in self.shares]

    def __init__(self, **kwargs):
        self.shares = []
        self.master = Bip39Secret(**kwargs)

    @staticmethod
    def _eval_at(poly, x):
        """Evaluates polynomial (coefficient tuple) at x, used to generate a
        shamir pool in make_random_shares below.
        """
        accum = 0
        for coeff in reversed(poly):
            accum *= x
            accum += coeff
            accum %= Bip39Secret.SECP256k1_ORDER
        return accum
    

    def split(self, shares, minimum):
        """
        Generates a random shamir pool for a given secret, returns share points.
        """
        if minimum > shares: raise Exception("ERROR: Too many minimum shares requested. Minimum: "+str(minimum)+" > Shares: "+str(shares))
        if minimum < 3: raise Exception("ERROR: Too few minimum shares requested. Minimum: "+str(minimum))

        LOG.info("Make "+str(shares)+" random shares, minimum share requested : "+str(minimum))


        self.shares = []
        poly = [self.master.key] + [secrets.randbelow(Bip39Secret.SECP256k1_ORDER-1)+1 for i in range(minimum - 1)]

        x_list = set()
        while len(x_list) < shares:
            x = secrets.randbelow(9000) + 1000  # Générer un nombre entre 1000 et 9999
            x_list.add(x)
    
        points = [(MnemonicSSSSplitter._eval_at(poly, i),i) for i in list(x_list)]

        for secret in points:
            LOG.debug("Share "+str(secret[1])+" : "+hex(secret[0]))
            self.shares.append(Bip39SecretSSSShare(key=secret[0],index=secret[1],language=self.master.language))


    def verify(self,shares, minimum):
        if len(self.shares) == 0: raise Exception("ERROR: No share found")

        all_permutations = []
        for r in range(1, len(self.mnemonic_with_index_list) + 1):
            all_permutations.extend(list(permutations(self.mnemonic_with_index_list, r)))
        all_permutations_as_lists = [list(p) for p in all_permutations]

        for permutation in all_permutations_as_lists:
            if len(permutation) > 2:
                merger = MnemonicSSSMerger(mnemonic_list=permutation,language=self.master.language)
                merger.merge()
                if len(permutation) > minimum - 1 and len(permutation) < shares + 1:
                    if merger.key == self.master.key and merger.mnemonic == self.master.mnemonic: continue
                else:
                    if merger.key != self.master.key and merger.mnemonic != self.master.mnemonic: continue
                raise Exception("ERROR: Wrong permutation "+str(len(permutation))+"/"+str(shares)+" : "+str(permutation))
            
        LOG.info("Verify mnemonic reconstruction : success !")


class MnemonicSSSMerger:

    @property
    def key(self):
        if self._result is None: raise Exception("ERROR: Not merged yet")
        return self._result.key
    
    @property
    def mnemonic(self):
        if self._result is None: raise Exception("ERROR: Not merged yet")
        return self._result.mnemonic

    @property
    def key_with_index_list(self):
        return [(share.key,share.index) for share in self.mnemonic_list]
    
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
            self.mnemonic_list.append(Bip39SecretSSSShare(mnemonic=mnemonic,language=self.language))

    @staticmethod
    def _extended_gcd(a, b):
        """
        Division in integers modulus p means finding the inverse of the
        denominator modulo p and then multiplying the numerator by this
        inverse (Note: inverse of A is B such that A*B % p == 1). This can
        be computed via the extended Euclidean algorithm
        http://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Computation
        """
        x = 0
        last_x = 1
        y = 1
        last_y = 0
        while b != 0:
            quot = a // b
            a, b = b, a % b
            x, last_x = last_x - quot * x, x
            y, last_y = last_y - quot * y, y
        return last_x, last_y

    @staticmethod
    def _divmod(num, den, p):
        """Compute num / den modulo prime p

        To explain this, the result will be such that:
        den * _divmod(num, den, p) % p == num
        """
        inv, _ = MnemonicSSSMerger._extended_gcd(den, p)
        return num * inv

    @staticmethod
    def _lagrange_interpolate(x, x_s, y_s, p):
        """
        Find the y-value for the given x, given n (x, y) points;
        k points will define a polynomial of up to kth order.
        """
        k = len(x_s)
        assert k == len(set(x_s)), "points must be distinct"
        def PI(vals):  # upper-case PI -- product of inputs
            accum = 1
            for v in vals:
                accum *= v
            return accum
        nums = []  # avoid inexact division
        dens = []
        for i in range(k):
            others = list(x_s)
            cur = others.pop(i)
            nums.append(PI(x - o for o in others))
            dens.append(PI(cur - o for o in others))
        den = PI(dens)
        num = sum([MnemonicSSSMerger._divmod(nums[i] * den * y_s[i] % p, dens[i], p)
                for i in range(k)])
        return (MnemonicSSSMerger._divmod(num, den, p) + p) % p

    def merge(self):
        """
        Recover the secret from share points
        (points (x,y) on the polynomial).
        """
        self._result = None
        if len(self.mnemonic_list) < 3:
            raise Exception("ERROR: Not enough shares to merge : "+str(len(self.mnemonic_list)))
        y_s, x_s = zip(*self.key_with_index_list)
        self._result = Bip39Secret(key=MnemonicSSSMerger._lagrange_interpolate(0, x_s, y_s, Bip39Secret.SECP256k1_ORDER),language=self.language)

