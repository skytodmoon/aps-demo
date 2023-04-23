from aps3 import WorkOrder, Operation, WorkCenter, GeneticAlgorithmAPS

if __name__ == "__main__":
    wo1 = WorkOrder(0, "I001", [Operation(0, "I001", 1, "W01", 20), Operation(0, "I001", 2, "W01", 20),
                                     Operation(0, "I001", 3, "W01", 20)], 100, 0)

    wo2 = WorkOrder(1, "I001", [Operation(1, "I001", 1, "W01", 20), Operation(1, "I001", 2, "W01", 20),
                                     Operation(1, "I001", 3, "W01", 20)], 100, 0)

    wo3 = WorkOrder(2, "I002", [Operation(2, "I002", 1, "W02", 50), Operation(2, "I002", 2, "W02", 50)],
                    150, 0)

    wo4 = WorkOrder(3, "I002", [Operation(3, "I002", 1, "W02", 50), Operation(3, "I002", 2, "W02", 50)],
                    150, 0)
    routing = [[wo1.operations[0], wo1.operations[1], wo1.operations[2]],
               [wo2.operations[0], wo2.operations[1], wo2.operations[2]], [wo3.operations[0], wo3.operations[1]],
               [wo4.operations[0], wo4.operations[1]], ]
    wc1 = WorkCenter("W01", ["Machine1", "Machine2", "Machine3"])
    wc2 = WorkCenter("W02", ["Machine1"])

    work_centers = [wc1, wc2]

    ga = GeneticAlgorithmAPS([wo1, wo2, wo3, wo4], routing, work_centers)

    # 运行遗传算法
    best_individual = ga.run()

    # 打印最优解
    print("Best individual:", best_individual)

    # 计算最优解的适应度
    best_fitness = ga.fitness(best_individual)

    # 打印最优解的适应度
    print("Best fitness:", best_fitness)