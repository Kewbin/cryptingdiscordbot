from cryptography.fernet import Fernet


key = 'Pmgzg9fQGFXnA4bUAf1yubBDQBjSYDWqZ7ERrfIYZa4='
text = 'gAAAAABdSatcvDpw4kAvED8ZohBtnIdL_NBsKaBUGY8MYJKZfaJsHdEDU4R33nmuyo1bCgSC3NXQI2PMgfH4n5edCLEunEByNC5Wz24riU48sIeBTk7dJpiAtuzN54X2E2QJqioEroNV_nQ72z70PW_HNANGnnoKUQ=='
f = Fernet(key)
token = f.decrypt(text.encode()).decode("utf-8").replace('\n','') 


