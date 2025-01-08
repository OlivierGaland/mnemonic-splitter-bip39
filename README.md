# mnemonic-splitter-bip39
A simple passphrase splitter for BIP39

IMPORTANT : While it is designed to be usable, this software has not been fully tested, consider using it for education purposes until it is seriously audited and tested. A bug or a security flaw could compromise your funds.  

This code will split a bip39 (english and 24 word only) passphrase into 2 or more passphrases (24 words).

It is usefull if you don't want to keep the backup in a single location (meaning if compromised you will lost access to your wallet). It can also fool anyone trying to get your passphrase by threat as you can give him access to any of those generated passphrases.

Once splitted in N passphrases, you can keep the generated passphrases in different physical locations, finding one generated passphrase won't compromise your wallet. You can also fake it is a legit wallet by putting a few $ in crypto inside.

Two algorithm are supported :

Standard : Can split your BIP-39 mnemonic into n mnemonic, ALL generated mnemonic are mandatory to recover the original. If you lose one of the generated mnemonic, you will lose access to your wallet

Shamir Secret Sharing : Can split your BIP-39 mnemonic into n mnemonic (with a pin code that can mimick a passphrase) with m mnemonic needed for the recovery (m < n), m generated mnemonic are mandatory to recover the original. This allow the loss of (n-m) menmonic while still being able to recover your wallet

mnemonic_splitter.py : Launch the GUI to split and reconstruct the mnemonic

make.bat : Generate standalone executable in dist/

Technical details : generated passphrases entropy is set using the secrets (generating random secure numbers) python library

GUI Example :

![image](https://github.com/user-attachments/assets/a40c522f-2593-481b-b221-529c7c507b41)


