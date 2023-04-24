import random
from typing import List, Tuple

# 定义遗传算法的参数
#种群大小（POP_SIZE）：一般取50~200之间的整数。
POP_SIZE = 200  # 种群大小
#精英个体数量（ELITE_SIZE）：一般取种群大小的10%~20%之间的整数。
ELITE_SIZE = 40  # 精英个体数量
#变异率（MUTATION_RATE）：一般取0.05~0.2之间的实数。
MUTATION_RATE = 0.1  # 变异率
#最大迭代次数（MAX_GENERATIONS）：一般取100~500之间的整数。
MAX_GENERATIONS = 100  # 最大迭代次数




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
    def __init__(self, order_id: int, item_id: str, operation_id: int, resource: str, processing_time: int):
        self.order_id = order_id
        self.item_id = item_id
        self.operation_id = operation_id
        self.resource = resource
        self.processing_time = processing_time

class WorkOrder:
    """
    工单类

    Attributes:
        order_id: 订单编号
        item_id: 物料编号
        operations: 工单的操作列表
        due_date: 交货日期
        start_date: 开始日期
    """
    def __init__(self, order_id: int, item_id: str, operations: List[Operation], due_date: int, start_date: int):
        self.order_id = order_id
        self.item_id = item_id
        self.operations = operations
        self.due_date = due_date
        self.start_date = start_date


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
        # 将个体转换为操作列表
        operation_list = []
        for i in individual:
            wo = self.work_orders[i]
            operation_list += [op for op in wo.operations]

        # 计算每个工单的开始时间和结束时间
        start_times = [0] * (len(self.work_orders) + 1)
        end_times = [0] * (len(self.work_orders) + 1)

        for op in operation_list:
            wo = self.work_orders[op.order_id]
            start_time = max(start_times[wo.order_id], end_times[wo.order_id - 1])
            end_time = start_time + op.processing_time
            start_times[wo.order_id] = start_time
            end_times[wo.order_id] = end_time

        # 计算每个工单的延迟时间和总延迟时间
        delays = [max(0, end_times[i] - wo.due_date) for i, wo in enumerate(self.work_orders, start=1)]
        total_delay = sum(delay for delay in delays)

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
        # 去重操作，对个体进行去重操作，保证每个工单只被计算一次
        pop = [list(set(individual)) for individual in pop]

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
            while individual[i] == individual[j]:
                j = random.randint(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]
        return individual

    def run(self) -> List[int]:
        """
        运行遗传算法，求解最优解，即最优的操作序列。

        Returns:
            最优的操作序列。
        """
        ## 初始化种群
        #pop = [random.sample(range(len(self.work_orders)), k=len(self.work_orders)) for _ in range(POP_SIZE)]
        # 初始化种群
        pop = [list(set(random.sample(range(len(self.work_orders)), k=len(self.work_orders)))) for _ in range(POP_SIZE)]

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
