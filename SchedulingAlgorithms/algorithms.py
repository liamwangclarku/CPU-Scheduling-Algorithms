from abc import ABC, abstractmethod

class Process:
    # data class for a process
    
    state : str
    ID : int
    AT : int # arrival time
    BT : int # burst/execution time
    CT : int # completion time
    TAT : int # turnaround time
    WT : int # wait time
    RT : int # remaining time
    
    def __init__(self, ID, AT, BT) -> None:
        self.ID = ID
        self.AT = AT
        self.BT = BT
        self.RT = BT

    def get_name(self):
        return "P" + str(self.ID)

    def set_CT(self, n : int):
        self.CT = n
        self.TAT = self.CT - self.AT
        self.WT = self.TAT - self.BT
    
    def to_list(self):
        ls = [self.ID, self.AT, self.BT, self.CT, self.TAT, self.WT]
        return ls

def pick_algorithm(algo_name, extra = 0):
    match algo_name:
        case "RR", "Round Robin":
            return RoundRobin(extra)
        case "SJF":
            return SJF()
        case _:
            return FCFS()

class Algorithm(ABC):
    
    name : str
    preemptive : bool    
    
    @abstractmethod
    def run(self, data):
        pass

    @abstractmethod
    def declare(self):
        print("Algorithm running: " + self.name)

# TODO: Implement more algorithms
class FCFS(Algorithm):
    
    name : str = "First Come First Served (FCFS)"
    
    def run(self, data):
        # Assumes that the first item in the list was the first one entered
        process : Process = data[0]
        return (process, process.BT)
    
    def declare(self):
        print("Algorithm running: " + self.name)
    
class RoundRobin(Algorithm):
    
    name : str = "Round Robin"
    time_Q : int
    
    def __init__(self, n = 1) -> None:     
        self.time_Q = n
    
    def run(self, data):
        # grabs the first item like FCFS, and assigns it the time quantum set
        process : Process = data[0]
        return (process, self.time_Q)
    
    def declare(self):
        print("Algorithm running: " + self.name)
        print(f"Time Quantum: {self.time_Q}")

class SJF(Algorithm):
    
    name : str = "Shortest Job First (SJF)"
    
    def run(self, data):
        # grab the process with the smallest burst time
        shortest = data[0]
        for i in range(1, len(data)):
            p : Process = data[i]
            if p.BT < shortest.BT:
                shortest = p
        return (shortest, shortest.BT)

    def declare(self):
        print("Algorithm running: " + self.name)