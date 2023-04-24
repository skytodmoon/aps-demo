from aps6 import WorkOrder, Operation, WorkCenter, GeneticAlgorithmAPS
from datetime import datetime, timedelta


# import matplotlib.pyplot as plt

if __name__ == "__main__":
    WC1 = WorkCenter("WC1", {"人力": 10, "机器": 3})
    WC2 = WorkCenter("WC2", {"人力": 5, "机器": 4})
    WC3 = WorkCenter("WC3", {"人力": 8, "机器": 6})

    wo1 = WorkOrder(1, "ITEM1", [Operation(1, "ITEM1", 1, "WC1", 100), Operation(1, "ITEM1", 2, "WC2", 3),
                                 Operation(1, "ITEM1", 3, "WC3", 2), ],
                    int(datetime.now().timestamp() + timedelta(days=70).total_seconds()),
                    int(datetime.now().timestamp()))

    wo2 = WorkOrder(2, "ITEM2", [Operation(2, "ITEM2", 1, "WC1", 2), Operation(2, "ITEM2", 2, "WC3", 3),
                                 Operation(2, "ITEM2", 3, "WC2", 1), ],
                    int(datetime.now().timestamp() + timedelta(days=10).total_seconds()),
                    int(datetime.now().timestamp()))

    wo3 = WorkOrder(3, "ITEM3", [Operation(3, "ITEM3", 1, "WC2", 2), Operation(3, "ITEM3", 2, "WC1", 1),
                                 Operation(3, "ITEM3", 3, "WC3", 4), ],
                    int(datetime.now().timestamp() + timedelta(days=14).total_seconds()),
                    int(datetime.now().timestamp()))

    wo4 = WorkOrder(4, "ITEM4", [Operation(4, "ITEM4", 1, "WC3", 3), Operation(4, "ITEM4", 2, "WC2", 2),
                                 Operation(4, "ITEM4", 3, "WC1", 2), ],
                    int(datetime.now().timestamp() + timedelta(days=21).total_seconds()),
                    int(datetime.now().timestamp()))

    wo5 = WorkOrder(5, "ITEM5", [Operation(5, "ITEM5", 1, "WC1", 1), Operation(5, "ITEM5", 2, "WC3", 4),
                                 Operation(5, "ITEM5", 3, "WC2", 3), ],
                    int(datetime.now().timestamp() + timedelta(days=28).total_seconds()),
                    int(datetime.now().timestamp()))

    wo6 = WorkOrder(6, "ITEM6", [Operation(6, "ITEM6", 1, "WC2", 2), Operation(6, "ITEM6", 2, "WC1", 3),
                                 Operation(6, "ITEM6", 3, "WC3", 1), ],
                    int(datetime.now().timestamp() + timedelta(days=35).total_seconds()),
                    int(datetime.now().timestamp()))

    wo7 = WorkOrder(7, "ITEM7", [Operation(7, "ITEM7", 1, "WC3", 3), Operation(7, "ITEM7", 2, "WC2", 4),
                                 Operation(7, "ITEM7", 3, "WC1", 2), ],
                    int(datetime.now().timestamp() + timedelta(days=42).total_seconds()),
                    int(datetime.now().timestamp()))

    wo8 = WorkOrder(8, "ITEM8", [Operation(8, "ITEM8", 1, "WC1", 1), Operation(8, "ITEM8", 2, "WC3", 2),
                                 Operation(8, "ITEM8", 3, "WC2", 3), ],
                    int(datetime.now().timestamp() + timedelta(days=49).total_seconds()),
                    int(datetime.now().timestamp()))

    wo9 = WorkOrder(9, "ITEM9", [Operation(9, "ITEM9", 1, "WC2", 2), Operation(9, "ITEM9", 2, "WC1", 1),
                                 Operation(9, "ITEM9", 3, "WC3", 4), ],
                    int(datetime.now().timestamp() + timedelta(days=56).total_seconds()),
                    int(datetime.now().timestamp()))

    wo10 = WorkOrder(10, "ITEM10", [Operation(10, "ITEM10", 1, "WC3", 3), Operation(10, "ITEM10", 2, "WC2", 2),
                                    Operation(10, "ITEM10", 3, "WC1", 2), ],
                     int(datetime.now().timestamp() + timedelta(days=63).total_seconds()),
                     int(datetime.now().timestamp()))

    routing = [[wo1.operations[0], wo5.operations[0], wo8.operations[0], wo10.operations[0], wo2.operations[0],
                wo6.operations[0], wo9.operations[0], wo3.operations[0], wo7.operations[0], wo4.operations[0]],
               [wo1.operations[1], wo5.operations[2]],
               [wo1.operations[2], wo5.operations[1], wo8.operations[1], wo3.operations[2], wo10.operations[1]],
               [wo2.operations[1], wo6.operations[2], wo7.operations[1], wo4.operations[2]],
               [wo2.operations[2], wo6.operations[1], wo9.operations[2]],
               [wo3.operations[1], wo7.operations[2], wo4.operations[1], wo10.operations[2]],
               [wo8.operations[2], wo9.operations[1]], ]

    ga_aps = GeneticAlgorithmAPS([wo1, wo2, wo3, wo4, wo5, wo6, wo7, wo8, wo9, wo10], routing, [WC1, WC2, WC3])
    best_individual = ga_aps.run()

    # 打印最优解
    print("Best individual:", best_individual)

    # 计算最优解的适应度
    best_fitness = ga_aps.fitness(best_individual)

    # 打印最优解的适应度
    print("Best fitness:", best_fitness)

# plt.plot(best_fitness)
# plt.xlabel("Generation")
# plt.ylabel("Best Fitness")
# plt.show()
