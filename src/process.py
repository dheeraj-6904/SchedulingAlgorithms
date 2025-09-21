import sys

class Process:
    """
    A class to represent a single process for the scheduling simulation.
    """
    def __init__(self, pid, arrival_time, bursts, priority=None, ptype=None):
        self.pid = pid
        self.arrival_time = arrival_time
        self.bursts = bursts  # e.g., [cpu1, io, cpu2]
        self.initial_priority = priority
        self.ptype = ptype # 0 for Foreground (RR), 1 for Background (FCFS)

        # Dynamic attributes
        self.current_priority = self.initial_priority
        self.state = 'New'  # Can be New, Ready, Running, Blocked, Terminated
        self.burst_index = 0
        self.remaining_burst_time = self.bursts[0] if self.bursts else 0
        
        # Metrics
        self.start_time = -1
        self.completion_time = -1
        self.wait_time = 0
        self.turnaround_time = 0
        self.response_time = -1

        # For Aging
        self.time_in_ready_queue = 0
        self.priority_history = [(0, self.initial_priority)]

    @property
    def is_terminated(self):
        """Check if the process has finished all its bursts."""
        return self.burst_index >= len(self.bursts)

    def go_to_next_burst(self):
        """Move to the next burst (CPU or I/O) and update remaining time."""
        self.burst_index += 1
        if not self.is_terminated:
            self.remaining_burst_time = self.bursts[self.burst_index]

    def __repr__(self):
        """String representation for easy debugging."""
        return (f"Process(pid={self.pid}, arrival={self.arrival_time}, "
                f"priority={self.initial_priority}, bursts={self.bursts}, ptype={self.ptype})")
    

    