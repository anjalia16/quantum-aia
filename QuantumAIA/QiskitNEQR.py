import math
from qiskit import QuantumCircuit, transpile, Aer, IBMQ
from qiskit import QuantumRegister, ClassicalRegister
from qiskit import execute

def NEQR(image):

    intensity = QuantumRegister(8)
    y_register = QuantumRegister(math.ceil(math.log(len(image)) / math.log(2)))
    x_register = QuantumRegister(math.ceil(math.log(len(image[0])) / math.log(2)))
    ancillas_y = QuantumRegister(len(y_register))
    ancillas_x = QuantumRegister(len(x_register))
    i_measurement = ClassicalRegister(8)
    y_measurement = ClassicalRegister(len(y_register)) 
    x_measurement = ClassicalRegister(len(x_register))
    circuit = QuantumCircuit(intensity, y_register, x_register, ancillas_y, ancillas_x, i_measurement, y_measurement, x_measurement)

    circuit.h(y_register)
    circuit.h(x_register)

    for y in range(0, len(image)):
        for x in range(0, len(image[0])):
            binIntensity = "{0:b}".format(image[y][x])
            binX = "{0:b}".format(x)
            binY = "{0:b}".format(y)
            storeAlteredX = []
            storeAlteredY = []

            while len(binIntensity) < 8:
                binIntensity = "0" + binIntensity

            while len(binX) < len(x_register):
                binX = "0" + binX

            while len(binY) < len(y_register):
                binY = "0" + binY

            for num in range(0, len(binX)):
                if binX[num] == '0':
                    circuit.x(x_register[num])
                    storeAlteredX.append(True)
                else:
                    storeAlteredX.append(False)
            
            for num in range(0, len(binY)):
                if binY[num] == '0':
                    circuit.x(y_register[num])
                    storeAlteredY.append(True)
                else:
                    storeAlteredY.append(False)

            for num in range(0, len(binIntensity)):
                if binIntensity[num] == '1':

                    #start controlled x gate
                    if len(x_register) + len(y_register) == 2:
                        circuit.ccx(x_register[0], y_register[0], intensity[num])
                    else:
                        circuit.ccx(y_register[0], y_register[1], ancillas_y[0])
                        for i in range(2, len(y_register)):
                            circuit.ccx(y_register[i], ancillas_y[i - 2], ancillas_y[i - 1])
                        circuit.cx(ancillas_y[len(ancillas_y) - 2], ancillas_y[len(ancillas_y) - 1])
                        circuit.ccx(x_register[0], x_register[1], ancillas_x[0])
                        for i in range(2, len(x_register)):
                            circuit.ccx(x_register[i], ancillas_x[i - 2], ancillas_x[i - 1])
                        circuit.cx(ancillas_x[len(ancillas_x) - 2], ancillas_x[len(ancillas_x) - 1])

                        circuit.ccx(ancillas_x[len(ancillas_x) - 1], ancillas_y[len(ancillas_y) - 1], intensity[num])

                        circuit.cx(ancillas_x[len(ancillas_x) - 2], ancillas_x[len(ancillas_x) - 1])
                        for i in range(len(x_register) - 1, 1, -1):
                            circuit.ccx(x_register[i], ancillas_x[i - 2], ancillas_x[i - 1])
                        circuit.ccx(x_register[0], x_register[1], ancillas_x[0])
                        circuit.cx(ancillas_y[len(ancillas_y) - 2], ancillas_y[len(ancillas_y) - 1])
                        for i in range(len(y_register) - 1, 1, -1):
                            circuit.ccx(y_register[i], ancillas_y[i - 2], ancillas_y[i - 1])
                        circuit.ccx(y_register[0], y_register[1], ancillas_y[0])
                    #end controlled x gate

            #makeshift adjoint
            for i in range(0, len(storeAlteredX)):
                if storeAlteredX[i]:
                    circuit.x(x_register[i])
            for i in range(0, len(storeAlteredY)):
                if storeAlteredY[i]:
                    circuit.x(y_register[i])


    circuit.measure(intensity, i_measurement)
    circuit.measure(x_register, x_measurement)
    circuit.measure(y_register, y_measurement)
    
    #run circuit
    simulator = Aer.get_backend('aer_simulator')
    simulation = execute(circuit, simulator, shots=1024)
    result = simulation.result()
    counts = result.get_counts(circuit)
    return counts

#tests

def test1():
    image = [
        [0, 16, 32, 48],
        [64, 80, 96, 112],
        [128, 144, 160, 176],
        [192, 208, 224, 255],
    ]

    for (state, count) in NEQR(image).items():
        y = int(state[1::-1], 2)
        x = int(state[4:2:-1], 2)
        i = int(state[13:5:-1], 2)

        if x < 4 and y < 4:
            print(f"Row {x}, item {y} is {i}.")

def test2():
    image = [
    [0, 12, 24, 36],
    [48, 60, 72, 84],
    [96, 108, 130, 142],
    [154, 166, 178, 180],
    [192, 204, 216, 228]
]

    for (state, count) in NEQR(image).items():
        y = int(state[1::-1], 2)
        x = int(state[5:2:-1], 2)
        i = int(state[14:6:-1], 2)

        if x < 5 and y < 4:
            print(f"Row {x}, item {y} is {i}.")

def test3():
    image = [
        [0, 70],
        [140, 210]
    ]

    for (state, count) in NEQR(image).items():
        y = int(state[0], 2)
        x = int(state[2], 2)
        i = int(state[11:3:-1], 2)

        if x < 2 and y < 2:
            print(f"Row {x}, item {y} is {i}.")

#uncomment to run tests
#test1()
#test2()
#test3()












