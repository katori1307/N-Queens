import random

#đọc input từ file .txt
with open("Input.txt","r") as file:
    lines = file.readlines()

max_weight = int(lines[0])
max_class = int(lines[1])

input = lines[2].split()
weight = [int(num) for num in input]

input = lines[3].split()
value = [int(num) for num in input]

input  = lines[4].split()
item_class = [int(num) for num in input]
    
# tạo các biến toàn cục cần thiết
n = len(weight)
generations = 50 #số lần thực hiện các bước trong giải thuật di truyền.
population_size = 100 # kích thước quần thể
better_choice_size = 20 # kích thước tập các cá thể có độ fitness cao

# tạo 1 cá thể là 1 list các giá trị 0, 1. 0 tức là đồ vật không được chọn, 1 tức là đồ vật được chọn
def create_individual():
    individual = [random.randint(0,1) for i in range(n)]
    return individual

# tạo 1 quần thể là nhiều cá thể với kích thước là population_size
def generate_population():
    population = [create_individual() for i in range(population_size)]
    return population

# độ fitness là tổng value, đồng thời kiểm tra xem tổng weight có vượt max_weight hay không
def process_fitness(individual):
    sum_value = sum(value[i] for i in range(n) if individual[i] != 0)
    sum_weight = sum(weight[i] for i in range(n) if individual[i]!=0)
    if sum_weight > max_weight:
        return 0
    else:
        return sum_value

# reverse = true để được sort theo thứ tự giảm dần với evaluation function là process_fitness
def selection(population):
    better_choices = sorted(population, key=process_fitness, reverse= True)
    return better_choices[:better_choice_size]

def cross_over(parent1, parent2):
    position = random.randint(0,n-1)
    child1 = parent1[:position] + parent2[position:]
    child2 = parent2[:position] + parent1[position:]
    return child1, child2

def mutation(individual):
    pos = random.randint(0,n-1)
    if(individual[pos]):
        individual[pos] = 0
    else:
        individual[pos] = 1
    return individual

def knapsack_genetic_alg():
    population = generate_population()
    for i in range(generations):
        better_choices = selection(population)
        children = []
        while len(children)< population_size - len(better_choices):
            parent1, parent2 = random.choices(population,k=2)
            child1, child2 = cross_over(parent1,parent2)
            child1 = mutation(child1)
            child2 = mutation(child2)
            children.append(child1)
            children.append(child2)
        population = better_choices + children
    for i in range(len(population)):
        individual = population[i]
        check_list = [item_class[j] for j in range(n) if individual[j]!=0]
        flag = True
        for j in range(n):
            if item_class[j] not in check_list:
                flag = False
        if flag == True:
            return individual
    

if __name__ == "__main__":
    print("max weight = ",max_weight)
    print("class = ", max_class)
    print(weight)
    print(value)
    print(item_class)
    print(n)
    print("Best solution: ")
    best_fitness = knapsack_genetic_alg()
    print("Best value:", process_fitness(best_fitness))
    print(best_fitness)
    




