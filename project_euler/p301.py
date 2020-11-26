# nimsum = n1 XOR n2 XOR n3
# for this problem:
#    nimsum = n ^ (2*n) ^ (3^n)
# we notice that nimsum not zero when '11' occurs in bin(n1)
# f(1) = {0, 1} = 2
# f(2) = {00, 01, 10} = 3      #(no 11)
# f(3) = '0' * {00, 01, 10} + '1' * '0' * {0, 1} = 3 + 2 = 5
#                                    ^ no 1 after 1  


l = [0,2,3]

for i in range(30):
    l.append(l[-1]+l[-2])

print(l[30])