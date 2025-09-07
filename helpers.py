# print gantt chart
def printGanttChart(ganttChart):
    
    # check jika gantt chart kosong
    if ganttChart is None:
        print("Gantt chart is empty")
        return

    print("Gantt Chart:")

    # create border horizontal
    border = ' '
    for process in ganttChart:
        border += '__' * process[1] + ' '

    # create process label
    label = '|'
    for process in ganttChart:
        space = '_' * (process[1]-1)
        label += space + process[0] + space + '|'

    # display
    print(border)
    print(label)

    time = 0
    # create list to store intervals for each process
    print(time, end="")
    for process in ganttChart:
        print('  ' * (process[1]), end='')
        time += process[1]

        if time > 9:
            print("\b", end="")
            
        print(time, end="")

    print()