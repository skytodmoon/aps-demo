import random
from collections import defaultdict
from typing import List, Tuple

# 定义遗传算法的参数
pop_size = 50 # 种群大小
elite_size = 10 # 精英个体数量
mutation_rate = 0.1 # 变异率
max_generations = 100 # 最大迭代次数

# 读取制造领域的数据
# InventoryObject 库存
# InventoryMoveObject 库存移动
# InventoryAdjustmentObject 库存调整
# InventorySnapshotObject 库存快照
# OrderObject 订单
# WorkOrderObject 工单
# OperationObject 操作
# OperationResourceObject 操作资源
# OperationLogObject 操作日志
# RoutingObject 生产路线
# RoutingStepObject 生产路线步骤
# RoutingStepOperationObject 生产路线步骤操作
# RoutingAlternateOperationObject 生产路线备选操作
# RoutingResourceObject 生产路线资源需求
# RoutingResourceRelationshipObject 生产路线资源关系

# 定义一个工单类
class WorkOrder:
    def __init__(self, order_id: str, item_id: str, operation_id: int, quantity: int, due_date: int, start_date: int):
        self.order_id = order_id
        self.item_id = item_id
        self.operation_id = operation_id
        self.quantity = quantity
        self.due_date = due_date
        self.start_date = start_date

# 定义一个操作类
class Operation:
    def __init__(self, order_id: str, item_id: str, operation_id: int, resource: str, processing_time: int):
        self.order_id = order_id
        self.item_id = item_id
        self.operation_id = operation_id
        self.resource = resource
        self.processing_time = processing_time


# 定义一个工作中心类
class WorkCenter:
    def __init__(self, name: str, resources: List[str]):
        self.name = name
        self.resources = resources

# 定义一个遗传算法类
class GeneticAlgorithmAPS:
    def __init__(self, work_orders: List[WorkOrder], routing: List[List[Operation]], work_centers: List[WorkCenter]):
        self.work_orders = work_orders
        self.routing = routing
        self.work_centers = work_centers

    # 定义适应度函数
    def fitness(self, individual: List[int]) -> float:
        # 计算每个工单的开始时间和结束时间
        start_times = [0] * len(self.work_orders)
        end_times = [0] * len(self.work_orders)

        for i, op_id in enumerate(individual):
            print(op_id)
            op = self.routing[op_id]
            print(len(op))
            wo = self.work_orders[op_id]

            start_time = max(start_times[wo.operation_id - 1], end_times[wo.operation_id - 1])
            print("start_time:", start_time)
            print("op process time:", op.order_id)
            end_time = start_time + op.processing_time

            start_times[wo.operation_id] = start_time
            end_times[wo.operation_id] = end_time

        # 计算每个工单的延迟时间和总延迟时间
        delays = [max(0, end_times[i] - wo.due_date) for i, wo in enumerate(self.work_orders)]
        total_delay = sum(delay * wo.quantity for delay, wo in zip(delays, self.work_orders))

        # 计算适应度
        fitness = 1 / (1 + total_delay)

        return fitness

    # 定义选择操作
    def selection(self, pop: List[List[int]]) -> List[List[int]]:
        fitnesses = [self.fitness(individual) for individual in pop]
        elite = sorted(range(len(fitnesses)), key=lambda i: fitnesses[i], reverse=True)[:elite_size]
        offspring = random.choices(population=pop, weights=fitnesses, k=pop_size - elite_size)
        return [pop[i] for i in elite] + offspring

    # 定义交叉操作
    def crossover(self, parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    # 定义变异操作
    def mutation(self, individual: List[int]) -> List[int]:
        if random.random() < mutation_rate:
            i, j = random.sample(range(len(individual)), k=2)
            individual[i], individual[j] = individual[j], individual[i]
        return individual

    # 定义运行遗传算法的主函数
    def run(self) -> List[int]:
        # 初始化种群
        pop = [random.sample(range(len(self.routing)), k=len(self.routing)) for _ in range(pop_size)]

        # 迭代遗传算法
        for generation in range(max_generations):
            pop = self.selection(pop)
            offspring = []

            # 生成下一代个体
            while len(offspring) < pop_size - elite_size:
                parent1, parent2 = random.choices(population=pop, k=2)
                child1, child2 = self.crossover(parent1, parent2)
                offspring.append(self.mutation(child1))
                offspring.append(self.mutation(child2))

            # 更新种群
            pop = pop[:elite_size] + offspring

        # 计算最优解
        best_individual = max(pop, key=lambda ind: self.fitness(ind))
        return best_individual
