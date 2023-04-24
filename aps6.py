import random
from typing import List, Tuple

# 定义遗传算法的参数
POP_SIZE = 200  # 种群大小
ELITE_SIZE = 40  # 精英个体数量
MUTATION_RATE = 0.1  # 变异率
MAX_GENERATIONS = 100  # 最大迭代次数


class Operation:
    """
    操作类

    Attributes:
        order_id: 订单编号
        item_id: 物料编号
        operation_id: 操作编号
        work_center_name: 工作中心名称
        processing_time: 处理时间
    """

    def __init__(self, order_id: int, item_id: str, operation_id: int, work_center_name: str, processing_time: int):
        self.order_id = order_id
        self.item_id = item_id
        self.operation_id = operation_id
        self.work_center_name = work_center_name
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
        resources: 资源字典，记录每个资源的数量和效率
    """

    def __init__(self, name: str, resources: dict):
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
        self.operation_list = []  # 缓存操作列表
        self.start_times = []  # 缓存每个工单的开始时间
        self.end_times = []  # 缓存每个工单的结束时间
        self.resource_usage = {}  # 缓存每个工作中心的资源使用情况

    def get_operation_list(self, individual: List[int]) -> List[Operation]:
        """
        获取个体的操作列表，同时对操作进行去重和排序操作。

        Args:
            individual: 个体，是一个工单编号列表。

        Returns:
            一个操作列表。
        """
        if self.operation_list:
            return self.operation_list
        self.operation_list = []
        for index in individual:
            routing_ops = self.routing[index]
            for op in routing_ops:
                wo = self.work_orders[op.order_id - 1]
                self.operation_list.append(op)
        self.operation_list.sort(key=lambda op: op.order_id * 1000 + op.operation_id)
        # 按照工单编号和操作编号排序
        return self.operation_list
        # if self.operation_list:
        #     return self.operation_list
        # self.operation_list = []
        # for i in individual:
        #     wo = self.work_orders[i]
        #     self.operation_list += [op for op in wo.operations if
        #                             (op.order_id, op.operation_id) not in [(op2.order_id, op2.operation_id) for op2 in
        #                                                                    self.operation_list]]
        #
        # self.operation_list.sort(key=lambda op: op.order_id * 1000 + op.operation_id)
        # # 按照工单编号和操作编号排序
        # return self.operation_list

    def get_start_time(self, op: Operation) -> int:
        """
        获取操作的开始时间。

        Args:
            op: 需要计算开始时间的操作。

        Returns:
            该操作的开始时间。
        """
        #if op.order_id - 1 < 0: return 0
        wo = self.work_orders[op.order_id - 1]
        #if wo.order_id - 1 <= 0: return 0
        start_time = max(self.start_times[wo.order_id], self.end_times[wo.order_id - 1])
        work_center = next((wc for wc in self.work_centers if wc.name == op.work_center_name), None)
        if not work_center:
            raise Exception(f"Can't find work center {op.work_center_name}")
        resources = work_center.resources
        usage = self.resource_usage.get(op.work_center_name, {})
        for resource, quantity in resources.items():
            if resource in usage:
                available_quantity = usage[resource].get(start_time, quantity)
            else:
                available_quantity = quantity
            efficiency = resources[resource] / available_quantity
            if resource in usage:
                start_time = max(start_time,
                                 max([t for t, q in usage[resource].items() if q >= quantity], default=start_time))
            for t in range(int(start_time), int(start_time + op.processing_time)):
                usage.setdefault(op.work_center_name, {}).setdefault(t, available_quantity)
                usage[op.work_center_name][t] -= quantity


        for wc, usage_dict in usage.items():
            if wc is not str: continue
            self.resource_usage.setdefault(wc, {}).update(usage_dict)
        return start_time

    def initialize_times(self):
        """
        初始化开始时间和结束时间。
        """
        self.start_times = [0] * (len(self.work_orders) + 1)
        self.end_times = [0] * (len(self.work_orders) + 1)
        self.resource_usage = {}

    def calculate_times(self, individual: List[int]):
        """
        计算每个工单的开始时间和结束时间。

        Args:
            individual: 个体，是一个工单编号列表。
        """
        self.initialize_times()
        operation_list = self.get_operation_list(individual)
        for op in operation_list:
            wo = self.work_orders[op.order_id - 1]
            start_time = self.get_start_time(op)
            end_time = start_time + op.processing_time
            self.start_times[wo.order_id] = start_time
            self.end_times[wo.order_id] = end_time

    def fitness(self, individual: List[int]) -> float:
        """
        计算个体的适应度，个体是工单编号列表。

        适应度是一个浮点数，表示个体的质量。质量越高，说明该操作序列越优秀。
        """
        self.calculate_times(individual)
        delays = [max(0, self.end_times[i-1] - wo.due_date) for i, wo in enumerate(self.work_orders, start=1)]
        total_delay = sum(delay for delay in delays)
        fitness = 1 / (1 + total_delay)
        return fitness

    def selection(self, pop: List[List[int]]) -> List[List[int]]:
        """
        选择操作。从种群中选择一些个体用于交叉和变异。

        Args:
            pop: 种群，是一组个体（工单编号列表）的列表。

        Returns:
            新的种群，是一组个体的列表。
        """
        pop = [list(individual) for individual in pop]

        fitnesses = [self.fitness(individual) for individual in pop]
        elite = sorted(range(len(fitnesses)), key=lambda i: fitnesses[i], reverse=True)[:ELITE_SIZE]
        offspring = random.choices(population=pop, weights=fitnesses, k=POP_SIZE - ELITE_SIZE)
        return [pop[i] for i in elite] + offspring

    def crossover(self, parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
        """
        交叉操作。将两个个体（工单编号列表）进行交叉操作，生成两个新的个体。

        Args:
            parent1: 一个个体，是一个工单编号列表。
            parent2: 另一个个体，是一个工单编号列表。

        Returns:
            两个新个体。
        """
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1.copy()
        child2 = parent2.copy()
        child1[crossover_point:], child2[crossover_point:] = child2[crossover_point:], child1[crossover_point:]
        return child1, child2

    def mutation(self, individual: List[int]) -> List[int]:
        """
        变异操作。对个体（工单编号列表）进行变异操作，生成新的个体。

        Args:
            individual: 一个个体，是一个工单编号列表。

        Returns:
            一个新个体。
        """
        if random.random() < MUTATION_RATE:
            i, j = random.sample(range(len(individual)), k=2)
            individual[i], individual[j] = individual[j], individual[i]
        return individual.copy()

    def run(self) -> List[int]:
        """
        运行遗传算法，求解最优解，即最优的工单编号列表。

        Returns:
            最优的工单编号列表。
        """
        pop = [list(set(random.sample(range(len(self.work_orders)), k=len(self.work_orders)))) for _ in range(POP_SIZE)]
        for generation in range(MAX_GENERATIONS):
            pop = self.selection(pop)
            offspring = []
            while len(offspring) < POP_SIZE - ELITE_SIZE:
                parent1, parent2 = random.choices(population=pop, k=2)
                child1, child2 = self.crossover(parent1, parent2)
                offspring.append(self.mutation(child1))
                offspring.append(self.mutation(child2))
            pop = pop[:ELITE_SIZE] + offspring
        best_individual = max(pop, key=lambda ind: self.fitness(ind))
        return best_individual
