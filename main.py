from aps2 import WorkOrder, Operation, WorkCenter, GeneticAlgorithmAPS

if __name__ == "__main__":
    # 制造测试数据
    work_orders = [
        WorkOrder("001", "A", 1, 10, 5, 0),
        WorkOrder("002", "B", 1, 5, 10, 0),
        WorkOrder("003", "C", 1, 8, 4, 0),
        WorkOrder("004", "D", 1, 6, 12, 0),
        WorkOrder("005", "E", 1, 15, 6, 0),
    ]

    routing = [
        [Operation("001", "A", 1, "WC1", 3)],
        [Operation("002", "B", 1, "WC2", 1)],
        [Operation("003", "C", 1, "WC1", 2)],
        [Operation("004", "D", 1, "WC2", 2)],
        [Operation("005", "E", 1, "WC1", 5)],
    ]

    work_centers = [
        WorkCenter("WC1", ["R1", "R2"]),
        WorkCenter("WC2", ["R2", "R3"]),
    ]

    # 运行遗传算法求最优解
    ga = GeneticAlgorithmAPS(work_orders, routing, work_centers)
    best_individual = ga.run()
    print("Best individual:", best_individual)
