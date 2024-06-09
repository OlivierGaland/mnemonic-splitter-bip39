# mnemonic-splitter-bip39
A simple passphrase splitter for BIP39

This code will split a bip39 (english and 24 word only) passphrase into 2 or more passphrases (24 words).

It is usefull if you don't want to keep the backup in a single location (meaning if compromised you will lost access to your wallet). It can also fool anyone trying to get your passphrase by threat as you can give him access to any of those generated passphrases.

Once splitted in N passphrases, you can keep the generated passphrases in different locations, finding one generated passphrase won't compromise your wallet. You can also fake it is a legit wallet by putting a few $ in crypto inside.

IMPORTANT : To regenerate the original passphrase you need to provide the complete list of generated passphrase. This means losing one of the generated passphrase will cause complete loss of access to your wallet. This is the counterpart to this method to add a layer of security.

split.py : provide your original passphrase and the split count in the code and run it to display the generated passphrases

merge.py : provide the list of splitted passphrases and run it to get original passphrase

test.*.py : test files for DEV

Technical details : generated passphrases entropy is set using the secrets (generating random secure numbers) python library, the adding of the entropy of generated passphrases (modulus 2**256) will give the original entropy. 
