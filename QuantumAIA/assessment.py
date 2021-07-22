from qiskit import Aer, transpile, execute
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


def resourceAssessment(image, sim, num, op_lvl, run_on_real):
    start = perf_counter()
    circuit = QiskitNEQR.NEQR(image)
    qc = transpile(circuit, backend=sim, optimization_level=op_lvl)
    end = perf_counter()

    if run_on_real:
        simulation = execute(qc, backend=sim, shots=num)
        results = simulation.result()

    print()
    print(f"Running resource assessment on the following image for {sim}:")
    for row in image:
        print(row)
    print()
    print(f"Circuit compiled in {end - start} seconds.")
    print(f"Circuit depth: {qc.depth()}")
    print(f"Necessary number of qubits: {qc.width()}")
    if run_on_real:
        print()
        print(f"Running the circuit with {num} shots.")
        print(f"Runtime: {results.time_taken} seconds.")
    print("-------------------------------------------------------------------------------")

def runAssessments(shots, optimization_level, run_real):
    for i in images:
        resourceAssessment(i, simulator_manhattan, shots, optimization_level, run_real)
        resourceAssessment(i, simulator_ideal, shots, optimization_level, True)

runAssessments(1024, 1, run_real=False)