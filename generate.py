import random
import csv
import feal4 as feal

# Generate 1000 plaintext-ciphertext pairs
samples = 100
k1 = 0xf6b5b8ab
k2 = 0b10000110101101011011111010101011
k3 = 0b11111110101101011111100010100001
k4 = 0b10010110101101011011100010101011
k5 = 0b11111111101101011111110010100001
k6 = 0b00000110101101011011111010111111

pairs = []

for _ in range(samples):
    plaintext = random.getrandbits(64)
    ciphertext = feal.feal4_encrypt(plaintext, k1, k2, k3, k4, k5, k6)
    pairs.append((plaintext, ciphertext))

# Store pairs in CSV file
filename = "pair.csv"

with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Plaintext", "Ciphertext"])
    for plaintext, ciphertext in pairs:
        writer.writerow([hex(plaintext), hex(ciphertext)])

print('Generated')