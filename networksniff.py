# Material used as aid to help complete assessment listed below:
# Aid: https://pythonprogramming.net/python-threaded-port-scanner/


# Subprocess for this application allows python to make commands usually achieved in a terminal
import subprocess
# Platform is used for multi platform accessibility in relation to conditions. Platform can show the OS type
import platform
# socket is needed to do port scan using the end points while opening up new TCP connection
import socket
# Imports threading for port scanner. Speeds up time it takes to scan
import threading
# Imports que to store new threads (workers)
from queue import Queue
# gives me access to correct date formats for database entry, general CRUD
from datetime import date
# Used for Regular Expressions, for validation
import re

# os being equal to platform allows me to see which OS the user is running so the correct code executes
os = platform
# locks down variables while running to avoid conflicts between threads
print_lock = threading.Lock()

# Will store data for pings and trace routes for future reference
import sqlite3

# Creates sql connection and database
conn = sqlite3.connect('networkstats')

# if conn already exists, pass else create the db for new user
if conn:
    print('You have connected to the db')
else:
    # cursor gives access to execute methods to sqlite3 db
    cursor = conn.cursor()
    # SQL Executes creating table with 3 columns. Primary key and auto increment is on for uniqueness per tuple
    cursor.execute('''CREATE TABLE stats (id INTEGER PRIMARY KEY, service VARCHAR, body VARCHAR, created_on DATE)''')
    # Commit to database
    conn.commit()
    # Close connection
    conn.close()


