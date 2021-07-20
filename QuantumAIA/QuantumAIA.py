import qsharp
from collections import Counter
from NEQR import EncodeNEQRResult

image = [
    [0, 16, 32, 48],
    [64, 80, 96, 112],
    [128, 144, 160, 176],
    [192, 208, 224, 255],
]

results = Counter()
for i in range(1024):
    result = EncodeNEQRResult.simulate(image=image)
    color = int(''.join([str(l) for l in result[7::-1]]), 2)
    y = int(''.join([str(l) for l in result[10:7:-1]]), 2)
    x = int(''.join([str(l) for l in result[13:10:-1]]), 2)

    if y < 4 and x < 4:
        results[(color, y, x)] += 1

print(results)
