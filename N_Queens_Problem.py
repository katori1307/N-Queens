import  time, tracemalloc
import heapq
import random
from queue import PriorityQueue


class Queens_UCS:
    def __init__(self, state=None):
        if state is None:
            self.state = []
        else:
            self.state = state
            self.cost = self.get_cost(self.state)
    
    # hàm đếm số lượng cặp quân hậu tấn công nhau
    def count_attacking_pairs(self, state):
        cost = 0
        # 2 vòng lặp để xét từng quân hậu so với các quân hậu còn lại
        for i in range(len(state)):
            for j in range(i+1, len(state)):
                #nếu 2 quân hậu cùng 1 dòng hoặc hiệu số dòng của 2 quân hậu = j - i (trên cùng 1 đường chéo) thì 2 quân hậu ăn nhau được
                if state[i] == state[j] or state[i] - state[j] == j - i or state[j] - state[i] == j - i:
                    cost += 1
        return cost
    
    def get_cost(self, state):
        return self.count_attacking_pairs(state)
    
    def is_goal(self):
        return self.cost == 0
    
    def move_queen(self, queen_num, point):
        self.state[queen_num] = point
        self.cost = self.count_attacking_pairs(self.state)
    
    def __lt__(self, other):
        return self.cost < other.cost
    

    def UCS(self):
        #sử dụng priority queue để lưu các trạng thái, bắt đầu với trạng thái đầu tiên
        state_list = PriorityQueue()
        state_list.put(self)
        while not state_list.empty():
            current_queens = state_list.get()
            #kiểm tra xem trạng thái hiện tại có đến đích chưa
            if current_queens.is_goal():
                return current_queens.state
            #dùng 2 vòng lặp để lần lượt tạo các successor bằng cách di chuyển quân hậu thứ i sang dòng j
            for i in range(len(current_queens.state)):
                for j in range(len(current_queens.state)):
                    if i!=j:
                        new_state = list(current_queens.state)
                        new_state[i] = j #di chuyển quân hậu thứ i sang hàng j
                        new_queens = Queens_UCS(new_state)
                        #chỉ thêm vào state_list các trạng thái có cost < trạng thái đang xét
                        if(new_queens.cost<current_queens.cost):
                            state_list.put(new_queens)


class Queens_Astar:
    def __init__(self, state):
        self.state = state

    def count_attacking_pair(self,state):
        count =0
        # 2 vòng lặp để xét từng quân hậu so với các quân hậu còn lại
        for i in range(len(state)):
            for j in range(i+1,len(state)):
                #nếu 2 quân hậu cùng 1 dòng hoặc hiệu số dòng của 2 quân hậu = j - i (trên cùng 1 đường chéo) thì 2 quân hậu ăn nhau được
                if state[i]==state[j] or state[i]-state[j]==j-i or state[j]-state[i]==j-i:
                    count+=1
        return count
    

    def generate_successors(self,state):
        successor_list = []
        #2 vòng lặp để lần lượt di chuyển quân hậu ở cột i sang hàng j
        for i in range(len(state)):
            for j in range(len(state)):
                if j == state[i]:
                    continue
                else:
                    successor = list(state)
                    successor[i] = j
                    successor_list.extend([successor])
        return successor_list
    
    def is_goal(self,state):
        return self.count_attacking_pair(state)==0
    
    def A_Star(self,start_state):
        #hàm A* với hereustic là số cặp quân hậu tấn công nhau
        list_state = [(self.count_attacking_pair(start_state),start_state)]
        visited = set()
        #lần lượt xét các trạng thái trong list_state sử dụng heapq
        while list_state:
            current_node = heapq.heappop(list_state)
            #lấy trạng thái (là phần tử thứ 2 trong node)
            current_state = current_node[1]
            #kiểm tra xem có là goal hay chưa
            if(self.is_goal(current_state)):
                return current_state
            visited.add(tuple(current_state))
            #lần lượt xét các successor của trạng thái hiện tại
            for successor in self.generate_successors(current_state):
                tmp = tuple(successor)
                #nếu successor không trong visited thì mới được đưa vào list_state
                if tmp not in visited:
                    #tính toán giá trị hereustic và push vào trong 
                    num_of_attacking_pairs = self.count_attacking_pair(current_state)
                    heapq.heappush(list_state, (num_of_attacking_pairs, successor))
        return None
    