# Main application class. Yes, the name is rather dodgy, but the context in its functionality is there
class Penatron:

    # First validation method. Looks similar to one below, however, only checks once
    def validation(self,ip):
        if re.match(r'(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$)', ip):
            return True
        else:
            return False

    # Validates host names, example: google.com, www.google.com, www.uws.ac.uk etc.
    def validationDomain(self, domain):
        for pings in domain:
             if re.match('(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$)', pings):
                return True
             else:
                 return False

    # Validates IP using regular expression from the re library
    def validationIP(self, ip):
        for pings in ip:
            # Expression looks for IPV4 pattern
            if re.match(r'\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b', pings):
                return True
            else:
                return False

    # Single host method. Uses 2 methods to ping from, either by ip or host name
    def singlehost(self, method):
        # Data passed into singlehost parameter 'method' is stored into a method variable
        method = method
        result = self.validation(method)

        if result:
            print('No validation issues')
            pass
        else:
            print('Validation issues')
            print(' invalid host name used')
            exit()

        # If statement checks users operating system for compatibility
        if os.system() == "Darwin":
            print('--- OS = MacOS ---')
            print('Running Ping, please wait until completion')
            # Running ping 5 times, then store result into var called 'returned'
            returned = subprocess.run(['ping', '-c 5', method], capture_output=True)
            # Use dict and use the stdout key and return value to stdout var
            stdout = returned.__dict__['stdout']
            # turn returned data into string to avoid any possible issues contained within data
            toString = str(stdout)
            # print to terminal
            print(type(toString))
            print(toString)
            # Save returned data to database
            print('--SAVED TO DATABASE--')
            # Calls static class, passes in service type 'host' and passes in data which processes depending on service type
            Database('host', toString)
            input('press any key to proceed')

        elif os.system() == "Windows":
            print('--- OS = Windows ---')
            print('Running Ping, please wait until completion')
            # Running ping 5 times
            returned = subprocess.run(['ping', method], capture_output=True)
            stdout = returned.__dict__['stdout']
            toString = str(stdout)
            print(toString)
            print('--SAVED TO DATABASE--')
            Database('host', toString)
            input('Continue? press any key')
        else:
            print('Running Ping, please wait until completion')
            print('--- OS = Linux ---')
            # Running ping 5 times
            returned = subprocess.run(['ping', method], capture_output=True)
            stdout = returned.__dict__['stdout']
            toString = str(stdout)
            print(toString)
            print('--SAVED TO DATABASE--')
            Database('host', toString)
            input('Continue? press any key')

    # This method Pings multiple hosts using a for loop and stores each iteration of returned data into the db
    def multiplehostsIP(self, ip):
        method = ip
        result = self.validationIP(method)
        if result:
            print('Validation Passed!')
            if os.system() == "Darwin":
                for choice in method:
                    print('--- OS = MacOS ---')
                    print('Running Ping, please wait until completion')
                    # Running ping 5 times, then store result into var called 'returned'
                    returned = subprocess.run(['ping', '-c 5', choice], capture_output=True)
                    # Use dict and use the stdout key and return value to stdout var
                    stdout = returned.__dict__['stdout']
                    # turn returned data into string to avoid any possible issues contained within data
                    toString = str(stdout)
                    # print to terminal
                    print(type(toString))
                    print(toString)
                    # Save returned data to database
                    print('--SAVED TO DATABASE--')
                    # Calls static class, passes in service type 'host' and passes in data which processes depending on service type
                    Database('host', toString)

            elif os.system() == "Windows":
                for choice in method:
                    print('--- OS = Windows ---')
                    print('Running Ping, please wait until completion')
                    # Running ping 5 times
                    returned = subprocess.run(['ping', choice], capture_output=True)
                    stdout = returned.__dict__['stdout']
                    toString = str(stdout)
                    print(toString)
                    print('--SAVED TO DATABASE--')
                    Database('host', toString)

            else:
                for choice in method:
                    print('Running Ping, please wait until completion')
                    print('--- OS = Linux ---')
                    # Running ping 5 times
                    returned = subprocess.run(['ping', choice], capture_output=True)
                    stdout = returned.__dict__['stdout']
                    toString = str(stdout)
                    print(toString)
                    print('--SAVED TO DATABASE--')
                    Database('host', toString)

        else:
            print('Validation Failed!')
            exit()

    def multiplehostsDomain(self, domain):
        method = domain
        result = self.validationDomain(method)
        if result:
            print('passed validation')
            if os.system() == "Darwin":
                for choice in method:
                    print('--- OS = MacOS ---')
                    print('Running Ping, please wait until completion')
                    # Running ping 5 times, then store result into var called 'returned'
                    returned = subprocess.run(['ping', '-c 5', choice], capture_output=True)
                    # Use dict and use the stdout key and return value to stdout var
                    stdout = returned.__dict__['stdout']
                    # turn returned data into string to avoid any possible issues contained within data
                    toString = str(stdout)
                    # print to terminal
                    print(type(toString))
                    print(toString)
                    # Save returned data to database
                    print('--SAVED TO DATABASE--')
                    # Calls static class, passes in service type 'host' and passes in data which processes depending on service type
                    Database('host', toString)
            elif os.system() == "Windows":
                for choice in method:
                    print('--- OS = Windows ---')
                    print('Running Ping, please wait until completion')
                    # Running ping 5 times
                    returned = subprocess.run(['ping', choice], capture_output=True)
                    stdout = returned.__dict__['stdout']
                    toString = str(stdout)
                    print(toString)
                    print('--SAVED TO DATABASE--')
                    Database('host', toString)
            else:
                for choice in method:
                    print('Running Ping, please wait until completion')
                    print('--- OS = Linux ---')
                    # Running ping 5 times
                    returned = subprocess.run(['ping', choice], capture_output=True)
                    stdout = returned.__dict__['stdout']
                    toString = str(stdout)
                    print(toString)
                    print('--SAVED TO DATABASE--')
                    Database('host', toString)
        else:
            print('validation failed')
            exit()

    # Traceroute function runs the traceroute command, and stores returned data into the db
    def traceroute(self, route):
        # If statement checks users operating system for compatibility
        route = route
        result = self.validation(route)
        if result:
            print(route)
            print('No validation issues')
            if os.system() == "Darwin":
                print('--- OS = MacOS ---')
                print('--- Allow the trace to finish. it is slow, so go get a coffee! Bugs bunny got 20 hops to do ---')
                # Run subprocess using traceroute command, max 20 hops, capture_output true for db
                returned = subprocess.run(['traceroute', '-m 20', route], capture_output=True)
                stdout = returned.__dict__['stdout']
                print(stdout)
                toString = str(stdout)
                Database('trace', toString)
            elif os.system() == "Windows":
                print('--- OS = Windows ---')
                print('--- Allow the trace to finish. it is slow, so go get a coffee! Bugs bunny got 20 hops to do ---')
                returned = subprocess.run(['tracert',  route], capture_output=True)
                stdout = returned.__dict__['stdout']
                print(stdout)
                toString = str(stdout)
                Database('trace', toString)
            else:
                print('--- OS = Linux ---')
                print('--- Allow the trace to finish. it is slow, so go get a coffee! Bugs bunny got 20 hops to do ---')
                returned = subprocess.run(['traceroute', '-m 20', route], capture_output=True)
                stdout = returned.__dict__['stdout']
                print(stdout)
                toString = str(stdout)
                Database('trace', toString)
        else:
            print('Validation issues')
            print('Either the IP is incorrect and not IPV4, or  the domain name length is too big')
            exit()
    # Menu method. Contains logic for menu options.
    def menu(self, choice):
        choice = choice
        # If choice is 1, it will ping single host and call on singlehost method using self, referring to this instance
        if choice == 1:
            # get users host target for ping
            method = input('Please enter the host name, ex: google.com or www.google.com: ')
            # call singlehost, pass in method var containing host target
            self.singlehost(method)
        # if 2, hosts will be stored into list. once user exits, hosts is is passed as argument into multiplehost method
        elif choice == 2:
            # if choice is IP, then append to methodIP list
            methodIP = []
            # if choice is Domain, then append to methodDomain list
            methodDomain = []
            continuation = True
            # Get deciding format from user
            ipordomain = input('Will you use IP 1 or Host 2: ')
            if ipordomain == "1":
                while continuation:
                    enteredtype = input('Insert IP: ')
                    # append user target ip to list
                    methodIP.append(enteredtype)
                    # confirm continue. if not, then loop out
                    confirm = input('Do you wish to add another ip? y or n: ')
                    if confirm == "y":
                        pass
                    else:
                        continuation = False
                self.multiplehostsIP(methodIP)
            elif ipordomain == "2":
                while continuation:
                    enteredtype = input('Insert Host: ')
                    methodDomain.append(enteredtype)
                    confirm = input('Do you wish to add another host? y or n: ')
                    if confirm == "y":
                        pass
                    else:
                        continuation = False
                self.multiplehostsDomain(methodDomain)
            else:
                print('No choice was made')
                exit()
        elif choice == 3:
            # If 3, threaded scanner function will run. Target is host to port scan
            target = input('What is the host: ')
            self.ThreadedScanner(target)
        elif choice == 4:
            # if 4, use traceroute command, passing in target as argument into traceroute method
            target = input('Please enter the host name: ')
            self.traceroute(target)
        elif choice == 5:
            # If 5, show all contents of Database of previous ran executions and returned data
            Database('show', None)
        else:
            print('Please enter an option')
    # Threaded scanner takes a normal port scanner and improves speed by using threads
    def ThreadedScanner(self, ip):

        result = self.validationIP(ip)
        if result:
            print('No validation issues')
            pass
        else:
            print('Validation issues')
            print('Host name is not correct')
            exit()

        # Create scanner function, port will contain number of ports to scan
        def scanner(port):
            # Set internet protocol version 4, open socket stream
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                # make connection attempt. Pass in IP and workers, aka threads count
                connect = sock.connect((ip, port))
                # With print lock to avoid conflicts, print out open ports
                with print_lock:
                    # Print out open ports to screen
                    print('--- Open ---')
                    print('Open Port', port)
                    portString = str('Target was:'+ip+' Open Port: '+port)
                    Database('port', portString)
                # Once execution completes, close connection
                connect.close()
            except:
                # use pass exception, too many threads running
                pass

        # Threader function. Creates new threads and calls on scanner method passing in worker (port num)
        def thread():
            # While true runs loop until tasks are done
            while True:
                # Get a thread
                worker = q.get()
                # Pass in new thread to scanner function < 1 worker = 1 port
                scanner(worker)
                # Finish tasks in que
                q.task_done()

        # Init queue
        q = Queue()

        # run for loop and create 200 threads. Target the thread function
        for x in range(200):
            t = threading.Thread(target=thread)
            # Daemon is needed to finalise and end process
            t.daemon = True
            # init threads
            t.start()

        # assign processes to workers. Port numbers checked [1 to 100]
        for worker in range(1, 101):
            # put worker into the queue
            q.put(worker)

        q.join()


