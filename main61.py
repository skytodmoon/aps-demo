import json
import json
import random
from aps6 import WorkOrder, Operation, WorkCenter, GeneticAlgorithmAPS
from datetime import datetime, timedelta

if __name__ == "__main__":
    work_center1 = WorkCenter(name="WC1", resources={"人工": 550, "设备": 150, "材料": 300})
    work_center2 = WorkCenter(name="WC2", resources={"人工": 70, "设备": 75, "材料": 150})
    work_center3 = WorkCenter(name="WC3", resources={"人工": 120, "设备": 100, "材料": 100})
    work_center4 = WorkCenter(name="WC4", resources={"人工": 80, "设备": 90, "材料": 150})
    work_centers = [work_center1, work_center2, work_center3, work_center4]

    op1 = Operation(order_id=1, item_id="Item-A", operation_id=1, work_center_name="WC1", processing_time=200)
    op2 = Operation(order_id=1, item_id="Item-A", operation_id=2, work_center_name="WC2", processing_time=3)
    op3 = Operation(order_id=2, item_id="Item-A", operation_id=1, work_center_name="WC1", processing_time=1)
    op4 = Operation(order_id=2, item_id="Item-A", operation_id=2, work_center_name="WC3", processing_time=4)
    op5 = Operation(order_id=3, item_id="Item-B", operation_id=1, work_center_name="WC1", processing_time=3)
    op6 = Operation(order_id=3, item_id="Item-B", operation_id=2, work_center_name="WC2", processing_time=2)
    op7 = Operation(order_id=4, item_id="Item-B", operation_id=1, work_center_name="WC2", processing_time=2)
    op8 = Operation(order_id=4, item_id="Item-B", operation_id=2, work_center_name="WC3", processing_time=5)
    op9 = Operation(order_id=5, item_id="Item-C", operation_id=1, work_center_name="WC1", processing_time=1)
    op10 = Operation(order_id=5, item_id="Item-C", operation_id=2, work_center_name="WC2", processing_time=2)
    op11 = Operation(order_id=5, item_id="Item-C", operation_id=3, work_center_name="WC3", processing_time=3)
    op12 = Operation(order_id=6, item_id="Item-D", operation_id=1, work_center_name="WC1", processing_time=2)
    op13 = Operation(order_id=6, item_id="Item-D", operation_id=2, work_center_name="WC4", processing_time=4)

    work_order1 = WorkOrder(order_id=1, item_id="Item-A", operations=[op1, op2], due_date=10, start_date=5)
    work_order2 = WorkOrder(order_id=2, item_id="Item-A", operations=[op3, op4], due_date=15, start_date=0)
    work_order3 = WorkOrder(order_id=3, item_id="Item-B", operations=[op5, op6], due_date=15, start_date=0)
    work_order4 = WorkOrder(order_id=4, item_id="Item-B", operations=[op7, op8], due_date=10, start_date=0)
    work_order5 = WorkOrder(order_id=5, item_id="Item-C", operations=[op9, op10, op11], due_date=20, start_date=0)
    work_order6 = WorkOrder(order_id=6, item_id="Item-D", operations=[op12, op13], due_date=10, start_date=0)

    work_orders = [work_order1, work_order2, work_order3, work_order4, work_order5, work_order6]

    routing = [[op1, op2], [op3, op4], [op5, op6], [op7, op8], [op9, op10, op11], [op12, op13]]

    ga_aps = GeneticAlgorithmAPS(work_orders=work_orders, routing=routing, work_centers=work_centers)
    best_individual = ga_aps.run()
    print(best_individual)
    # Update data
    work_centers.append(WorkCenter(name="WC5", resources={"人工": 60, "设备": 80, "材料": 100}))
    op14 = Operation(order_id=7, item_id="Item-E", operation_id=1, work_center_name="WC4", processing_time=3)
    op15 = Operation(order_id=7, item_id="Item-E", operation_id=2, work_center_name="WC5", processing_time=2)
    work_order7 = WorkOrder(order_id=7, item_id="Item-E", operations=[op14, op15], due_date=12, start_date=0)
    work_orders.append(work_order7)
    routing.append([op14, op15])
    updated_ga_aps = GeneticAlgorithmAPS(work_orders=work_orders, routing=routing, work_centers=work_centers)

    best_individual = updated_ga_aps.run()
    print(best_individual)
