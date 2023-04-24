from aps6 import WorkOrder, Operation, WorkCenter, GeneticAlgorithmAPS

# import matplotlib.pyplot as plt

if __name__ == "__main__":
    work_orders = [WorkOrder(1, "A", [Operation(1, "A", 1, "WC1", 5), Operation(1, "A", 2, "WC2", 6),
                                      Operation(1, "A", 3, "WC3", 4)], 20, 0), WorkOrder(2, "B", [
        Operation(2, "B", 1, "WC1", 4), Operation(2, "B", 2, "WC3", 6), Operation(2, "B", 3, "WC2", 5)], 25, 0),
                   WorkOrder(3, "C", [Operation(3, "C", 1, "WC2", 7), Operation(3, "C", 2, "WC1", 4),
                                      Operation(3, "C", 3, "WC3", 5)], 30, 0), WorkOrder(4, "D", [
            Operation(4, "D", 1, "WC3", 5), Operation(4, "D", 2, "WC2", 6), Operation(4, "D", 3, "WC1", 4)], 35, 0),
                   WorkOrder(5, "E", [Operation(5, "E", 1, "WC1", 4), Operation(5, "E", 2, "WC3", 7),
                                      Operation(5, "E", 3, "WC2", 5)], 40, 0), WorkOrder(6, "F", [
            Operation(6, "F", 1, "WC3", 5), Operation(6, "F", 2, "WC2", 6), Operation(6, "F", 3, "WC1", 5)], 45, 0),
                   WorkOrder(7, "G", [Operation(7, "G", 1, "WC2", 5), Operation(7, "G", 2, "WC1", 6),
                                      Operation(7, "G", 3, "WC3", 4)], 50, 0), WorkOrder(8, "H", [
            Operation(8, "H", 1, "WC3", 6), Operation(8, "H", 2, "WC2", 4), Operation(8, "H", 3, "WC1", 5)], 55, 0),
                   WorkOrder(9, "I", [Operation(9, "I", 1, "WC2", 5), Operation(9, "I", 2, "WC3", 6),
                                      Operation(9, "I", 3, "WC1", 4)], 60, 0), WorkOrder(10, "J", [
            Operation(10, "J", 1, "WC1", 6), Operation(10, "J", 2, "WC2", 5), Operation(10, "J", 3, "WC3", 7)], 65, 0)]
    routing = [[1, 2, 3], [2, 3, 1], [3, 1, 2], [1, 2, 3], [2, 3, 1], [3, 1, 2], [1, 2, 3], [2, 3, 1], [3, 1, 2],
               [1, 2, 3]]
    work_centers = [WorkCenter("WC1", {"Machine": 2, "Worker": 1}), WorkCenter("WC2", {"Machine": 3, "Worker": 1}),
                    WorkCenter("WC3", {"Machine": 1, "Worker": 2})]

    ga = GeneticAlgorithmAPS(work_orders, routing, work_centers)

    # 运行遗传算法
    best_individual = ga.run()

    # 打印最优解
    print("Best individual:", best_individual)

    # 计算最优解的适应度
    best_fitness = ga.fitness(best_individual)

    # 打印最优解的适应度
    print("Best fitness:", best_fitness)

# plt.plot(best_fitness)
# plt.xlabel("Generation")
# plt.ylabel("Best Fitness")
# plt.show()
