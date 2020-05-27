from cryptography.fernet import Fernet

# -------------- USE THIS FOR GENERATING THE KEY
# key = Fernet.generate_key()
# print(key)

# -------------- USE THIS FOR BEGINNING OF THE DATABASE
# AUTH_KEY = 'PUT YOUR KEY HERE'
# with open('database.json', 'r') as inputFile:
#     dec_dtb = inputFile.read()
#     crypter = Fernet(AUTH_KEY)
#     enc_dtb = crypter.encrypt(dec_dtb.encode())
#     with open('database2.json', 'wb') as outputFile:
#         outputFile.write(enc_dtb)
