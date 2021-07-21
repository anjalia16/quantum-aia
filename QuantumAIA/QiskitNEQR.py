import math
# Importing standard Qiskit libraries
from qiskit import QuantumCircuit, transpile, Aer, IBMQ
from qiskit import QuantumRegister, ClassicalRegister, execute


# Loading your IBM Quantum account(s)
provider = IBMQ.load_account()

def NEQR(image):

    intensity = QuantumRegister(8)
    y_register = QuantumRegister(math.ceil(math.log(len(image))))
    x_register = QuantumRegister(math.ceil(math.log(len(image[0]))))
    i_measurement = ClassicalRegister(8)
    y_measurement = ClassicalRegister(len(y_register))
    x_measurement = ClassicalRegister(len(x_register))
    circuit = QuantumCircuit(intensity, y_register, x_register, i_measurement, y_measurement, x_measurement)

    circuit.h(y_register)
    circuit.h(x_register)

    for y in range(0, len(image)):
        for x in range(0, len(image[0])):
            tempColor = "{0:b}".format(image[y][x])
            tempX = "{0:b}".format(x)
            tempY = "{0:b}".format(y)
            storeAlteredX = []
            storeAlteredY = []

            for num in range(0, len(tempX)):
                if tempX[num] == '0':
                    circuit.x(x_register[num])
                    storeAlteredX.append(True)
                else:
                    storeAlteredX.append(False)
            
            for num in range(0, len(tempY)):
                if tempY[num] == '0':
                    circuit.x(y_register[num])
                    storeAlteredY.append(True)
                else:
                    storeAlteredY.append(False)

            for num in range(0, len(tempColor)):
                if tempColor[num] == '1':
                    circuit.ccx(x_register[num], y_register[num], intensity[num])

            #makeshift adjoint
            for i in range(0, len(storeAlteredX)):
                if storeAlteredX[i]:
                    circuit.x(x_register[i])
            for i in range(0, len(storeAlteredY)):
                if storeAlteredY[i]:
                    circuit.x(y_register[i])

    simulator = Aer.get_backend('aer_simulator')
    simulation = execute(circuit, simulator, shots=1024)
    result = simulation.result()
    counts = result.get_counts(circuit)

    for (state, count) in counts.items():
        state_be = state[::-1]
        print(f"Measured {state_be} {count} times.")

    image1 = [
        [0, 16, 32, 48],
        [64, 80, 96, 112],
        [128, 144, 160, 176],
        [192, 208, 224, 255],
    ]







