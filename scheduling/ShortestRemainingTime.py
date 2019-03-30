import turtle
import os

MAX = 100               # Dinh nghia so luong toi da tien trinh trong hang doi readyQueue

class Process:
    def __init__(self, processID, arrivalTime, duration, priority):
        self.processID = processID
        self.arrivalTime = arrivalTime
        self.duration = duration
        self.priority = priority
        self.standbyTime = 0
        self.timeFinish = arrivalTime

class Control:
    def __init__(self):
        self.timer = 0
        self.flag = 0
        self.readyQueue = [None] * MAX
        self.processList = initializeData()
        self.readyQueueSize = 0
        self.processListSize = len(self.processList)
        self.running = None

class gantt:
    def __init__(self, ID, time):
        self.ID = ID
        self.time = time

#   Mang luu cac "Process":   processList
#   Du lieu doc tu file :   data.txt
#
# Ham Khoi tao mang cac "Process"
def initializeData():
    #Doc du lieu tu file va luu vao mang "processList"
    processList = []
    with open ('data.txt') as file:
        array = [[int(x) for x in line.split()] for line in file]
    for i in range(len(array)):
        processList.append(Process('P'+str(array[i][0]), array[i][1], array[i][2], array[i][3]))

    # Ham sap xep cac "Process" trong "ProcessList"
    for i in range(len(processList) - 1):
        for j in range(i + 1, len(processList)):
            # Sap xep lai "processList" theo "arrivalTime" cua "Process"
            if processList[i].arrivalTime < processList[j].arrivalTime:
                processList[i], processList[j] = processList[j], processList[i]
            # Neu hai "process" co cung "arrivalTime" sap xep theo "priority"
            elif processList[i].arrivalTime == processList[j].arrivalTime:
                if processList[i].priority < processList[j].priority:
                    processList[i], processList[j] = processList[j], processList[i]
            j += 1
        i += 1
    return processList

# Ham sap xep hang doi read dua tren do uu tien "duration" cua "process"
def setReadyQueue(process, readyQueue, readyQueueSize):
    if readyQueueSize == 0:
        readyQueue[readyQueueSize] = process
        return readyQueue
    for i in range(readyQueueSize):
        if process.duration < readyQueue[i].duration:
            j = readyQueueSize
            while j > i:
                readyQueue[j] = readyQueue[j-1]
                j -= 1
            readyQueue[i] = process
            return readyQueue
        i += 1
    readyQueue[readyQueueSize] = process
    return readyQueue

