from transformation import transformation
import time

last_transformation = {0: [8, 7, 6, 5, 4, 3, 2, 1], 1: [4, 1, 2, 3, 6, 7, 8, 5], 2: [1, 7, 2, 4, 5, 3, 6, 8], 3: [4, 1, 2, 3, 6, 7, 8, 5], 4: [6, 5, 8,
7, 2, 1, 4, 3], 5: [5, 1, 8, 6, 3, 7, 2, 4], 6: [1, 3, 6, 4, 5, 7, 2, 8], 7: [5, 8, 2, 7, 6, 3, 1, 4], 8: [8, 3, 2, 5, 4, 7, 6, 1]
, 9: [4, 1, 2, 3, 6, 7, 8, 5], 10: [6, 5, 8, 7, 2, 1, 4, 3], 11: [5, 1, 8, 6, 3, 7, 2, 4], 12: [6, 5, 8, 7, 2, 1, 4, 3], 13: [2, 3
, 4, 1, 8, 5, 6, 7], 14: [3, 5, 4, 2, 7, 1, 8, 6], 15: [5, 7, 2, 6, 3, 1, 8, 4], 16: [3, 4, 8, 1, 2, 7, 5, 6], 17: [4, 7, 8, 3, 6,
 1, 2, 5], 18: [1, 7, 2, 4, 5, 3, 6, 8], 19: [5, 8, 6, 3, 2, 7, 1, 4], 20: [8, 7, 6, 5, 4, 3, 2, 1], 21: [5, 8, 6, 3, 2, 7, 1, 4],
 22: [2, 4, 1, 7, 6, 8, 5, 3], 23: [4, 8, 1, 2, 3, 7, 6, 5], 24: [8, 3, 2, 5, 4, 7, 6, 1], 25: [4, 1, 6, 7, 2, 3, 8, 5], 26: [1, 3
, 6, 4, 5, 7, 2, 8]}
sequency_of_methods = 13

before = time.time()
for i in range(0, 10_000_000):
    transformation(last_transformation[3], 1)

after = time.time()
print(f'it took {after - before} seconds to excute the function')

# v1.0 for 10_000_000 times
# it took 8.629139423370361 seconds to excute the function
# v2.0
# it took 6.631270408630371 seconds to excute the function