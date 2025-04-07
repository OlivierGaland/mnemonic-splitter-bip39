import hashlib,sys
from og_log import LOG

class MnemonicWords:
    _instance = None

    # MNEMONICS_FILES_DATA = {
    #     'english': ('english.txt', '2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda'),
    #     'chinese_simplified': ('chinese_simplified.txt', '5c5942792bd8340cb8b27cd592f1015edf56a8c5b26276ee18a482428e7c5726'),
    #     'spanish': ('spanish.txt', '46846a5a0139d1e3cb77293e521c2865f7bcdb82c44e8d0a06a2cd0ecba48c0b'),
    #     'french': ('french.txt', 'ebc3959ab7801a1df6bac4fa7d970652f1df76b683cd2f4003c941c63d517e59'),
    #     'italian': ('italian.txt', 'd392c49fdb700a24cd1fceb237c1f65dcc128f6b34a8aacb58b59384b5c648c2'),
    #     'japanese': ('japanese.txt', '2eed0aef492291e061633d7ad8117f1a2b03eb80a29d0e4e3117ac2528d05ffd'),
    #     'korean': ('korean.txt', '9e95f86c167de88f450f0aaf89e87f6624a57f973c67b516e338e8e8b8897f60'),
    #     'portuguese': ('portuguese.txt', '2685e9c194c82ae67e10ba59d9ea5345a23dc093e92276fc5361f6667d79cd3f'),
    #     'czech': ('czech.txt', '7e80e161c3e93d9554c2efb78d4e3cebf8fc727e9c52e03b83b94406bdcc95fc'),
    #     'chinese_traditional': ('chinese_traditional.txt', '417b26b3d8500a4ae3d59717d7011952db6fc2fb84b807f3f94ac734e89c1b5f'),
    # }

    MNEMONICS_DATA = {
        'english': { 'file': 'english.txt', 'hash': '2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda', 'lines': 3  },
        'chinese_simplified': { 'file': 'chinese_simplified.txt', 'hash': '5c5942792bd8340cb8b27cd592f1015edf56a8c5b26276ee18a482428e7c5726', 'lines': 2  },
        'spanish': { 'file': 'spanish.txt', 'hash': '46846a5a0139d1e3cb77293e521c2865f7bcdb82c44e8d0a06a2cd0ecba48c0b', 'lines': 3  },
        'french': { 'file': 'french.txt', 'hash': 'ebc3959ab7801a1df6bac4fa7d970652f1df76b683cd2f4003c941c63d517e59', 'lines': 3  },
        'italian': { 'file': 'italian.txt', 'hash': 'd392c49fdb700a24cd1fceb237c1f65dcc128f6b34a8aacb58b59384b5c648c2', 'lines': 3  },
        'japanese': { 'file': 'japanese.txt', 'hash': '2eed0aef492291e061633d7ad8117f1a2b03eb80a29d0e4e3117ac2528d05ffd', 'lines': 3  },
        'korean': { 'file': 'korean.txt', 'hash': '9e95f86c167de88f450f0aaf89e87f6624a57f973c67b516e338e8e8b8897f60', 'lines': 4  },
        'portuguese': { 'file': 'portuguese.txt', 'hash': '2685e9c194c82ae67e10ba59d9ea5345a23dc093e92276fc5361f6667d79cd3f', 'lines': 3  },
        'czech': { 'file': 'czech.txt', 'hash': '7e80e161c3e93d9554c2efb78d4e3cebf8fc727e9c52e03b83b94406bdcc95fc', 'lines': 3  },
        'chinese_traditional': { 'file': 'chinese_traditional.txt', 'hash': '417b26b3d8500a4ae3d59717d7011952db6fc2fb84b807f3f94ac734e89c1b5f', 'lines': 2 },
    }

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def instance(cls):
        return cls._instance or cls()

    @property
    def supported_languages(self):
        return list(MnemonicWords.MNEMONICS_DATA.keys())
    
    @property
    def default_language(self):
        return self.supported_languages[0]

    def __init__(self):
        self.words_dict = {}
        for lang, data in MnemonicWords.MNEMONICS_DATA.items():
            LOG.debug(f"Loading {lang} words")   
            self._load_words(lang, data)
        
    def _load_words(self, lang, data):

        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS + '/src/mnemonics/'    # For generated exe : copy data files
        else:
            base_path = './src/mnemonics/'

        #file_path = './src/mnemonics/' + data['file']
        file_path = base_path + data['file']
        with open(file_path, 'r', encoding='utf-8') as file: self.words_dict[lang] = file.read().splitlines()
        if self._calculate_file_hash(file_path) != self.MNEMONICS_DATA[lang]['hash']: raise Exception(f"{data['file']} hash incorrect")
    
    def _calculate_file_hash(self, file_path):
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as file:
            for byte_block in iter(lambda: file.read(4096), b""): sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def word(self, lang, index):
        if lang in self.words_dict:
            words = self.words_dict[lang]
            if 0 <= index < len(words):
                return words[index]
        return None
    
    def index(self, lang, word):
        if lang in self.words_dict:
            words = self.words_dict[lang]
            if word in words:
                return words.index(word)
        return None

    def get_lines(self, lang):
        return MnemonicWords.MNEMONICS_DATA[lang]['lines']

# # Exemple d'utilisation


# # Créer l'objet avec les fichiers
# mnemonic = MnemonicWords()

# # Exemple de récupération d'un mot pour l'anglais à l'index 0
# word = mnemonic.get_word('chinese_simplified', 0)
# print(f"Premier mot en chinese_simplified: {word}")

# # Exemple de récupération de l'index d'un mot pour l'anglais
# index = mnemonic.get_index('chinese_simplified', word)
# print(f"Index du mot '{word}' en chinese_simplified: {index}")

# print(mnemonic.supported_languages)
# print(mnemonic.default_language)

