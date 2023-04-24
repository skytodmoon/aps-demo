import json
import random
from aps6 import WorkOrder, Operation, WorkCenter, GeneticAlgorithmAPS
from datetime import datetime, timedelta

if __name__ == "__main__":
    orders = []
    for i in range(1, 21): item_id = f"P{i}"
    for j in range(1, 6): order_id = j
    operations = []
    for k in range(1, 6): operation_id = k
    work_center_name = f"W{j}"
    processing_time = random.randint(1, 10)
    operations.append(
        {"order_id": order_id, "item_id": item_id, "operation_id": operation_id, "work_center_name": work_center_name,
         "processing_time": processing_time})
due_date = random.randint(20, 40)
start_date = random.randint(0, due_date - 10)
order = {"order_id": order_id, "item_id": item_id, "operations": operations, "due_date": due_date,
         "start_date": start_date}
orders.append(order)

routing = []
for j in range(1, 6): work_center_name = f"W{j}"
operation_ids = list(range(1, 6))
random.shuffle(operation_ids)
routing.append({"work_center_name": work_center_name, "operation_ids": operation_ids})

work_centers = []
for j in range(1, 6): work_center_name = f"W{j}"
resources = {"worker": random.randint(1, 5), "machine": random.randint(1, 5)}
work_center = {"name": work_center_name, "resources": resources}
work_centers.append(work_center)

data = {"orders": orders, "routing": routing, "work_centers": work_centers}
with open("test_data.json", "w") as f:
    json.dump(data, f, indent=4)

with open("test_data.json", "r") as f:
    data = json.load(f)

work_orders = [WorkOrder(order["order_id"], order["item_id"], [
    Operation(op["order_id"], op["item_id"], op["operation_id"], op["work_center_name"], op["processing_time"]) for
    op in order["operations"]], order["due_date"], order["start_date"]) for order in data["orders"]]

routing = [[Operation(op["order_id"], op["item_id"], op["operation_id"],
                       op["work_center_name"], op["processing_time"])
            for op in data["orders"]
            if "operation_id" in op and int(op["order_id"]) == order_id and op["operation_id"] == operation_id]
            for op in data["routing"] for operation_id in op["operation_ids"]]





work_centers = [WorkCenter(wc["name"], wc["resources"]) for wc in data["work_centers"]]

ga = GeneticAlgorithmAPS(work_orders, routing, work_centers)

best_individual = ga.run()
operation_list = ga.get_operation_list(best_individual)
print([op.order_id for op in operation_list])
