from scheduler import Scheduler

class PrioritySchedulerWithAging(Scheduler):
    """Implements a preemptive priority scheduler with an aging mechanism."""
    def __init__(self, processes, context_switch_time, aging_interval):
        super().__init__(processes, context_switch_time)
        self.aging_interval = aging_interval
        self.ready_queue = sorted(self.ready_queue, key=lambda p: (p.current_priority, p.arrival_time))
        
    def _add_to_ready_queue(self, process):
        process.state = 'Ready'
        process.time_in_ready_queue = 0
        self.ready_queue.append(process)
        self.ready_queue.sort(key=lambda p: (p.current_priority, p.arrival_time))

    def _select_next_process(self):
        if not self.ready_queue:
            return None
        return self.ready_queue.pop(0)

    def _handle_preemption(self):
        if not self.ready_queue:
            return
        
        if self.ready_queue[0].current_priority < self.running_process.current_priority:
            preempted_process = self.running_process
            end_time = self.current_time #+ 1
            self.gantt_chart.append((preempted_process.pid, end_time))
            self._add_to_ready_queue(preempted_process)
            self.running_process = None
            self._start_context_switch(end_time)

    def _update_wait_times_and_age(self):
        """Handles aging for processes in the ready queue."""
        for p in self.ready_queue:
            p.time_in_ready_queue += 1
            if self.aging_interval > 0 and p.time_in_ready_queue > 0 and \
               p.time_in_ready_queue % self.aging_interval == 0:
                if p.current_priority > 0:
                    p.current_priority -= 1
                    p.priority_history.append((self.current_time, p.current_priority))
                    self.ready_queue.sort(key=lambda p: (p.current_priority, p.arrival_time))

    def display_results(self):
        super().display_results()
        print("\n--- Priority Changes (Bonus) ---")
        for p in sorted(self.processes, key=lambda x: x.pid):
            history = " -> ".join([f"P{p.pid} @ t={t}: {pr}" for t, pr in p.priority_history])
            print(f"PID {p.pid}: {history}")