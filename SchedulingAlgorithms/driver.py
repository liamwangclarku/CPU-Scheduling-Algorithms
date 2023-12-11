import algorithms
from algorithms import Process
import sys

# Code by Liam Wang for Operating Systems 215

class CPU:
    
    # 0 for idle, 1 for running
    running : bool
    curr_process : Process
    duration : int
    cs_time: int # context switch time
    cs_time_left : int # time left for context to switch
    
    def __init__(self, cs_time = 0) -> None:
        self.running = False
        self.curr_process = Process(-1,-1,-1)
        self.cs_time = cs_time
        self.cs_time_left : int = 0
        
    def set_process(self, p : Process, duration):
        # assigns itself the process given and its duration
        self.running = True
        self.curr_process = p
        self.duration = duration
    
    def cycle(self):
        # to simulate the cycles of the CPU
        if self.running:
            self.duration -= 1
            self.curr_process.RT -= 1
            if self.duration <= 0 or self.curr_process.RT <= 0:
                self.running = False
                self.cs_time_left = self.cs_time_left + self.cs_time
            return
        
        if self.cs_time_left > 0:
            self.cs_time_left = self.cs_time_left - 1

        
def last_arrival(data : list[Process]) -> int:
    # to prevent premature exiting of the program
    n : int = 0 
    for i in range(len(data)):
        n += data[i].AT
    return n

def driver(algo : algorithms.Algorithm, CPU_arg : CPU, data):
    # main function responsible for simulating the program
    start = 0
    last_process = False
    ready = []
    completed = []
    data_len = len(data)
    CPU_time = 0
    
    # in the event the user wants context switching
    curr_CPU : CPU = CPU_arg
        

    min_last_cycle = last_arrival(data)
    for w in range(10000):
        # a pseudo while loop
        
        # iterate through processes
        for i in range(start, data_len):
            p : Process = data[i]
            if p.AT == CPU_time:
                ready.append(p)
            elif p.AT > CPU_time:
                start = i
                break
                
        curr_CPU.cycle()
        
        if not curr_CPU.running and curr_CPU.cs_time_left == 0:
            
            run_process = curr_CPU.curr_process
            if run_process.ID != -1:
                if run_process.RT == 0:
                    run_process.set_CT(CPU_time)
                    completed.append(run_process)
                    curr_CPU.curr_process = Process(-1,-1,-1)
                else:
                    ready.append(run_process)
                    curr_CPU.curr_process = Process(-1,-1,-1)

            if len(ready) > 0:        
                instruction = algo.run(ready)
                curr_CPU.set_process(instruction[0], instruction[1])
                ready.remove(instruction[0])
            
            if CPU_time > min_last_cycle: # necessary in the event there are processes that haven't been entered
                last_process = (len(ready) == 0 and curr_CPU.curr_process.ID == -1)
                               
        CPU_time += 1
        
        if last_process and not curr_CPU.running:
            break
    return completed

@staticmethod
def make_processes(data) -> list:
    # requires a 2D list
    dataLen = len(data)
    process_list = []
    
    for i in range(dataLen):
        p = Process(data[i][0], data[i][1], data[i][2])
        process_list.append(p)
    return process_list

@staticmethod
def dismantle_processes(header, data) -> list:
    # breaks the process from a data object, into an array
    dataLen = len(data)
    ls = []
    for i in range(dataLen):
        p : Process = data[i]
        ls.append(p.to_list())
    return [header] + ls

@staticmethod
def displayTable(table : list) -> None:
    # should only take an array of strings as input
    tableLength : int = len(table)
    for i in range(tableLength):
        print(table[i])
    
