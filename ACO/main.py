import sys
from ACO import ACO

def main_test():
    num_ants = 10
    iterations = 10
    alpha = 1
    beta = 3
    evaporation_rate = 0.8
    return ACO("queen11_11.col",num_ants,iterations,alpha,beta,evaporation_rate).solve()


def main():
    filename = sys.argv[1]
    num_ants = int(sys.argv[2])
    iterations = int(sys.argv[3])
    alpha = float(sys.argv[4])
    beta = float(sys.argv[5])
    evaporation_rate = float(sys.argv[6])
    return ACO(filename,num_ants,iterations,alpha,beta,evaporation_rate).solve()


if sys.argv[1] == "test":
    sol = main_test()
else:
    sol = main()

print("Colors Needed")
for i in sol[0]:
    print(i[0])