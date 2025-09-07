from schedular import Scheduler

class PriorityPreemptive(Scheduler):
    def __init__(self, processes):
        super().__init__(processes)

    def run(self):
        while self.n > 0:
            self.setReadyQ()

            # check if readyQ is empty i.e, no process has arrived
            if not self.readyQ:
                self.current_time += 1
                self.currentRuntime += 1
                continue
            
            # sort the pq based on priority
            self.readyQ.sort(key = lambda x: (x.getPriority(),x.getArrivalTime()))

            # get the top process
            process = self.getRunningProcess()

            #  execute ir
            self.execute(process)




        