@staticmethod
def buildTable(data : list) -> None:
    # First row of data should be the header
    header = data[0]
    row = len(data)
    col = len(header)
    
    
    maxColArray = [] # holds the greatest length of an element found in each column
    for j in range(col): 
        maxColArray.append(len(header[j])) # initialize with the header elements
    for i in range(1, row):
        for j in range(col):
            elem = str(data[i][j])
            elemSize = len(elem)
            if elemSize > maxColArray[j]:
                maxColArray[j] = elemSize
    
    # assemble the header
    tableArray = []
    stringBuffer = ""
    vertLine = "  | " # this variable creates the separators
    for j in range(col):
        maxSize = maxColArray[j]
        stringBuffer += fillEmptySpace(header[j], maxSize)
        if j != (col - 1): # if i == last element
            stringBuffer += vertLine
    tableArray.append(stringBuffer)
    
    # add a line separating the header from the data
    stringBuffer = ""
    for j in range(col):
        stringBuffer += "-" * maxColArray[j]
        if j != (col - 1):
            stringBuffer += vertLine.replace(" ", "-")
        else:
            stringBuffer += "-"
    tableArray.append(stringBuffer)
    
    # build each row of the table
    for i in range(1, row):
        stringBuffer = ""
        for j in range(col):
            maxSize = maxColArray[j]
            elem = str(data[i][j])
            elem = fillEmptySpace(elem, maxSize)
            stringBuffer += elem
            if j != (col - 1):
                stringBuffer += vertLine
        tableArray.append(stringBuffer)
    
    return tableArray

@staticmethod
def fillEmptySpace(s : str, maxLength : int):
        inputLength = len(s)
        stringBuffer = s
        if inputLength > maxLength:
            raise ValueError("Max length of a column value is larger than expected")
        diff = maxLength - inputLength
        for i in range(diff):
            stringBuffer = stringBuffer + " "
            #alt = i % 2
            #match alt:
            #    case 0:
            #        stringBuffer = " " + stringBuffer
            #    case 1:
            #        stringBuffer = stringBuffer + " "
            
        return stringBuffer

@staticmethod
def process_file(filename) -> list[int]:
    file_list = []
    with open(filename, "r") as file:
        file_list = file.readlines()
        file.close()
    
    result = []
    for i in range(len(file_list)):
        line = file_list[i]
        line = line.strip()
        line = line.split()
        block = []
        for i in range(len(line)):
            num = int(line[i])
            block += [num]
        result += [block]
    
    return result

@staticmethod
def calc_schedule_len(data : list[Process]) -> int:
    first = data[0]
    last = data[-1]
    return last.CT - first.AT
    
@staticmethod
def avg_TAT(data : list[Process]) -> float:
    data_len = len(data)
    total_TAT = 0
    for i in range(data_len):
        p : Process = data[i]
        total_TAT = p.TAT
    result : float = total_TAT / data_len
    return round(result, 2)

    
            
def main():
    process_args = sys.argv[1:]
    
    args_len = len(process_args)
    
    cs_time = 0
    time_Q = 1
    arg_i = 0
    alg_pick = ""
    while arg_i < args_len:
        arg = process_args[arg_i]
        match arg:
            case "-cs-time":
                arg_i += 1
                cs_time = int(process_args[arg_i])
            case "-round-robin", "rr":
                
                alg_pick = "RR"
                try:
                    time_Q = int(process_args[arg_i + 1])
                    arg_i += 1
                except:
                    time_Q = 1
            case "-sjf":
                alg_pick = "SJF"
            case _:
                process_args = process_args[arg_i:]
                arg_i = args_len
        arg_i += 1
            
                
    
    
    if ".txt" in process_args[0]:
        data = process_file(process_args[0])
    # elif args_len % 3 != 0:
       # raise ValueError("Process args must be input in groups of 3.")
    else:
        data = []
        for i in range(args_len):
            tracker = i % 3
            if tracker == 0:
                process_block = []
            val = int(process_args[i])
            process_block += [val]
            if tracker == 2:
                data += [process_block]
            
    p1 = [1, 1, 3]
    p2 = [2, 2, 4]
    p3 = [3, 3, 1]
    header = ["PID", "AT", "BT", "CT", "TAT", "WT"]
    data = make_processes(data)
    algo = algorithms.pick_algorithm(alg_pick)
    prog_CPU = CPU(cs_time)
    completed = driver(algo, prog_CPU, data) 
    process_list = dismantle_processes(header, completed)
    table = buildTable(process_list)
    
    algo.declare()
    print(f"Context switch time: {cs_time}")
    displayTable(table)
    schedule_len = calc_schedule_len(completed)
    print("Schedule length: " + str(schedule_len))
    print("Avg TAT: " + str(avg_TAT(completed)))
    print("Throughput: " + str(len(completed)) + " / " + str(schedule_len))
    
main()