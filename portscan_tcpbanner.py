#print_lock = threading.Lock()

def grab(conn):
    try:
        conn.send('OPEN \r\n')
        ret = conn.recv(1024)
        print '[+]' + str(ret)
    except Exception, e:
        print '[-] Unable to grab any information: ' + str(e)
        
def grab_80(conn):
    try:
        conn.send('HEAD / HTTP/1.0\r\n\r\n')
        ret = conn.recv(1024)
        if (str(ret) == "Protocol mismatch."):
            conn.send('HEAD / HTTP/1.1\r\n\r\n')
            ret = conn.recv(1024)
            
        print '[+]' + str(ret)
    except Exception, e:
        print '[-] Unable to grab any information: ' + str(e)
    

def portscan_tcp(ip_addr, port, delay):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(delay)
    open = False
    conn = ""
    try:
        conn = s.connect((ip_addr,port))
        #with print_lock:
        print "Port " +  str(port) + ": Open"
        open = True
    except socket.timeout:
        print "Socket timeout on " + str(port)
    except (KeyboardInterrupt, SystemExit):
        s.close()
        sys.exit()
    except:
        print "Port " +  str(port) + ": Closed"
        pass

    # Banner Grabbing
    if (open):
        if (port == 80):
            grab_80(s)
        else:
            grab(s)
        s.close()
        
        
    
    
if __name__ == '__main__':
    import threading
    from Queue import Queue
    import time
    import socket
    import sys
    ip_addr = "scanme.nmap.org"
    #ip_addr = raw_input('Enter host to scan: ')
    delay = 5
    for i in range(20, 81):
        portscan_tcp(ip_addr, i, delay)