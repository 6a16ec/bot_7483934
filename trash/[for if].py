abc = ["1234", "345", "1344"]
first = [string[0] for string in abc]
first_1 = [string[0] for string in abc if string[0] == "1"]

print (first, first_1)