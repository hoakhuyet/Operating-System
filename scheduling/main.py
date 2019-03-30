import os

def print_menu():       ## Your menu design here
    print 30 * "-" , "MENU" , 30 * "-"
    print "1. Input Data"
    print "2. Open File Data"
    print "3. FCFS"
    print "4. RR"
    print "5. SJF"
    print "6. SRT"
    print "7. Exit"
    print 67 * "-"

loop=True

while loop:
    print_menu()
    choice = input("Enter your choice [1-7]: ")

    if choice==1:
        print "Menu 1 has been selected"
        os.system('python input.py')
    elif choice==2:
        print "Menu 2 has been selected"
        os.system('gedit ~/scheduling/data.txt')
    elif choice==3:
        print "Menu 3 has been selected"
        os.system('python FIrstComeFirstServed.py')

    elif choice==4:
        print "Menu 4 has been selected"
        os.system('python RoundRobin.py')

    elif choice==5:
        print "Menu 5 has been selected"
        os.system('python ShortJobFirst.py')

    elif choice==6:
        print "Menu 6 has been selected"
        os.system('python ShortestRemainingTime.py')

    elif choice==7:
        print "Menu 7 has been selected"
        break

    else:
        raw_input("Error...")
