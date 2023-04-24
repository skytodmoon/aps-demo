import json
import random
from aps6 import WorkOrder, Operation, WorkCenter, GeneticAlgorithmAPS
from datetime import datetime, timedelta

if __name__ == '__main__':
    # 工单数据
    wo1 = WorkOrder(order_id=1, item_id='ITEM1', operations=[
        Operation(order_id=1, item_id='ITEM1', operation_id=1, work_center_name='WC1', processing_time=10),
        Operation(order_id=1, item_id='ITEM1', operation_id=2, work_center_name='WC2', processing_time=10),
    ], due_date=60, start_date=0)
    wo2 = WorkOrder(order_id=2, item_id='ITEM2', operations=[
        Operation(order_id=2, item_id='ITEM2', operation_id=1, work_center_name='WC1', processing_time=5),
        Operation(order_id=2, item_id='ITEM2', operation_id=2, work_center_name='WC1', processing_time=5),
        Operation(order_id=2, item_id='ITEM2', operation_id=3, work_center_name='WC2', processing_time=5),
        Operation(order_id=2, item_id='ITEM2', operation_id=4, work_center_name='WC2', processing_time=5),
    ], due_date=80, start_date=0)

    # 生产路线数据
    routing = [
        [wo1.operations[0], wo1.operations[1]],  # 工单1的生产路线
        [wo2.operations[0], wo2.operations[1], wo2.operations[2], wo2.operations[3]],  # 工单2的生产路线
    ]

    # 工作中心数据
    wc1 = WorkCenter(name='WC1', resources={'resource1': 10, 'resource2': 5})
    wc2 = WorkCenter(name='WC2', resources={'resource1': 20, 'resource2': 10})
    work_centers = [wc1, wc2]

    # 运行遗传算法
    genetic_algorithm_aps = GeneticAlgorithmAPS(work_orders=[wo1, wo2], routing=routing, work_centers=work_centers)
    best_individual = genetic_algorithm_aps.run()
    print(f"Best individual: {best_individual}")

    # 计算最优的开始时间和结束时间
    operation_list = genetic_algorithm_aps.get_operation_list(best_individual)
    genetic_algorithm_aps.initialize_times()
    for op in operation_list:
        start_time = genetic_algorithm_aps.get_start_time(op)
        end_time = start_time + op.processing_time
        wo = genetic_algorithm_aps.work_orders[op.order_id - 1]
        genetic_algorithm_aps.start_times[wo.order_id] = start_time
        genetic_algorithm_aps.end_times[wo.order_id] = end_time
    print(f"Start times: {genetic_algorithm_aps.start_times}")
    print(f"End times: {genetic_algorithm_aps.end_times}")

    # 验证结果是否符合要求
    assert genetic_algorithm_aps.fitness(best_individual) > 0  # 检查适应度是否大于0
    assert genetic_algorithm_aps.start_times == [0, 10, 10, 20, 25, 35, 40]  # 检查开始时间是否正确
    assert genetic_algorithm_aps.end_times == [0, 20, 20, 30, 30, 40, 45]  # 检查结束时间是否正确

