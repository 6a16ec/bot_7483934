
test = (1, 2, 3, 4)
print(test)
print(test[0])

abc = []
abc.append(None)
abc.append(None)
abc.append(None)
print(abc)

print(str(True))

for i, element in enumerate(abc):
    print(i, element)

print(type(abc) is dict)

a = {}
a[9] = 7
a[2] = 8
a[6] = 4
print(a.get(66))


a = ["1", "2", "3"]
b = ["a", "b", "c"]

for i in zip(a, " ", b):
    print(i)

print("njdf {abc} kdf".format(abc = 1))

array = {}
array[0] = 1
array["3"] = "4"
print(list(array.keys()))
