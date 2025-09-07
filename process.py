
from enum import Enum 
class processState(Enum):
    READY = 'READY'
    RUNNING = 'RUNNING'
    WAITING = 'WAITING'
    TERMINATED = 'TERMINATED'
    BLOCKED = 'BLOCKED'
    NEW = 'NEW'


class Process:
    def __init__(self, pid, arrival_time, burst_time,priority = None):
        self.__pid = pid
        self.__arrival_time = arrival_time
        self.__burst_time = burst_time
        self.__remaining_time = burst_time
        self.__state = processState.READY
        self.__start_time = None
        self.__completion_time = None
        self.__waiting_time = 0
        self.__turnaround_time = 0
        self.__priority = priority
        self.__isQueued = False
        self.__isCompleted = False
        self.__response_time = None

    # repr function for easy debugging and logging
    def __repr__(self):
        return (f"Process(pid={self.getPID()}, arrival_time={self.getArrivalTime()}, "
                f"burst_time={self.getBurstTime()}, remaining_time={self.getRemainingTime()}, "
                f"state={self.getState()}, start_time={self.getStartTime()}, "
                f"completion_time={self.getCompletionTime()}, waiting_time={self.getWaitingTime()}, "
                f"turnaround_time={self.getTurnaroundTime()})")

    # reset process to initial state
    def reset(self):
        self.__remaining_time = self.burst_time
        self.__state = processState.READY
        self.__start_time = None
        self.__completion_time = None
        self.__waiting_time = 0
        self.__turnaround_time = 0
        self.__isQueued = False
        self.__isCompleted = False
        self.__response_time = None

    # define getters and setters for all attributes
    def setPID(self, pid):
        self.__pid = pid
    def getPID(self):
        return self.__pid
    def setArrivalTime(self, arrival_time):
        self.__arrival_time = arrival_time
    def getArrivalTime(self):
        return self.__arrival_time
    def setBurstTime(self, burst_time):
        self.__burst_time = burst_time
    def getBurstTime(self):
        return self.__burst_time
    def setRemainingTime(self, remaining_time):
        self.__remaining_time = remaining_time
    def getRemainingTime(self):
        return self.__remaining_time
    def setState(self, state):
        self.__state = state
    def getState(self):
        return self.__state
    def setStartTime(self, start_time):
        self.__start_time = start_time
    def getStartTime(self):
        return self.__start_time
    def setCompletionTime(self, completion_time):
        self.__completion_time = completion_time
    def getCompletionTime(self):
        return self.__completion_time
    def setWaitingTime(self, time=None):
        if time == None:
            self.__waiting_time = self.__turnaround_time - self.__burst_time
        else: 
            self.__waiting_time = time
    def getWaitingTime(self):
        return self.__waiting_time
    def setTurnaroundTime(self, time = None):
        if time == None:
            self.__turnaround_time = self.__completion_time - self.__arrival_time
        else:
            self.__turnaround_time = time
    def getTurnaroundTime(self):
        return self.__turnaround_time
    def setResponseTime(self, time=None):
        if time == None and self.__start_time != None:    
            self.__response_time = self.__start_time - self.__arrival_time
        else:
            self.__response_time = time
    def getResponseTime(self):
        return self.__response_time
    
    # queued status
    def setIsQueued(self, isQueued):
        self.__isQueued = isQueued
    def getIsQueued(self):
        return self.__isQueued
    # completed status
    def setIsCompleted(self, isCompleted):
        self.__isCompleted = isCompleted
    def getIsCompleted(self):
        return self.__isCompleted
    # priority
    def setPriority(self, priority):
        self.__priority = priority  
    def getPriority(self):
        return self.__priority
    
    
    
    