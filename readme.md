<h1 style='color:skyblue'>Advanced Scheduling Algorithms Simulation</h1>

This project implements and simulates two advanced CPU scheduling algorithms:
1.  **Preemptive Priority with Aging**: A scheduler that addresses the problem of process starvation.
2.  **Multi-Level Queue**: A scheduler that handles different types of processes (interactive vs. batch) with different scheduling needs.

## <h1 style='color:skyblue'>Comparative Analysis</h1>

### 1. Preemptive Priority Scheduler with Aging

* **Problem Solved**: This algorithm directly solves the critical issue of **starvation** that can occur in standard preemptive priority schedulers. In a simple priority system, a continuous stream of high-priority processes can indefinitely prevent low-priority processes from ever running.
* **How it Solves It**: By implementing **aging**, the scheduler dynamically increases the priority of processes that have been waiting in the ready queue for a long time. Eventually, any waiting process will have its priority raised high enough to be selected for execution, guaranteeing it will not be starved.
* **When to Use It**: This scheduler is ideal for systems where all tasks must eventually be completed, but some are inherently more urgent than others. A good scenario would be an operating system managing background system tasks (like indexing files or running a virus scan) alongside user-facing applications. While the user's application should have higher priority for responsiveness, the system tasks should not be postponed forever.

### 2. Multi-Level Queue Scheduler

* **Problem Solved**: This algorithm addresses the need to provide different levels of service to different classes of processes. **Interactive (foreground) processes** require a very low response time to feel responsive to the user, while **batch (background) processes** primarily need high throughput to finish their work efficiently, and response time is not a major concern.
* **How it Solves It**: It segregates processes into different queues, each with its own scheduling algorithm. Our implementation uses a high-priority queue with Round-Robin (RR) for interactive jobs and a low-priority queue with First-Come, First-Serve (FCFS) for batch jobs. The high-priority queue gets absolute preference, ensuring that as long as an interactive task is ready, it will run, providing excellent response times. The batch jobs are processed only when no interactive tasks are pending.
* **When to Use It**: This is the model used in most modern general-purpose operating systems (like Windows, macOS, and Linux). A perfect scenario is a developer's workstation. The text editor or IDE the developer is actively using is an interactive, foreground process that needs immediate response. In the background, a large software project might be compiling—a batch process that can be preempted whenever the developer types a character in the editor.

### <h2 style = "color:skyblue"> Conclusion</h1>

| Feature | Priority with Aging | Multi-Level Queue |
| :--- | :--- | :--- |
| **Primary Goal** | Prevent Starvation | Differentiate Service for Process Types |
| **Mechanism** | Dynamic Priority Increase | Static Queues with Different Algorithms |
| **Best Use Case** | Systems with mixed-urgency tasks that all must run. | Systems with a clear distinction between interactive and batch jobs. |

<h1 style='color:skyblue'>Results</h1>
 ** shows context switches, ## shows idle time

```Welcome to the Advanced CPU Scheduler Simulation!
--- Running in Hardcoded Test Mode ---

Running Multi-Level Queue Scheduler...

Gantt Chart Data (PID, End Time):

Gantt Chart:
 ____ __________ ______ __ ____ ______ ______ ______ ____ ____ ________
|_**_|____P1____|__**__|P2|_**_|__P1__|__**__|__P2__|_##_|_**_|___P2___|
0    2          7     10 11   13     16     19     22   24   26       30

--- Final Metrics Summary ---
PID  Arrival CPU 1   I/O     CPU 2   Type      Response  Waiting   Turnaround
-------------------------------------------------------------------------------
1    0       5       4       3       FG(RR)    2         4         16
2    2       4       2       4       BG(FCFS)  8         18        28
-------------------------------------------------------------------------------
Average:                                       5.00      11.00     22.00

CPU Utilization: 53.33%
```