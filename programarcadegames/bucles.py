"""
Escribe el código para conseguir:
0 1 2 3 4 5 6 7 8 9
0 1 2 3 4 5 6 7 8 9
0 1 2 3 4 5 6 7 8 9
0 1 2 3 4 5 6 7 8 9
0 1 2 3 4 5 6 7 8 9
0 1 2 3 4 5 6 7 8 9
0 1 2 3 4 5 6 7 8 9
0 1 2 3 4 5 6 7 8 9
0 1 2 3 4 5 6 7 8 9
0 1 2 3 4 5 6 7 8 9    
"""
def bucles():
    for i in range(10):
        for j in range(10):
            print(j, end=" ") 
        print()

"""" 
Ajusta el programa anterior para obtener:
0 0 0 0 0 0 0 0 0 0 
1 1 1 1 1 1 1 1 1 1 
2 2 2 2 2 2 2 2 2 2 
3 3 3 3 3 3 3 3 3 3 
4 4 4 4 4 4 4 4 4 4 
5 5 5 5 5 5 5 5 5 5 
6 6 6 6 6 6 6 6 6 6 
7 7 7 7 7 7 7 7 7 7 
8 8 8 8 8 8 8 8 8 8 
9 9 9 9 9 9 9 9 9 9 
"""
def bucles2():
    for i in range(10):
        for j in range(10):
            print(i, end=" ") 
        print()

"""
Escribe el código que imprimirá esto:
0
0 1
0 1 2
0 1 2 3
0 1 2 3 4
0 1 2 3 4 5
0 1 2 3 4 5 6
0 1 2 3 4 5 6 7
0 1 2 3 4 5 6 7 8
0 1 2 3 4 5 6 7 8 9
"""
def bucles3():
    for i in range(11):
        for j in range(i):
            print(j, end=" ") 
        print()

""" 
Escribe el código para conseguir:
0 1 2 3 4 5 6 7 8 9
  0 1 2 3 4 5 6 7 8
    0 1 2 3 4 5 6 7
      0 1 2 3 4 5 6
        0 1 2 3 4 5
          0 1 2 3 4
            0 1 2 3
              0 1 2
                0 1
                  0
""" 
def bucles4():
    f = 10
    for i in range(10):
        for j in range(f):
            print(j, end=" ") 
        f -= 1
        print("\n"," "*(i+i),end=" ")


if __name__ == "__main__":
    # bucles()
    # bucles2()
    # bucles3()
    bucles4()