s = "open book challenge"
f = []
def reverse_str(s):
    rev = s.split(" ")
    for w in rev:
        w = w[::-1]
        f.append(w)
    return f

q = reverse_str(s)
for y in q:
    print(y, end=" ")

##########################################
# s = "GeeksforGeeks"
# rev = ''.join(reversed(s))
# print(rev)
#############################################
# s = "GeeksforGeeks"
# rev = ""

# for c in s:
#     rev = c + rev
# print(rev)
###########################################
# var1 = "Geeks"
# var2 = "forGeeks"

# print("".join((var1, var2)))

# var3 = " ".join([var1, var2])
# print(var3)
########################################