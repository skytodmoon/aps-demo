from aps import WorkOrder, Operation, WorkCenter, GeneticAlgorithmAPS

# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.




def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    orders = [
        WorkOrder("1", "A", 0, 10, 20, 0),
        WorkOrder("2", "A", 1, 15, 30, 0),
        WorkOrder("3", "B", 0, 20, 40, 0),
        WorkOrder("4", "C", 0, 8, 16, 0),
        WorkOrder("5", "C", 1, 12, 24, 0)
    ]

    routing = [
        [Operation("1", "A", 0, "E1", 5),
         Operation("1", "A", 1, "E2", 5),
         Operation("1", "A", 2, "E1", 5)],
        [Operation("2", "A", 0, "E2", 7),
         Operation("2", "A", 1, "E1", 7)],
        [Operation("3", "B", 0, "E3", 10)],
        [Operation("4", "C", 0, "E2", 8)],
        [Operation("5", "C", 0, "E1", 6),
         Operation("5", "C", 1, "E2", 6)]
    ]

    work_centers = [
        WorkCenter("C1", ["E1", "E2"]),
        WorkCenter("C2", ["E2"]),
        WorkCenter("C3", ["E3"])
    ]
    ga = GeneticAlgorithmAPS(orders, routing, work_centers)
    best_individual = ga.run()

    print("Best individual:", best_individual)
    print("Fitness:", ga.fitness(best_individual))
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
