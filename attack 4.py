import feal4 as feal
import csv

# Linear Approximation Equation
def linear_approximation(P_L, P_R, C_L, C_R, k1):
    left_side = (P_L >> 16 & 1) ^ (P_L >> 26 & 1) ^ (P_R >> 24 & 1) ^ feal.fM(k1, P_L^P_R) >> 24 & 1
    left_side ^= (C_L >> 16 & 1) ^ (C_L >> 26 & 1) ^ (C_R >> 24 & 1)
    return left_side == 0

def count_bias(filename, k1):
    count = 0
    total = 0

    # Read the CSV file
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            plaintext = int(row[0], 16)
            ciphertext = int(row[1], 16)
            
            P_L = (plaintext >> 32) & 0xFFFFFFFF
            P_R = plaintext & 0xFFFFFFFF
            C_L = (ciphertext >> 32) & 0xFFFFFFFF
            C_R = ciphertext & 0xFFFFFFFF

            if linear_approximation(P_L, P_R, C_L, C_R, k1):
                count += 1
            total += 1
    return count / total if total > 0 else 0

def find_best_k1(filename):
    best_bias = 0
    best_k1 = 0
    max_distance = 0

    # Iterate over all possible 14-bit combinations for bits 18-31
    for bits in range(0, 2**14):
        # Construct k1 by setting only bits 18-31
        k1 = bits << 18  # Shift the 14 bits to positions 18-31

        # Calculate bias for this k1
        bias = count_bias(filename, k1)

        # Calculate the distance from the range [0.45, 0.55]
        if bias < 0.45:
            distance = 0.45 - bias
        elif bias > 0.55:
            distance = bias - 0.55
        else:
            # Bias is within the range, so skip this k1
            continue

        # Update best k1 if this distance is higher
        if distance > max_distance:
            max_distance = distance
            best_k1 = k1
            best_bias = bias
            print(f"New best k1: {hex(k1)} with bias: {best_bias} (distance: {distance})")

    return best_k1, best_bias

# Example usage
filename = "pair.csv"
best_k1, best_bias = find_best_k1(filename)
print(f"Best k1: {hex(best_k1)} with bias: {best_bias}")