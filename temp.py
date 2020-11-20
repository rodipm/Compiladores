X = [10, 30, 20]

n = len(X) 

# Traverse through all array elements 
for i in range(n): 

    # Last i elements are already in place 
    for j in range(0, n-i-1): 
        nindex = j + 1
        print(X[j])
        print(X[nindex])
        if X[j] > X[nindex] : 
            print("OK")
            temp = X[j]
            X[j] = X[nindex]
            X[nindex] = temp
            print(X[j])
        print("THEN")


print(X)


# 100 DIM X(3)
# 120 LET X[0] = 10
# 130 LET X[1] = 30
# 140 LET X[2] = 20
# 150 FOR I = 0 TO 2
# 170 FOR J = 0 TO 2-I-1
# 190 LET NIDEX = J + 1
# 200 IF X[J] <= X[NIDEX] THEN 600
# 300 LET TEMP = X[J]
# 400 LET X[J] = X[NIDEX]
# 500 LET X[NIDEX] = TEMP
# 600 NEXT J
# 700 NEXT I