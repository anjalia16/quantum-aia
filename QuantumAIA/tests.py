from collections import Counter
from math import ceil, log2
from NEQR import EncodeNEQRResult
import qsharp
import time
from typing import List

ITR = 1024
images = [
    # 4x4 increasing grayscale test
    [
        [0, 16, 32, 48],
        [64, 80, 96, 112],
        [128, 144, 160, 176],
        [192, 208, 224, 255]
    ],
    # 6x8 same color
    [
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8,
    ]

]

def get_results_qs(iterations : int, image : List[List[int]]) -> Counter:
    """
    Returns results of running NEQR encoding multiple times on the Q# implementation
    """
    y_size : int = len(image)
    x_size : int = len(image[0])
    b_y : int = ceil(log2(y_size))
    b_x : int = ceil(log2(x_size))
    results = Counter()
    for i in range(iterations):
        result = EncodeNEQRResult.simulate(image=image)
        color = int(''.join([str(l) for l in result[7::-1]]), 2)
        y = int(''.join([str(l) for l in result[7 + b_y:7:-1]]), 2)
        x = int(''.join([str(l) for l in result[7 + b_y + b_x: 7 + b_x:-1]]), 2)

        if y < y_size and x < x_size:
            results[(color, y, x)] += 1
    return results

def get_results_qiskit(iterations :int, image) -> Counter:
    """
    Returns all the results of running qiskit multiple times mon 
    """
    pass

def verify_results(results : Counter, image : List[List[int]]) -> bool:
    corrects : List[List[bool]] = [[False for pixel in row] for row in image]

    passing : bool = True

    for (color, y, x) in list(results):
        if not (0 <= y < len(image) and 0 <= x < len(image[0])):
            print("(row, col) found among the results is out of bounds")
            passing = False
        elif image[y][x] == color:
            corrects[y][x] = True
        else:
            print("Position", y, x, "(row, col) has incorrect color",color,"which should be",image[y][x])
            passing = False

    for row in corrects:
        for item in row:
            if not item:
                print("Position",y,x,"(row, col) was not found among the results")
                passing = False

    return passing

def test():
    for i, image in enumerate(images):
        start = time.time()
        qs_result = get_results_qs(ITR, image)
        end = time.time()
        # qiskit_result = get_results_qiskit(ITR, image)
        print("Q# test",i,"passed" if verify_results(qs_result, image) else "failed","in",end-start,"ms")
        print("Results (color, row, col): # of measurements")
        print(qs_result)
        print()
        # print("Q# test",i,"passed" if verify_results(qiskit_result, image) else "failed")

if __name__ == "__main__":
    test()