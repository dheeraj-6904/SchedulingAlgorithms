from helpers import printGanttChart
from priorityPreemptive import PriorityPreemptive
from process import Process
if __name__ == "__main__":
    processes = [
        Process("P1", 0, 7, 4),
        Process("P2", 2, 2, 2),
        Process("P0", 4, 7, 3),
        Process("P3", 7, 4, 1),
        Process("P5", 8, 3, 2),
        Process("P4", 4, 1, 5),
        Process("P6", 1, 5, 8),
    ]
    priority = PriorityPreemptive(processes)
    priority.run()
    printGanttChart(priority.getGanttChart())
    # print(priority.getGanttChart())