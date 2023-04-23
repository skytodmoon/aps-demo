from aps3 import WorkOrder, Operation, WorkCenter, GeneticAlgorithmAPS
import matplotlib.pyplot as plt

if __name__ == "__main__":
    work_orders = [WorkOrder(0, 'item0',
                             [Operation(0, 'item0', 0, 'resource1', 10), Operation(0, 'item0', 1, 'resource2', 30),
                              Operation(0, 'item0', 2, 'resource3', 20)], 100, 0),

                   WorkOrder(1, 'item1', [Operation(1, 'item1', 0, 'resource2', 20),
                                          Operation(1, 'item1', 1, 'resource3', 30)], 90, 0),

                   WorkOrder(2, 'item2', [Operation(2, 'item2', 0, 'resource1', 30),
                                          Operation(2, 'item2', 1, 'resource2', 20)], 80, 0),

                   WorkOrder(3, 'item3', [Operation(3, 'item3', 0, 'resource1', 10),
                                          Operation(3, 'item3', 1, 'resource2', 20)], 70, 0),

                   WorkOrder(4, 'item4', [Operation(4, 'item4', 0, 'resource3', 10)], 60, 0),

                   WorkOrder(5, 'item5', [Operation(5, 'item5', 0, 'resource1', 40),
                                          Operation(5, 'item5', 1, 'resource2', 10)], 50, 0),

                   WorkOrder(6, 'item6', [Operation(6, 'item6', 0, 'resource3', 20),
                                          Operation(6, 'item6', 1, 'resource1', 20)], 40, 0),

                   WorkOrder(7, 'item7', [Operation(7, 'item7', 0, 'resource2', 40)], 30, 0),

                   WorkOrder(8, 'item8', [Operation(8, 'item8', 0, 'resource1', 20),
                                          Operation(8, 'item8', 1, 'resource2', 30),
                                          Operation(8, 'item8', 2, 'resource3', 20)], 100, 0),

                   WorkOrder(9, 'item9', [Operation(9, 'item9', 0, 'resource2', 20),
                                          Operation(9, 'item9', 1, 'resource3', 30)], 90, 0),

                   WorkOrder(10, 'item10', [Operation(10, 'item10', 0, 'resource1', 30),
                                            Operation(10, 'item10', 1, 'resource2', 20)], 80, 0),

                   WorkOrder(11, 'item11', [Operation(11, 'item11', 0, 'resource1', 10),
                                            Operation(11, 'item11', 1, 'resource2', 20)], 70, 0),

                   WorkOrder(12, 'item12', [Operation(12, 'item12', 0, 'resource3', 10)], 60, 0),

                   WorkOrder(13, 'item13', [Operation(13, 'item13', 0, 'resource1', 40),
                                            Operation(13, 'item13', 1, 'resource2', 10)], 50, 0),

                   WorkOrder(14, 'item14', [Operation(14, 'item14', 0, 'resource3', 20),
                                            Operation(14, 'item14', 1, 'resource1', 20)], 40, 0),

                   WorkOrder(15, 'item15', [Operation(15, 'item15', 0, 'resource2', 40)], 30, 0),

                   WorkOrder(16, 'item16', [Operation(16, 'item16', 0, 'resource1', 20),
                                            Operation(16, 'item16', 1, 'resource2', 30),
                                            Operation(16, 'item16', 2, 'resource3', 20)], 100, 0),

                   WorkOrder(17, 'item17', [Operation(17, 'item17', 0, 'resource2', 20),
                                            Operation(17, 'item17', 1, 'resource3', 30)], 90, 0),

                   WorkOrder(18, 'item18', [Operation(18, 'item18', 0, 'resource1', 30),
                                            Operation(18, 'item18', 1, 'resource2', 20)], 80, 0),

                   WorkOrder(19, 'item19', [Operation(19, 'item19', 0, 'resource1', 10),
                                            Operation(19, 'item19', 1, 'resource2', 20)], 70, 0),
                   ]

    routing = [[Operation(0, 'item0', 0, 'resource1', 10), Operation(0, 'item0', 1, 'resource2', 30),
            Operation(0, 'item0', 2, 'resource3', 20)],
           [Operation(1, 'item1', 0, 'resource2', 20), Operation(1, 'item1', 1, 'resource3', 30)],
           [Operation(2, 'item2', 0, 'resource1', 30), Operation(2, 'item2', 1, 'resource2', 20)],
           [Operation(3, 'item3', 0, 'resource1', 10), Operation(3, 'item3', 1, 'resource2', 20)],
           [Operation(4, 'item4', 0, 'resource3', 10)],
           [Operation(5, 'item5', 0, 'resource1', 40), Operation(5, 'item5', 1, 'resource2', 10)],
           [Operation(6, 'item6', 0, 'resource3', 20), Operation(6, 'item6', 1, 'resource1', 20)],
           [Operation(7, 'item7', 0, 'resource2', 40)],
           [Operation(8, 'item8', 0, 'resource1', 20), Operation(8, 'item8', 1, 'resource2', 30),
            Operation(8, 'item8', 2, 'resource3', 20)],
           [Operation(9, 'item9', 0, 'resource2', 20), Operation(9, 'item9', 1, 'resource3', 30)],
           [Operation(10, 'item10', 0, 'resource1', 30), Operation(10, 'item10', 1, 'resource2', 20)],
           [Operation(11, 'item11', 0, 'resource1', 10), Operation(11, 'item11', 1, 'resource2', 20)],
           [Operation(12, 'item12', 0, 'resource3', 10)],
           [Operation(13, 'item13', 0, 'resource1', 40), Operation(13, 'item13', 1, 'resource2', 10)],
           [Operation(14, 'item14', 0, 'resource3', 20), Operation(14, 'item14', 1, 'resource1', 20)],
           [Operation(15, 'item15', 0, 'resource2', 40)],
           [Operation(16, 'item16', 0, 'resource1', 20), Operation(16, 'item16', 1, 'resource2', 30),
            Operation(16, 'item16', 2, 'resource3', 20)],
           [Operation(17, 'item17', 0, 'resource2', 20), Operation(17, 'item17', 1, 'resource3', 30)],
           [Operation(18, 'item18', 0, 'resource1', 30), Operation(18, 'item18', 1, 'resource2', 20)],
           [Operation(19, 'item19', 0, 'resource1', 10), Operation(19, 'item19', 1, 'resource2', 20)], ]

    work_centers = [WorkCenter('resource1', ['resource1']), WorkCenter('resource2', ['resource2']),
                WorkCenter('resource3', ['resource3']), ]

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