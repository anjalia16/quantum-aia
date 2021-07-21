import qsharp
import time
import QiskitNEQR

from collections import Counter
from math import ceil, log2
from NEQR import EncodeNEQRResult
from qiskit import Aer, execute, IBMQ, QuantumCircuit, transpile 
from typing import List

IBMQ.load_account()

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
        [1] * 8,
        [2] * 8,
        [3] * 8,
        [4] * 8,
        [5] * 8,
    ]

]

def get_results_qs(iterations : int, image : List[List[int]]) -> Counter:
    """
    Returns all the results of measuring the NEQR image encoded with the Q# implementation.

    Parameters
        iterations -> int: The number of times to measure the NEQR encoded image. Higher is slower, but is more likely to find all the encoded pixels.
        image -> List[List[int]]: The image to encode and measure.
    Returns
        Counter: A Counter collections object containing all the measurements. Key is in (color, y, x), value is the number of measurements.
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

def get_results_qiskit(iterations :int, image : List[List[int]]) -> Counter:
    """
    Returns all the results of measuring the NEQR image encoded with the Qiskit implementation.

    Parameters
        iterations -> int: The number of times to measure the NEQR encoded image. Higher is slower, but is more likely to find all the encoded pixels.
        image -> List[List[int]]: The image to encode and measure.
    Returns
        Counter: A Counter collections object containing all the measurements. Key is in (color, y, x), value is the number of measurements.
    """
    circuit : QuantumCircuit = QiskitNEQR.NEQR(image) 
    simulator = Aer.get_backend('aer_simulator')
    circuit = transpile(circuit, backend=simulator, optimization_level=2)
    simulation = execute(circuit, simulator, shots=iterations)
    result = simulation.result()
    counts = result.get_counts(circuit)

    y_size : int = len(image)
    x_size : int = len(image[0])
    b_y : int = ceil(log2(y_size))
    b_x : int = ceil(log2(x_size))
    #output
    resultc = Counter()
    for (state, count) in counts.items():

        x = int(state[b_x - 1::-1], 2)
        y = int(state[b_x + b_y:b_x - 1:-1], 2)
        i = int(state[b_x + b_y + 9:b_x + b_y:-1], 2)

        if x < x_size and y < y_size:
            resultc[(i, y, x)] = count
    return resultc

def verify_results(results : Counter, image : List[List[int]]) -> bool:
    """
    Verifies that all the measurement results have valid positions and all positions were found, 
    in addition to matching colors.

    Parameters:
        results -> Counter: results from either get_results_qiskit() or get_results_qs() to compare to the image
        image -> List[List[int]]: the image to verify results on
    Returns:
        bool: True if the results are valid and match the image, False otherwise
    """
    founds : List[List[bool]] = [[False for pixel in row] for row in image]

    passing : bool = True

    for (color, y, x) in list(results):
        if not (0 <= y < len(image) and 0 <= x < len(image[0])):
            print("(row, col) found among the results is out of bounds")
            passing = False
        elif image[y][x] == color:
            founds[y][x] = True
        else:
            print("Position", y, x, "(row, col) has incorrect color",color,"which should be",image[y][x])
            passing = False
            founds[y][x] = True

    for row in founds:
        for item in row:
            if not item:
                print("Position",y,x,"(row, col) was not found among the results")
                passing = False

    return passing

def test() -> None:
    """
    Iterates through all of the globally defined images, encodes them with both Q# and Qiskit, and verifies the results.
    Outputs if it passed or failed, and the time it took to do so.
    """
    for i, image in enumerate(images):
        start = time.time()
        qs_result = get_results_qs(ITR, image)
        end = time.time()
        print("Q# test",i,"passed" if verify_results(qs_result, image) else "failed","in",end-start,"ms")
        print("Results (color, row, col): # of measurements")
        print(qs_result)

        start = time.time()
        qiskit_result = get_results_qiskit(ITR, image)
        end = time.time()
        print("Qiskit test",i,"passed" if verify_results(qiskit_result, image) else "failed","in",end-start,"ms")
        print("Results (color, row, col): # of measurements")
        print(qiskit_result)
        print()
        

if __name__ == "__main__":
    test()