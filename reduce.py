
def bruh(data):
    while len(data) > 1:
        print(data)
        new_data = []
        for i in range(0, len(data) - 1, 2):
            new_data.append(data[i] + data[i + 1])
        if len(data) % 2 == 1:
            new_data.append(data[-1])
        data = new_data
    return data[0]

data = [i for i in range(1,11)]
print(sum(data))
x = bruh(data)
print(x)

def kahan(data):
    sum = 0.0
    for i in range(10):
        sum = sum + data
    return sum

x = kahan(data)
print(x)