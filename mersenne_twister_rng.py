# Mersenne Twister random number generator

MT = [0]*624
index = 0

def initialize_generator(seed):
    index = 0
    MT[0] = seed
    for i in range(1, 624):
        MT[i] = (1812433253 *  (MT[i-1] ^ (MT[i-1]>>30)) + i) & 0xffffffff

def extract_number():
    if index == 0:
        generate_numbers()

    y = MT[index]
    y = y ^ (y >> 11)
    y = y ^ ((y << 7) & 0x9d2c5680)
    y = y ^ ((y << 15) & 0xefc60000)
    y = y ^ (y >> 18)

    return y

def generate_numbers():
    for i in range(0, 624):
        y = (MT[i] & 0x80000000) + (MT[(i+1) % 624] & 0x7fffffff)
        MT[i] = MT[(i+397) % 624] ^ (y >> 1)
        if (y % 2 != 0):
            MT[i] = MT[i] ^ 0x9908b0df