# Database class. This is called as static directly from class. No instances are needed, only 1 db will exist.
class Database:

    # CONSTRUCTOR INIT - Sets up service type 'ping host' or 'show' etc and data being passed in as argument into class.
    def __init__(self,service,data):
        # init all variables for class wide access
        self.conn = sqlite3.connect('networkstats')
        self.data = data
        self.service = service
        self.cur = self.conn.cursor()
        # if the service is host, it will call the inserthost method
        if service == "host":
            self.inserthost(data)
        # if service is show, it will call on show method
        elif service == "show":
            self.show()
        # if service is trace, it will call on insertTrace method
        elif service == "trace":
            self.insertTrace(data)
            # if service is trace, it will call on insertTrace method
        elif service == "port":
            self.insertPorts(data)
        else:
            exit()

    # Inserts pinged host data into db
    def inserthost(self, networkData):
        # Create empty list for diff columns
        statlist = []
        # Returned pinged data put into var
        hostData = networkData
        # Gets todays date
        today = date.today()
        # formats todays date
        d1 = today.strftime("%d/%m/%Y")
        # Appends hardcoded service type
        statlist.append('Network Testing')
        # Append the returned data to the list
        statlist.append(hostData)
        # Append date to list
        statlist.append(d1)
        # Execute the SQL query
        self.cur.execute('''INSERT INTO stats (service, body, created_on) VALUES (?, ?, ?)''',statlist)
        # Commit to the database < no rollbacks
        self.conn.commit()
        # Close connection to the database until next SQL query is executed
        self.conn.close()

    # InsertTrace method works just like previous method. No need for comment repetition
    def insertTrace(self, networkData):
        statlist = []
        hostData = networkData
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        statlist.append('Trace Route Stats')
        statlist.append(hostData)
        statlist.append(d1)
        self.cur.execute('''INSERT INTO stats (service, body, created_on) VALUES (?, ?, ?)''', statlist)
        self.conn.commit()
        self.conn.close()

    def insertPorts(self, networkData):
        statlist = []
        hostData = networkData
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        statlist.append('Port Scanner')
        statlist.append('Open Port:' + hostData)
        statlist.append(d1)
        self.cur.execute('''INSERT INTO stats (service, body, created_on) VALUES (?, ?, ?)''', statlist)
        self.conn.commit()
        self.conn.close()

    # Show method shows all data in the database
    def show(self):
        # Execute SQL query
        self.cur.execute('''SELECT * FROM stats''')
        # Fetch all tuples from stats table
        rows = self.cur.fetchall()
        # If len of rows is less than 1, then no records exist yet, or records are failing to insert
        if len(rows) < 1:
            print('No records exist yet!')
        else:
            # For each row in ALL the rows
            for row in rows:
                # Each row is accessed by its index aka column. row[0] = id. etc
                print('============================================================================')
                print('Stat ID: ', row[0])
                print('Service Ran: ', row[1])
                print('Body: ', row[2])
                print('Executed On:', row[3])
                print('=============================================================================')
        self.conn.commit()
        self.conn.close()

