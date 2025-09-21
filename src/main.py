from process import Process
from priority_aging_scheduler import PrioritySchedulerWithAging
from multi_level_scheduler import MultiLevelQueueScheduler

def get_priority_aging_input():
    """Gets user input for the Priority with Aging scheduler."""
    processes = []
    num_processes = int(input("Enter the number of processes: "))
    for i in range(num_processes):
        print(f"\nEnter details for Process {i+1}:")
        arrival = int(input(f"  Arrival Time: "))
        priority = int(input(f"  Initial Priority: "))
        cpu1 = int(input(f"  CPU Burst 1: "))
        io = int(input(f"  I/O Burst: "))
        cpu2 = int(input(f"  CPU Burst 2: "))
        processes.append(Process(pid=i+1, arrival_time=arrival, bursts=[cpu1, io, cpu2], priority=priority))
    
    aging_interval = int(input("\nEnter Aging Interval (X): "))
    context_switch = int(input("Enter Context Switch Time: "))
    return processes, context_switch, aging_interval

def get_multi_level_input():
    """Gets user input for the Multi-Level Queue scheduler."""
    processes = []
    num_processes = int(input("Enter the number of processes: "))
    for i in range(num_processes):
        print(f"\nEnter details for Process {i+1}:")
        arrival = int(input(f"  Arrival Time: "))
        ptype = int(input(f"  Process Type (0 for Foreground-RR, 1 for Background-FCFS): "))
        cpu1 = int(input(f"  CPU Burst 1: "))
        io = int(input(f"  I/O Burst: "))
        cpu2 = int(input(f"  CPU Burst 2: "))
        processes.append(Process(pid=i+1, arrival_time=arrival, bursts=[cpu1, io, cpu2], ptype=ptype))
    
    time_quantum = int(input("\nEnter Time Quantum for RR Queue: "))
    context_switch = int(input("Enter Context Switch Time: "))
    return processes, context_switch, time_quantum

from process import Process
from priority_aging_scheduler import PrioritySchedulerWithAging
from multi_level_scheduler import MultiLevelQueueScheduler

# The input-gathering functions (like get_priority_aging_input) are no longer needed for hardcoded tests,
# but you can keep them in the file for when you want to switch back to manual input.

def hardcodedTests():
    """Main function to run the scheduler simulation with hardcoded test data."""
    print("Welcome to the Advanced CPU Scheduler Simulation!")
    print("--- Running in Hardcoded Test Mode ---")

    # # ==============================================================================
    # # == TEST CASE 1: PREEMPTIVE PRIORITY SCHEDULING WITH AGING                   ==
    # # ==============================================================================
    # print("\nRunning Preemptive Priority Scheduler with Aging...")

    # # Define 4 processes for testing
    # processes_priority = [
    #     Process(pid=1, arrival_time=0, priority=1, bursts=[7, 2, 5]),
    #     Process(pid=2, arrival_time=3, priority=2, bursts=[2,4,5]), # Higher priority, should preempt P1
    #     # Process(pid=3, arrival_time=4, priority=4, bursts=[3, 5, 2]), # Lower priority, might starve/age
    #     # Process(pid=4, arrival_time=6, priority=3, bursts=[4, 3, 4])
    # ]
    
    # # Set scheduler parameters
    # context_switch = 2
    # aging_interval = 5 # Priority increases every 10 time units of waiting

    # # # Initialize and run the scheduler
    # scheduler = PrioritySchedulerWithAging(processes_priority, context_switch, aging_interval)


    # ==============================================================================
    # == TEST CASE 2: MULTI-LEVEL QUEUE SCHEDULING (RR/FCFS)                      ==
    # ==============================================================================
    print("\nRunning Multi-Level Queue Scheduler...")

    # Define 4 processes for testing (note the 'ptype' attribute)
    # ptype=0 is Foreground (RR), ptype=1 is Background (FCFS)
    processes_mlq = [
        Process(pid=1, arrival_time=0, ptype=0, bursts=[5, 4, 3]), # RR
        Process(pid=2, arrival_time=2, ptype=1, bursts=[4, 2, 4]), # FCFS
        # Process(pid=3, arrival_time=4, ptype=0, bursts=[3, 5, 2]), # RR - should run before P2 if P2 is running
        # Process(pid=4, arrival_time=6, ptype=1, bursts=[4, 3, 4])  # FCFS
    ]

    # Set scheduler parameters
    context_switch_mlq = 2
    time_quantum_rr = 4 # Time quantum for the Round Robin queue

    # Initialize the scheduler
    scheduler = MultiLevelQueueScheduler(processes_mlq, context_switch_mlq, time_quantum_rr)


    # --- Common part for both tests ---
    
    # Run the simulation
    scheduler.run()

    # The Gantt chart data is available in scheduler.gantt_chart
    # You can use it to visualize the chart as you see fit.
    print("\nGantt Chart Data (PID, End Time):")
    scheduler.printGanttChart()
    scheduler.display_results_table()
    # print(scheduler.gantt_chart)
def main():
    """Main function to run the scheduler simulation."""
    print("Welcome to the Advanced CPU Scheduler Simulation!")
    print("1. Preemptive Priority Scheduling with Aging")
    print("2. Multi-Level Queue Scheduling (RR/FCFS)")
    
    choice = input("Please choose the scheduler to run (1 or 2): ")
    
    if choice == '1':
        processes, context_switch, aging_interval = get_priority_aging_input()
        scheduler = PrioritySchedulerWithAging(processes, context_switch, aging_interval)
        print("\nRunning Preemptive Priority Scheduler with Aging...")
    elif choice == '2':
        processes, context_switch, time_quantum = get_multi_level_input()
        scheduler = MultiLevelQueueScheduler(processes, context_switch, time_quantum)
        print("\nRunning Multi-Level Queue Scheduler...")
    else:
        print("Invalid choice. Exiting.")
        return

    # Run the simulation
    scheduler.run()

    # The Gantt chart data is available in scheduler.gantt_chart
    # You can use it to visualize the chart as you see fit.
    print("\nGantt Chart Data (PID, End Time):")
    scheduler.printGanttChart()
    scheduler.display_results_table()

if __name__ == "__main__":
    # hardcodedTests()
    main()
