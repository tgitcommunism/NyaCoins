arr = [["qwerty 0", "ytrewq 2", "qywter 1"], [0, 2, 1]]

print(arr)

for i in range(len(arr[0])):
    for i in range(len(arr[0]) - 1):
        if arr[1][i] > arr[1][i + 1]:
            arr[1][i], arr[1][i + 1] = arr[1][i + 1], arr[1][i]
            arr[0][i], arr[0][i + 1] = arr[0][i + 1], arr[0][i]

print(arr)
