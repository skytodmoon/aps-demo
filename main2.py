from aps2 import WorkOrder, Operation, WorkCenter, GeneticAlgorithmAPS

if __name__ == "__main__":
    work_orders = [WorkOrder("1001", "A", 1, 50, 20, 0),
                   WorkOrder("1002", "B", 1, 30, 30, 0),
                   WorkOrder("1003", "B", 2, 30, 40, 0),
                   WorkOrder("1004", "C", 1, 40, 50, 0),
                   WorkOrder("1005", "C", 2, 20, 60, 0)]

routing = [[Operation("1001", "A", 0, "WC1", 5)],
           [Operation("1002", "B", 0, "WC2", 10)],
           [Operation("1003", "B", 1, "WC2", 20)],
           [Operation("1004", "C", 0, "WC3", 15)],
           [Operation("1005", "C", 1, "WC3", 30)]]

work_centers = [WorkCenter("WC1", ["R1"]),
                WorkCenter("WC2", ["R2"]),
                WorkCenter("WC3", ["R2"])]

# 初始化遗传算法
ga = GeneticAlgorithmAPS(work_orders, routing, work_centers)

# 运行遗传算法
best_individual = ga.run()

# 打印最优解
print("Best individual:", best_individual)

# 计算最优解的适应度
best_fitness = ga.fitness(best_individual)

# 打印最优解的适应度
print("Best fitness:", best_fitness)
