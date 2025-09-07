from process import Process, processState

# the scheduler class
class Scheduler:
    def __init__(self,processes:list[Process]):
        self.processes = processes
        self.readyQ: list[Process] = []
        self.current_time = 0
        self.completed_processes:list[Process] = []
        self.n = len(processes)
        self.gantt_chart = []
        self.current_running_process : Process = None
        self.IDLE_time = 0
        self.currentRuntime = 0

        # default priority is arival time
        self.processes.sort(key=lambda x: x.getArrivalTime())
    

    def addProcess(self, process):
        self.processes.append(process)
        self.n += 1
    
    # getters
    def getN(self):
        return self.n
    def getProcesses(self):
        return self.processes
    def getReadyQ(self):
        return self.readyQ
    def getCurrentTime(self):
        return self.current_time
    def getCompletedProcesses(self):
        return self.completed_processes
    def getGanttChart(self):
        return self.gantt_chart
    
    def getRunningProcess(self):
        if self.readyQ[0].getState() == processState.READY:
            process = self.readyQ.pop(0)
            process.setState(processState.RUNNING)

            # check if this is the first time its running
            if process.getStartTime() is None:
                process.setStartTime(self.current_time)
            return process
        else:
            return None
    # setters
    def setCompleteProcess(self, process: Process):
        process.setState(processState.TERMINATED)
        process.setCompletionTime(self.current_time)

        process.setTurnaroundTime()

        process.setResponseTime()
        process.setWaitingTime()

        self.completed_processes.append(process)
        self.processes.remove(process)
        process.setIsQueued(False)
        self.n -= 1
    def setReadyQ(self):
        # Iterate the processes and if its arival time is <= current time then its eligible to be in readyQ

        for process in self.processes:
            if process.getArrivalTime() > self.current_time:
                # Break as all process are sorted on the basis of arrival time
                break
            if not process.getIsQueued() and not process.getIsCompleted():
                process.setState(processState.READY)
                process.setIsQueued(True)
                self.readyQ.append(process)
    def setIDLE_time(self):
        if self.IDLE_time != 0:
            # "##" means cpu is idle for IDLE_time
            self.gantt_chart.append(['##',self.IDLE_time])
            self.IDLE_time = 0

    def execute(self,process:Process):
        self.setIDLE_time()
        # print(process)
        if process != self.current_running_process:
            if self.current_running_process and not self.current_running_process.getIsCompleted():
                self.gantt_chart.append([self.current_running_process.getPID(),self.currentRuntime])
                self.currentRuntime = 0
            self.current_running_process = process

        self.currentRuntime += 1
        self.current_time += 1

        process.setBurstTime(process.getBurstTime() - 1)

        if process.getBurstTime() == 0:
            # print("process complete")
            self.gantt_chart.append([process.getPID(),self.currentRuntime])
            self.setCompleteProcess(process)
            self.currentRuntime = 0
            
            self.current_running_process = None
        
        #else: # as given process is here coz its running still check 
        elif process.getState() == processState.RUNNING:
            process.setState(processState.READY)
            self.readyQ.append(process)

        