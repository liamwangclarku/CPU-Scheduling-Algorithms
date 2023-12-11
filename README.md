# CPU-Scheduling-Algorithms
Please read Readme for instructions on how to use

Run program from windows command line with 'python driver.py arg1, arg2, etc.'

Supports reading text files in local path, try 'python driver.py text.txt'

Can also run processes given like so 'python driver.py <ID1> <AT1> <BT1> <ID2> <AT2> <BT2> <ID3> <AT3> <BT3> etc.'
try 'python driver.py 1 1 3 2 2 4 3 3 6'

By default, program runs First Come First Served, to assign a different algorithm, enter the following options:

## Optional arguments are supported:
-cs-time <int>
    to assign a context switch time to every process swap.
    try 'python driver.py -cs-time 4'

-rr <time_q>, or -round-robin <time_q>
    to assign the Round Robin algorithm to the scheduler
    try 'python driver.py -rr 3'

    *time_q argument is optional

-sjf
    to assign Shortest Job First to the scheduler


Because it is command line, you can also use '>' to write the results to a file.
try 'python driver.py test.txt > results.txt'



