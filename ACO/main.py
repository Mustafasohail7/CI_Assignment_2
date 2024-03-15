import sys
from ACO import ACO
import matplotlib.pyplot as plt

iterations = 0

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
    print(i)


best_sols = sol[0]
avg_sols = sol[1]
iterations = range(1,11)
plt.plot(iterations, best_sols, label='Best Solutions')

# Plotting the average solutions
plt.plot(iterations, avg_sols, label='Average Solutions')

# Adding labels and title
plt.xlabel('Generations')
plt.ylabel('Solutions')
plt.title('Best and Average Solutions over Generations for queen11_11.col')

# Restricting x-axis and y-axis to display only integers
plt.xticks(range(min(iterations), max(iterations)+1))
plt.yticks(range(int(min(best_sols)), int(max(best_sols))+1))

# Adding legend
plt.legend()

# Displaying the plot
plt.show()