description:
challenge-CFT-cipher.txt contains the base64 encoded XOR encrypted secret text
the text contains the flag (see below)

# create flag hash
import hashlib
m = hashlib.sha256()
m.update(b"Natural")
m.hexdigest()
--> flag:
mucctf{song} with song = Natural
mucctf{e22163187924a32113f3c2bec434c0089c15b5be4e2ea3d67c6106404177580b}

#create flag for Vigenere Cipher Challenge
The flag is mucctf{361b5c512b91325faef4a1e2ad70df84f3588c243e7053b14f7a4072b4eda4be}
>>> import hashlib
>>> m = hashlib.sha256()
>>> m.update(b"SimpleCiphersAreNotCool")
>>> m.hexdigest()
'361b5c512b91325faef4a1e2ad70df84f3588c243e7053b14f7a4072b4eda4be'
>>> 

