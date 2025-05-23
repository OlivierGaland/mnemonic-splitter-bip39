# mnemonic-splitter-bip39
A simple passphrase splitter for BIP39

IMPORTANT : 
- While it is designed to be usable, this software has not been fully tested, consider using it for education purposes until it is seriously audited and tested. A bug or a security flaw could compromise your funds.
- Never trust anyone ! If you plan to use this software to secure a real asset wallet, always confirm the application is safe (check the sources or be sure the application has been audited and confirmed safe). 

This code will split a bip39 (english and 24 word only) mnemonic into 2 or more mnemonics (24 words).

It is usefull if you don't want to keep the backup in a single location (meaning if compromised you will lost access to your wallet). It can also fool anyone trying to get your mnemonic by threat as you can give him access to any of those generated mnemonics.

Once splitted in N mnemonics, you can destroy the original mnemonic and you can keep the generated mnemonics in different securized physical locations, finding one generated mnemonic won't compromise your wallet. You can also fake it is a legit wallet by putting a few $ in crypto inside.

Two algorithm are supported :

Standard : Can split your BIP-39 mnemonic into n mnemonic, ALL generated mnemonic are mandatory to recover the original. If you lose one of the generated mnemonic, you will lose access to your wallet

Shamir Secret Sharing : Can split your BIP-39 mnemonic into n mnemonic (with a pin code that can mimick a passphrase) with m mnemonic needed for the recovery (m < n), m generated mnemonic are mandatory to recover the original. This allow the loss of (n-m) menmonic while still being able to recover your wallet

Note : If the provided mnemonics for reconstruction does not meet requirement, the application will provide a passphrase not matching the original one instead of showing an error, this will fool the attacker as he won't know if he has enough share discovered. 

Files :

mnemonic_splitter.py : Launch the GUI to split and reconstruct the mnemonic

make.bat : Generate standalone executable in dist/

test/ : Several example of class usage in python if you need to customize

Technical details : generated passphrases entropy is set using the secrets (generating random secure numbers) python library

Dependancies : pip install og_log ttkbootstrap

GUI Usage :

![image](https://github.com/user-attachments/assets/6a1e3889-9d27-4426-80ee-cb20669e332f)

Split :

- Launch program (either from python or the standalone executable)

- Select language, algorithm and share count 

- Fill master mnemonic field (random generate a random one)

- Hit split to create the shares (copy will get all in clipboard, line separated)

Reconstruct : 

- Launch program (either from python or the standalone executable)

- Select language, algorithm and share count 

- Fill share fields with the share mnemonics (paste will fill all from your clipboard, one mnemonic per line)

- Hit reconstruct to get your mnemonic back

Miscellaneous :

- Multi-language : you can use the language button to convert a mnemonic from one language to another
- Length : not implemented yet (only 24 words currently) 

Tested working on windows 64bit

