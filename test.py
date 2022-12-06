from passlib.hash import pbkdf2_sha256

password=pbkdf2_sha256.hash("scott")

mypass="dada"


if pbkdf2_sha256.verify("scottd",password):
    print("ues")
    