# Call on instance of penetron class. Could have prob chosen better class name.
app = Penatron()
# Counter to detect program running second time
count = 0
continuation = True
while continuation:
    count += 1
    print('Welcome to Troys Network Utilities')
    if count >= 2:
        print('Would you like to continue?')
        confirmProcess = input('y or n:')
        if confirmProcess == 'y':
            # Get user option
            print('please select an option')
            # Visible user interface options of menu screen shown
            print('Please make a choice by following the options')
            print('1) Ping host')
            print('2) Ping Multiple Hosts')
            print('3) Port Scan')
            print('4) Trace Route')
            print('5) View previously ran service stats')
            # Get user input, convert string to int
            user = int(input('Enter number: '))

            # run application, pass in user input for option menu
            app.menu(user)
        else:
            exit()
    # Get user option
    print('please select an option')
    # Visible user interface options of menu screen shown
    print('Please make a choice by following the options')
    print('1) Ping host')
    print('2) Ping Multiple Hosts')
    print('3) Port Scan')
    print('4) Trace Route')
    print('5) View previously ran service stats')
    # Get user input, convert string to int
    user = int(input('Enter number: '))

    # run application, pass in user input for option menu
    app.menu(user)


# PROGRAM DEVELOPMENT COMPLETED ON 01/11/2019 AT 23:10 :) #
