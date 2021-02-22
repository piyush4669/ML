# python -m transcrypt -b -m -n hello.py

from phe import paillier
public_key, private_key = paillier.generate_paillier_keypair()
input_1 = public_key.encrypt(-0.007)
print(private_key.decrypt(input_1))