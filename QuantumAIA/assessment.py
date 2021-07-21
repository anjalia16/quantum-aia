from qiskit import Aer, transpile 
from qiskit.providers.aer import AerSimulator
from time import perf_counter
from qiskit.test.mock import FakeManhattan
import QiskitNEQR

images = [
    [
        [0, 16, 32, 48],
        [64, 80, 96, 112],
        [128, 144, 160, 176],
        [192, 208, 224, 255]
    ],
    [
        [0] * 8,
        [1] * 8,
        [2] * 8,
        [3] * 8,
        [4] * 8,
        [5] * 8,
    ],
    [
        [0, 12, 24, 36],
        [48, 60, 72, 84],
        [96, 108, 130, 142],
        [154, 166, 178, 180],
        [192, 204, 216, 228]
    ],
    [
        [0, 70],
        [140, 210]
    ]
]

simulator_manhattan = AerSimulator.from_backend(FakeManhattan())
simulator_ideal = Aer.get_backend('aer_simulator')


def practicalityAssessmentManhattan(image):
    start = perf_counter()
    circuit = QiskitNEQR.NEQR(image)
    qc = transpile(circuit, backend=simulator_manhattan, optimization_level=1)
    end = perf_counter()

    print()
    print("Running practicality assessment on the following image for Manhattan:")
    print(image)
    print()
    print(f"Circuit compiled in {end - start} seconds.")
    print(f"Circuit depth: {qc.depth()}")
    print(f"Necessary number of qubits: {qc.width()}")
    print("-------------------------------------------------------------------------------")

def practicalityAssessmentIdeal(image):
    start = perf_counter()
    circuit = QiskitNEQR.NEQR(image)
    qc = transpile(circuit, backend=simulator_ideal, optimization_level=1)
    end = perf_counter()

    print()
    print("Running practicality assessment on the following image for an ideal quantum computer:")
    print(image)
    print()
    print(f"Circuit compiled in {end - start} seconds.")
    print(f"Circuit depth: {qc.depth()}")
    print(f"Necessary number of qubits: {qc.width()}")
    print("-------------------------------------------------------------------------------")

def runAssessments():
    for i in images:
        practicalityAssessmentManhattan(i)
        practicalityAssessmentIdeal(i)

runAssessments()