# Ham "main" thuat toan "Round Robin"
if __name__ == '__main__':
    ctrl = Control()    # Khoi tao lop dieu khien
    timeProcess = 0.0
    ganttFlowChart = []
    terminated = []
    fileLog = open('log.txt', 'wb')
    for p in ctrl.processList:
        timeProcess += p.duration

    fileLog.write('---------------------BEGIN TIMELINE-----------------\n')
    while True:
        fileLog.write('\nTimer=' + str(ctrl.timer))
        if ctrl.timer < 10:
            fileLog.write('    ')
        else:
            fileLog.write('   ')
        # Day "process" vua toi vao hang doi "readyQueue"
        while ctrl.processList[ctrl.processListSize - 1].arrivalTime == ctrl.timer and ctrl.processListSize > 0:
            ctrl.readyQueue = setReadyQueue(ctrl.processList[ctrl.processListSize - 1], ctrl.readyQueue, ctrl.readyQueueSize)
            fileLog.write('[Move ' + ctrl.processList[ctrl.processListSize - 1].processID + ' to Ready Queue!]')
            ctrl.readyQueueSize  += 1
            ctrl.processListSize -= 1

        # Kiem tra truong hop neu CPU dang ranh - chuyen mot "process" vao running de xu ly
        if ctrl.flag == 0 and ctrl.readyQueueSize > 0:
            ctrl.flag = 1

            # Chuyen mot "process" tu hang doi vao "running"
            ctrl.running = ctrl.readyQueue[0]
            ganttFlowChart.append(gantt(ctrl.running.processID, ctrl.timer))
            # Sap xep lai hang doi sau khi da lay phan tu dau tien
            for i in range(ctrl.readyQueueSize - 1):
                ctrl.readyQueue[i] = ctrl.readyQueue[i + 1]
                i += 1
            ctrl.readyQueueSize -= 1
            # Tinh thoi gian doi "standbyTime" cua "process"
            ctrl.running.standbyTime += ctrl.timer - ctrl.running.arrivalTime
            ctrl.running.arrivalTime = ctrl.timer

        # Kiem tra truong hop neu CPU dang ban xu ly
        if ctrl.flag == 1:
            # So sanh "duration" giua tien trinh trong "running" va "readyQueue"
            # Neu thoi thoi gian xu ly con lai cua tien trinh trong "running" it hon
            # Thay the bang tien trinh trong hang doi "readyQueue"
            if ctrl.readyQueue[0].duration < ctrl.running.duration:
                ganttFlowChart.append(gantt(ctrl.readyQueue[0].processID, ctrl.timer))
                ctrl.running.arrivalTime = ctrl.timer
                fileLog.write('[Move ' + ctrl.running.processID + ' to Ready Queue!]')
                ctrl.running, ctrl.readyQueue[0] = ctrl.readyQueue[0], ctrl.running
                ctrl.running.standbyTime += ctrl.timer - ctrl.running.arrivalTime

            ctrl.running.duration -= 1
            fileLog.write('[Processing process ' + ctrl.running.processID + ']')
            # Neu tien trinh da xu ly xong dua trang thai CPU va dang ranh
            if ctrl.running.duration == 0:
                ctrl.running.timeFinish = ctrl.timer + 1 - ctrl.running.timeFinish
                terminated.append(ctrl.running)
                fileLog.write('[Move ' + ctrl.running.processID + ' to terminated]')
                ctrl.flag = 0

        ctrl.timer += 1

        # Dieu kien de ket thuc thuat toan
        # Neu CPu ranh va khong con "process" nao trong "processList" + "readyQueue"
        if ctrl.processListSize <= 0 and ctrl.readyQueueSize <= 0 and ctrl.flag == 0:
            break
    fileLog.write('\n\n---------------------END TIMELINE-----------------\n\n')

    # Ghi ket qua ra file log
    fileLog.write('Process     Thoi gian cho     Thoi gian thuc thi')
    fileLog.write('\n----------------------------------------------------')
    standbyTime = 0.0
    for i in terminated:
        standbyTime += i.standbyTime
        fileLog.write('\n')
        if i.standbyTime < 10:
            fileLog.write('  ' + i.processID + '              ' + str(i.standbyTime) + '                  ' + str(i.timeFinish))
        else:
            fileLog.write('  ' + i.processID + '             ' + str(i.standbyTime) + '                  ' + str(i.timeFinish))
    fileLog.write('\n----------------------------------------------------')
    fileLog.write('\nThoi gian cho trung binh: ' + str(standbyTime / len(terminated)))
    fileLog.write('\nThoi gian thuc thi trung binh: ' + str(standbyTime / len(terminated) + timeProcess / len(terminated)))
    fileLog.close()

    # Ve gian do gantt
    turtle.setup(width = 1800, height = 400, startx = -900, starty = -500)
    style = ('Courier', 20)
    timeline = turtle.Turtle()
    label = turtle.Turtle()
    timeline.pen(fillcolor = 'white', pensize = 5)
    timeline.pencolor('white')
    label.pencolor('white')
    timeline.setposition(-400, 0)
    label.setposition(-400, -100)
    title = turtle.Turtle()
    title.pencolor('white')
    timeline.pen(fillcolor = 'white', pensize = 5)
    title.setposition(-400, 100)
    title.pencolor('black')
    _style = ('Courier', 25)
    title.write('Shortest Remaining Time', font=_style)
    color1 = 'red'
    color2 = 'blue'
    for i in range(int(timeProcess + 1)):
        for x in ganttFlowChart:
            if i == x.time:
                color1, color2 = color2, color1
                timeline.pencolor(color1)
                timeline.write(i, font = style)
                label.setposition(timeline.pos()[0] + 10, -50)
                label.pencolor('black')
                label.write(x.ID, font = style)
                label.pencolor('white')
        timeline.forward(30)
    timeline.write(i, font = style)
    os.system('gedit ~/scheduling/log.txt')
    raw_input()
