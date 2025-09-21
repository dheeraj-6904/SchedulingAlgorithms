from abc import ABC, abstractmethod

class Scheduler(ABC):
    """
    Abstract base class for all scheduling algorithms.
    This final version uses a corrected simulation loop structure.
    """
    def __init__(self, processes, context_switch_time):
        self.processes = sorted(processes, key=lambda p: p.arrival_time)
        self.context_switch_time = context_switch_time
        
        # Start time at -1 so the first tick of the simulation is t=0
        self.current_time = -1
        
        self.running_process = None
        self.ready_queue = []
        self.blocked_queue = []
        self.terminated_processes = []
        
        self.gantt_chart = []
        self.cpu_busy_time = 0
        
        self.is_context_switching = False
        self.is_idle = False
        self.context_switch_end_time = 0

    def run(self):
        """Main simulation loop with time incremented at the start."""
        
        while len(self.terminated_processes) < len(self.processes):
            # 1. ADVANCE TIME
            # Time is incremented at the beginning of the loop.
            self.current_time += 1

            # 2. UPDATE QUEUES
            # Handle all arrivals and I/O completions that happen at this exact time.
            for p in self.processes:
                if p.state == 'New' and p.arrival_time == self.current_time:
                    self._add_to_ready_queue(p)

            for p in self.blocked_queue[:]:
                if p.remaining_burst_time == 1: # Was 1, now becomes 0
                    self.blocked_queue.remove(p)
                    p.go_to_next_burst()
                    self._add_to_ready_queue(p)
                else:
                    p.remaining_burst_time -= 1

            # 3. EXECUTE CPU ACTION
            # Decide what the CPU is doing during the tick from t to t+1.
            if self.is_context_switching:
                if self.current_time >= self.context_switch_end_time:
                    self.is_context_switching = False
                    self.running_process = self._select_next_process()
                    if self.running_process:
                        self.running_process.state = 'Running'
                        if self.running_process.response_time == -1:
                            self.running_process.response_time = self.current_time - self.running_process.arrival_time
            
            elif self.running_process:
                if self.running_process.remaining_burst_time == 1:
                    self._handle_burst_completion() # Will finish at end of this tick
                else:
                    self.running_process.remaining_burst_time -= 1
                    self.cpu_busy_time += 1
                    self._handle_preemption()
            
            else: # CPU is idle
                if self.ready_queue:
                    if self.is_idle:
                        self.gantt_chart.append(('#', self.current_time))
                        self.is_idle = False
                    self._start_context_switch(self.current_time)
                elif not self.is_idle:
                     self.is_idle = True
            
            self._update_wait_times_and_age()

        self._calculate_metrics()

    def _start_context_switch(self, start_time):
        self.is_context_switching = True
        self.context_switch_end_time = start_time + self.context_switch_time
        self.gantt_chart.append(('*', self.context_switch_end_time))

    def _handle_burst_completion(self):
        process = self.running_process
        self.cpu_busy_time += 1
        
        # An action during tick 't' finishes at the moment 't+1'
        end_time = self.current_time # + 1
        self.gantt_chart.append((process.pid, end_time))
        
        process.go_to_next_burst()
        
        if process.is_terminated:
            process.state = 'Terminated'
            process.completion_time = end_time
            self.terminated_processes.append(process)
        else:
            process.state = 'Blocked'
            self.blocked_queue.append(process)
        
        self.running_process = None
        
        if self.ready_queue:
            self._start_context_switch(end_time)

    def _calculate_metrics(self):
        """Calculate TAT, WT for all processes."""
        # This function remains correct.
        total_wt, total_tat, total_rt = 0, 0, 0
        if not self.processes: return

        for p in self.processes:
            cpu_bursts_total = sum(p.bursts[i] for i in range(0, len(p.bursts))) # include io burts also
            if p.completion_time != -1:
                p.turnaround_time = p.completion_time - p.arrival_time
                p.wait_time = p.turnaround_time - cpu_bursts_total
                total_wt += p.wait_time
                total_tat += p.turnaround_time
                total_rt += p.response_time if p.response_time != -1 else 0
    
        self.avg_wt = total_wt / len(self.processes)
        self.avg_tat = total_tat / len(self.processes)
        self.avg_rt = total_rt / len(self.processes)
        final_time = self.gantt_chart[-1][1] if self.gantt_chart else self.current_time
        if final_time > 0: self.cpu_utilization = (self.cpu_busy_time / final_time) * 100
        else: self.cpu_utilization = 0

    # def display_results(self):
    #     """Prints the final results and metrics."""
    #     # This function remains correct.
    #     print("\n--- Final Metrics ---")
    #     for p in sorted(self.processes, key=lambda x: x.pid):
    #         print(f"PID: {p.pid}, WT: {p.wait_time}, TAT: {p.turnaround_time}, RT: {p.response_time}")
        
    #     print(f"\nAverage Waiting Time: {self.avg_wt:.2f}")
    #     print(f"Average Turnaround Time: {self.avg_tat:.2f}")
    #     print(f"Average Response Time: {self.avg_rt:.2f}")
    #     print(f"CPU Utilization: {self.cpu_utilization:.2f}%")
    def display_results_table(self):
        """Prints the final results and metrics in a formatted table."""
        if not self.processes:
            print("No processes to display.")
            return

        print("\n--- Final Metrics Summary ---")

        # Determine if we're dealing with Priority or Type for the header
        has_priority = hasattr(self.processes[0], 'initial_priority') and self.processes[0].initial_priority is not None
        has_ptype = hasattr(self.processes[0], 'ptype') and self.processes[0].ptype is not None
        
        # Define table headers
        headers = ["PID", "Arrival", "CPU 1", "I/O", "CPU 2"]
        if has_priority:
            headers.append("Priority")
        if has_ptype:
            headers.append("Type")
        headers.extend(["Response", "Waiting", "Turnaround"])

        # Define column widths for alignment
        widths = {'PID': 5, 'Arrival': 8, 'CPU 1': 8, 'I/O': 8, 'CPU 2': 8, 
                  'Priority': 10, 'Type': 10, 'Response': 10, 'Waiting': 10, 'Turnaround': 12}

        # Build and print the header row
        header_str = "".join([f"{h:<{widths[h]}}" for h in headers])
        print(header_str)
        print("-" * len(header_str))

        # Print data for each process
        for p in sorted(self.processes, key=lambda x: x.pid):
            row = [
                f"{p.pid:<{widths['PID']}}",
                f"{p.arrival_time:<{widths['Arrival']}}",
                f"{p.bursts[0]:<{widths['CPU 1']}}",
                f"{p.bursts[1]:<{widths['I/O']}}",
                f"{p.bursts[2]:<{widths['CPU 2']}}",
            ]
            if has_priority:
                row.append(f"{p.initial_priority:<{widths['Priority']}}")
            if has_ptype:
                ptype_str = "FG(RR)" if p.ptype == 0 else "BG(FCFS)"
                row.append(f"{ptype_str:<{widths['Type']}}")
            
            row.extend([
                f"{p.response_time:<{widths['Response']}}",
                f"{p.wait_time:<{widths['Waiting']}}",
                f"{p.turnaround_time:<{widths['Turnaround']}}",
            ])
            print("".join(row))

        # Print the footer with averages
        print("-" * len(header_str))
        
        # Calculate padding to align the "Average" label
        avg_label = "Average:"
        padding_cols = ["PID", "Arrival", "CPU 1", "I/O", "CPU 2"]
        if has_priority: padding_cols.append("Priority")
        if has_ptype: padding_cols.append("Type")
        
        padding_width = sum(widths[col] for col in padding_cols)
        
        avg_row = (
            f"{avg_label:<{padding_width}}"
            f"{self.avg_rt:<{widths['Response']}.2f}"
            f"{self.avg_wt:<{widths['Waiting']}.2f}"
            f"{self.avg_tat:<{widths['Turnaround']}.2f}"
        )
        print(avg_row)

        print(f"\nCPU Utilization: {self.cpu_utilization:.2f}%")
    @abstractmethod
    def _add_to_ready_queue(self, process): pass
    @abstractmethod
    def _select_next_process(self): pass
    @abstractmethod
    def _handle_preemption(self): pass
    @abstractmethod
    def _update_wait_times_and_age(self): pass

    def printGanttChart(self):
        """
        Prints a formatted ASCII Gantt chart from scheduler data.
        """
        ganttChart = self.gantt_chart
        # 1. Check if the Gantt chart data is empty
        if not ganttChart:
            print("Gantt chart is empty.")
            return

        print("\nGantt Chart:")

        top_border = " "
        middle_labels = "|"
        last_time = 0

        # 2. Build the top border and middle label strings by iterating through the chart data
        for process_id, end_time in ganttChart:
            duration = end_time - last_time
            
            # Define a visual width for the segment (e.g., 2 characters per time unit)
            segment_width = duration * 2 

            # --- Build Top Border ---
            top_border += "_" * segment_width + " "

            # --- Build Middle Labels ---
            # Format the label based on the process_id
            if process_id == '*':
                label = '**'
            elif process_id == '#':
                label = '##'
            else:
                label = f"P{process_id}"
            
            # Center the label within the segment, padded by underscores
            padding = segment_width - len(label)
            left_pad = padding // 2
            right_pad = padding - left_pad
            middle_labels += "_" * left_pad + label + "_" * right_pad + "|"
            
            last_time = end_time
        
        # 3. Build the bottom time-line string
        # Create a list of all the time points, starting with 0
        times = [0] + [item[1] for item in ganttChart]
        time_line = ""
        
        for i in range(len(times)):
            time_str = str(times[i])
            time_line += time_str
            
            # Add spacing to align the next number under the next pipe separator
            if i < len(times) - 1:
                start_time = times[i]
                end_time = times[i+1]
                duration = end_time - start_time
                
                # Calculate spaces needed: segment width + 1 for the border space, 
                # then subtract the length of the number we just printed.
                spaces_needed = (duration * 2) + 1 - len(str(times[i+1]))
                time_line += " " * spaces_needed

        # 4. Print all the assembled parts
        print(top_border)
        print(middle_labels)
        print(time_line)

