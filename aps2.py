import random
from typing import List, Tuple

# 定义遗传算法的参数
POP_SIZE = 50  # 种群大小
ELITE_SIZE = 10  # 精英个体数量
MUTATION_RATE = 0.1  # 变异率
MAX_GENERATIONS = 100  # 最大迭代次数


class WorkOrder:
    """
    工单类

    Attributes:
        order_id: 订单编号
        item_id: 物料编号
        operation_id: 操作编号
        quantity: 数量
        due_date: 交货日期
        start_date: 开始日期
    """
    def __init__(self, order_id: str, item_id: str, operation_id: int, quantity: int, due_date: int, start_date: int):
        self.order_id = order_id
        self.item_id = item_id
        self.operation_id = operation_id
        self.quantity = quantity
        self.due_date = due_date
        self.start_date = start_date


class Operation:
    """
    操作类

    Attributes:
        order_id: 订单编号
        item_id: 物料编号
        operation_id: 操作编号
        resource: 资源
        processing_time: 处理时间
    """
    def __init__(self, order_id: str, item_id: str, operation_id: int, resource: str, processing_time: int):
        self.order_id = order_id
        self.item_id = item_id
        self.operation_id = operation_id
        self.resource = resource
        self.processing_time = processing_time


class WorkCenter:
    """
    工作中心类

    Attributes:
        name: 名称
        resources: 资源列表
    """
    def __init__(self, name: str, resources: List[str]):
        self.name = name
        self.resources = resources


class GeneticAlgorithmAPS:
    """
    遗传算法类

    Attributes:
        work_orders: 工单列表
        routing: 生产路线列表
        work_centers: 工作中心列表
    """
    def __init__(self, work_orders: List[WorkOrder], routing: List[List[Operation]], work_centers: List[WorkCenter]):
        self.work_orders = work_orders
        self.routing = routing
        self.work_centers = work_centers

    def fitness(self, individual: List[int]) -> float:
        """
        计算个体的适应度，个体是操作序列。

        适应度是一个浮点数，表示个体的质量。质量越高，说明该操作序列越优秀。
        """
        # 计算每个工单的开始时间和结束时间
        start_times = [0] * (len(self.work_orders) + 1)
        end_times = [0] * (len(self.work_orders) + 1)

        for i, op_id in enumerate(individual):
            op = self.routing[op_id][0]
            wo = self.work_orders[individual[i]]
            start_time = max(start_times[wo.operation_id - 1], end_times[wo.operation_id - 1])
            end_time = start_time + op.processing_time
            start_times[wo.operation_id] = start_time
            end_times[wo.operation_id] = end_time

        # 计算每个工单的延迟时间和总延迟时间
        delays = [max(0, end_times[i] - wo.due_date) for i, wo in enumerate(self.work_orders)]
        total_delay = sum(delay * wo.quantity for delay, wo in zip(delays, self.work_orders))

        # 计算适应度
        fitness = 1 / (1 + total_delay)

        return fitness


    def selection(self, pop: List[List[int]]) -> List[List[int]]:
        """
        选择操作。从种群中选择一些个体用于交叉和变异。

        Args:
            pop: 种群，是一组个体（操作序列）的列表。

        Returns:
            新的种群，是一组个体的列表。
        """
        fitnesses = [self.fitness(individual) for individual in pop]
        elite = sorted(range(len(fitnesses)), key=lambda i: fitnesses[i], reverse=True)[:ELITE_SIZE]
        offspring = random.choices(population=pop, weights=fitnesses, k=POP_SIZE - ELITE_SIZE)
        return [pop[i] for i in elite] + offspring

    def crossover(self, parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
        """
        交叉操作。将两个个体（操作序列）进行交叉操作，生成两个新的个体。

        Args:
            parent1: 一个个体，是一个操作序列。
            parent2: 另一个个体，是一个操作序列。

        Returns:
            两个新个体。
        """
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    def mutation(self, individual: List[int]) -> List[int]:
        """
        变异操作。对个体（操作序列）进行变异操作，生成新的个体。

        Args:
            individual: 一个个体，是一个操作序列。

        Returns:
            一个新个体。
        """
        if random.random() < MUTATION_RATE:
            i, j = random.sample(range(len(individual)), k=2)
            individual[i], individual[j] = individual[j], individual[i]
        return individual

    def run(self) -> List[int]:
        """
        运行遗传算法，求解最优解，即最优的操作序列。

        Returns:
            最优的操作序列。
        """
        # 初始化种群
        pop = [random.sample(range(len(self.routing)), k=len(self.routing)) for _ in range(POP_SIZE)]

        # 迭代遗传算法
        for generation in range(MAX_GENERATIONS):
            pop = self.selection(pop)
            offspring = []

            # 生成下一代个体
            while len(offspring) < POP_SIZE - ELITE_SIZE:
                parent1, parent2 = random.choices(population=pop, k=2)
                child1, child2 = self.crossover(parent1, parent2)
                offspring.append(self.mutation(child1))
                offspring.append(self.mutation(child2))

            # 更新种群
            pop = pop[:ELITE_SIZE] + offspring

        # 计算最优解
        best_individual = max(pop, key=lambda ind: self.fitness(ind))
        return best_individual
