from scheduler import Scheduler
from process import Process

class MultiLevelQueueScheduler(Scheduler):
    """
    Implements a preemptive Multi-Level Queue Scheduler.

    - Queue 1 (Foreground): Round-Robin (RR) scheduling with high priority.
    - Queue 2 (Background): First-Come, First-Serve (FCFS) scheduling with low priority.
    """
    def __init__(self, processes, context_switch_time, time_quantum):
        # Call the parent constructor
        super().__init__(processes, context_switch_time)
        
        # Specific attributes for this scheduler
        self.time_quantum = time_quantum
        self.rr_queue = []    # High-priority queue
        self.fcfs_queue = []  # Low-priority queue
        
        # Tracks the time slice used by the current RR process
        self.quantum_timer = 0

    def _add_to_ready_queue(self, process: Process):
        """
        Overrides the base method to add processes to the correct queue
        based on their process type (ptype).
        """
        process.state = 'Ready'
        if process.ptype == 0:  # 0 is for Foreground (RR)
            self.rr_queue.append(process)
        else:  # 1 is for Background (FCFS)
            self.fcfs_queue.append(process)

    def _select_next_process(self) -> Process | None:
        """
        Selects the next process to run. It gives absolute priority
        to the high-priority RR queue.
        """
        if self.rr_queue:
            return self.rr_queue.pop(0)
        elif self.fcfs_queue:
            return self.fcfs_queue.pop(0)
        return None

    def _handle_preemption(self):
        """
        Handles preemption for two cases:
        1. A low-priority FCFS process is running, but a high-priority RR process is ready.
        2. A high-priority RR process has used up its time quantum.
        """
        if not self.running_process:
            return

        # Case 1: Preempt FCFS process if a RR process is in the ready queue.
        if self.running_process.ptype == 1 and self.rr_queue:
            preempted_process = self.running_process
            end_time = self.current_time
            self.gantt_chart.append((preempted_process.pid, end_time))
            
            # Put the FCFS process back at the front of its queue
            self.fcfs_queue.insert(0, preempted_process)
            
            self.running_process = None
            self._start_context_switch(end_time)
            return

        # Case 2: Handle RR process and its time quantum.
        if self.running_process.ptype == 0:
            if self.quantum_timer >= self.time_quantum and self.rr_queue:
                # If the RR process is the only one ready, let it continue.
                # This avoids unnecessary context switches.
                if not self.rr_queue and not self.fcfs_queue:
                    self.quantum_timer = 0
                    return
                
                # Otherwise, preempt and move it to the back of the RR queue.
                preempted_process = self.running_process
                end_time = self.current_time
                self.gantt_chart.append((preempted_process.pid, end_time))
                self._add_to_ready_queue(preempted_process)
                self.running_process = None
                self._start_context_switch(end_time)

    def _update_wait_times_and_age(self):
        """No aging is used in this scheduler, so we do nothing."""
        pass

    def run(self):
        """
        Main simulation loop. Overridden from the base Scheduler to handle
        the quantum timer and check both ready queues for idle logic.
        """
        while len(self.terminated_processes) < len(self.processes):
            self.current_time += 1

            # Check for arriving processes
            for p in self.processes:
                if p.state == 'New' and p.arrival_time == self.current_time:
                    self._add_to_ready_queue(p)

            # Check for I/O completion
            for p in self.blocked_queue[:]:
                if p.remaining_burst_time == 1:
                    self.blocked_queue.remove(p)
                    p.go_to_next_burst()
                    self._add_to_ready_queue(p)
                else:
                    p.remaining_burst_time -= 1

            # --- CPU ACTION ---
            if self.is_context_switching:
                if self.current_time >= self.context_switch_end_time:
                    self.is_context_switching = False
                    self.running_process = self._select_next_process()
                    if self.running_process:
                        self.running_process.state = 'Running'
                        # Reset quantum timer for the newly started RR process
                        if self.running_process.ptype == 0:
                            self.quantum_timer = 0
                        if self.running_process.response_time == -1:
                            self.running_process.response_time = self.current_time - self.running_process.arrival_time
            
            elif self.running_process:
                # Increment quantum timer if the running process is RR
                if self.running_process.ptype == 0:
                    self.quantum_timer += 1

                if self.running_process.remaining_burst_time == 1:
                    self._handle_burst_completion()
                else:
                    self.running_process.remaining_burst_time -= 1
                    self.cpu_busy_time += 1
                    self._handle_preemption()
            
            else:  # CPU is idle
                # Check BOTH queues to see if we should start a context switch
                if self.rr_queue or self.fcfs_queue:
                    if self.is_idle:
                        self.gantt_chart.append(('#', self.current_time))
                        self.is_idle = False
                    self._start_context_switch(self.current_time)
                elif not self.is_idle:
                    self.is_idle = True
            
            self._update_wait_times_and_age()
        self._calculate_metrics()

        