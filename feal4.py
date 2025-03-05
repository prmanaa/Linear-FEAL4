import random
import csv

# FEAL-4 S-Box approximation function using the SA and SB operations
def rol2(x):
    return ((x << 2) & 0xFF) | (x >> 6)

# SA(x, y) = ROL2(x + y + 1) % 256
# SB(x, y) = ROL2(x + y) % 256
def SAC(x, y):
    return rol2((x + y + 1) % 256)

def SBD(x, y):
    return rol2((x + y) % 256)

# XOR operation
def XOR(x, k):
    return x ^ k

# Rotation operation
def SD(x):
    return rol2(x)

# FEAL-4 f function
def fM(k, x):
    x0 = (x >> 24) & 0xFF
    x1 = (x >> 16) & 0xFF
    x2 = (x >> 8) & 0xFF
    x3 = x & 0xFF

    k0 = (k >> 24) & 0xFF
    k1 = (k >> 16) & 0xFF
    k2 = (k >> 8) & 0xFF
    k3 = k & 0xFF

    row_3 = XOR(x3, x2)
    row_3 = XOR(row_3, k2)
    row_3 = SAC(row_3, ((x1 ^ k1) ^ (x0 ^ x1)))

    row_2 = (x1 ^ k1) ^ (x0 ^ x1)
    row_2 = SBD(row_3, row_2)

    row_1 = XOR(x0, k0)
    row_1 = SAC(row_1, row_2)

    row_4 = XOR(k3, x3)
    row_4 = SBD(row_4, row_3)

    return (row_1 << 24) | (row_2 << 16) | (row_3 << 8) | row_4

# FEAL-4 Encryption Function with k5 and k6
def feal4_encrypt(plaintext, k1, k2, k3, k4, k5, k6):
    L = (plaintext >> 32) & 0xFFFFFFFF
    R = plaintext & 0xFFFFFFFF

    # Round before
    R ^= L

    # Round 1
    L ^= fM(k1, R)
    
    # Round 2
    R ^= fM(k2, L)
    
    R ^= k6

    # Additional operation with k5
    L ^= k5
    
    # Round 3
    L ^= fM(k3, R)
    
    # Round 4
    R ^= fM(k4, L)

    # Final swap
    L ^= R

    return (R << 32) | L