class Queens_GeneticAlg:
    def __init__(self,state):
        self.state = state
    
    #tính số cặp quân hậu không ăn nhau
    def generate_fitness(self,state):
        count = 0
        for i in range(len(state)):
            for j in range(i+1,len(state)):
                if state[i]!=state[j] and state[i]-state[j]!=j-i and state[j]-state[i]!=j-i:
                    count+=1
        return count
    
    def generate_population(self,num_of_state, n_queens):
        population = []
        #num_of_state là số lượng trạng thái trong 1 population
        for i in range(num_of_state):
            state = []
            for j in range(n_queens):
                # tạo ngẫu nhiên các trạng thái với n quân hậu
                queen_pos = random.randint(0,n_queens-1)
                state.append(queen_pos)
            #thêm vào population
            population.append(state)
        return population
    
    def selection(self, population):
        selected = []
        #tính độ fitness của từng trạng thái trong tập population
        fitness_list = [self.generate_fitness(state) for state in population]
        for i in range(len(population)):
            #chọn ngẫu nhiên cha, mẹ từ tập population
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            # chọn parent có độ fitness cao hơn trong 2 parents vừa chọn để đưa vào tập selected
            if fitness_list[population.index(parent1)] > fitness_list[population.index(parent2)]:
                selected.append(parent1)
            else:
                selected.append(parent2)
        return selected
    
    #hàm thay đổi ngẫu nhiên 1 quân hậu sang 1 vị trí ngẫu nhiên
    def mutation(self, state):
        queen_num = random.randint(0,len(state)-1)
        queen_pos = random.randint(0,len(state)-1)
        state[queen_num] = queen_pos
        return state
    
    #hàm lai ghép giữa 2 parents để tạo ra 2 children
    def cross_over(self,parent1, parent2):
        #vị trí lai ghép được chọn ngẫu nhiên từ 0 đến n-1
        pos = random.randint(0,len(parent1)-1)
        child1 = parent1[:pos] + parent2[pos:]
        child2 = parent2[:pos] + parent1[pos:]
        return child1, child2
    
    def genetic_algorithm_n_queens(self, n):
        population_size = 1000
        #tạo ngẫu nhiên tập population
        population = self.generate_population(population_size,n)
        #thực hiện quy trình của genetic algorithm trong vòng 1000 lần
        for i in range(1000):
            # thực hiện chọn lọc
            population = self.selection(population)
            #chọn ra 10 trạng thái tốt nhất bằng cách sắp xếp tập population
            best_state_list = sorted(population,key=lambda i: self.generate_fitness(i), reverse= True)[:10]
            children = []
            #lần lượt tạo các children và thêm vào tập best_state_list sao cho đủ 1000 phần tử (đã định sẵn)
            while len(children)< population_size - len(best_state_list):
                parent1, parent2 = random.choices(population,k=2)
                # thực hiện lai ghép
                child1, child2 = self.cross_over(parent1, parent2)
                # thực hiện biến dị
                child1 = self.mutation(child1)
                child2 = self.mutation(child2)
                children.append(child1)
                children.append(child2)
            population = best_state_list + children
            best_fitness = self.generate_fitness(best_state_list[0])
            # nếu trạng thái tốt nhất có số cặp quân hậu không tấn công nhau max ( = (n*(n-1))/2 ) thì trả về kết quả
            if best_fitness == (n*(n-1))/2:
                return best_state_list[0]
            
        return None
    

def print_state_with_ui(state):
    print()
    for i in range(len(state)):
        for j in range(len(state)):
            if i==state[j]:
                print("Q",end="   ")
            else:
                print("*",end="   ")
        print()
    

if __name__ == '__main__':
    
    tracemalloc.start()
    n= int(input("Enter number of queens: "))
    print("Choose one method:")
    print("1: UCS")
    print("2: A*")
    print("3: Genetic Algorithm")
    choice = int(input("Enter your method: "))
    start_time = time.time()
    if(choice==1):
        queens = Queens_UCS([0]*n)
        goal_state = queens.UCS()
        if goal_state is None:
            print("No solution found.")
        else:
            print("Found a solution:")
            print(goal_state)
            if(n<=10):
                print_state_with_ui(goal_state)
    if(choice == 2):
        start_state = [0]*n
        queens = Queens_Astar(start_state)
        goal_state = queens.A_Star(start_state)
        if(goal_state is not None):
            print("Found a solution:")
            print(goal_state)
            if(n<=10):
                print_state_with_ui(goal_state)
        else:
            print("Not found solution")
    if (choice == 3):
        queens = Queens_GeneticAlg([])
        goal_state = queens.genetic_algorithm_n_queens(n)
        if goal_state is not None:
            print(goal_state)
            if(n<=10):
                print_state_with_ui(goal_state)
            print()
        else:
            print("Not found solution")
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("\nTime used = ",(time.time()-start_time)*1000)
    print("Memory: ", current/1024)