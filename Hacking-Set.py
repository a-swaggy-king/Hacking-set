import socket
import pyfiglet
from datetime import datetime
import sys
import nmap
import urllib,re
import rsa
from urllib.request import urlopen
from getmac import get_mac_address


class bcolors:
    YELLOW = '\033[93m'

banner = pyfiglet.figlet_format("Hacking - set")
print(bcolors.YELLOW + banner)
linea = ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
linea2 = ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
hora = datetime.now()
socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
escoje = int(input("Choose option \n 1- see status of 1- 1000 ports \n 2- See status of one port   \n 3- host descovery \n 4- conver host-name <---> IP-address \n 5- web-scrap(email & phone number) \n 6- create or varify a file signature \n Option: "))


def service(port):
    serv = socket.getservbyport(port)
    print(serv)

def un_puerto(port):
    try:
            port2 = 43
            print(linea)
            print("Starting Scan...", hora)
            print(linea,"\n")
            if socket1.connect_ex((host,port)):
                    print("Closed")
            else:
                    print("The Port", port, "is Opened")
                    print("The service running is")
                    service(port)
    except KeyboardInterrupt:
        print ("You pressed Ctrl+C")
        sys.exit()        
def mac(IP="idk"):
    mac2 = get_mac_address(ip=IP)
    print(mac2)
def host_discover():
    try:
            a = nmap.PortScanner()
            print(linea2)
            print("Starting Scan...",hora)
            print(linea2)
            a.scan(hosts=hosts1, arguments="-sn")
            lista_hosts = [(x, a[x] ["status"]["state"]) for x in a.all_hosts()]
            print("Active hosts: \t   Status: \n")
            for host, status in lista_hosts:
                print("MAC:")
                print("IP:\n",host,"\t   ", status," ",mac(host),"\n")
    except KeyboardInterrupt:
        print ("You pressed Ctrl+C")
        sys.exit()  

def allport():
    remoteServer =  input("Enter host to scan: ")
    remoteServerIP  = socket.gethostbyname(remoteServer)

    print("-" * 60)
    print("please wait, scanning remote host", remoteServerIP)
    print("-" * 60)

    t = datetime.now()

    try: 
        for port in range (1,1000):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((remoteServerIP, port))
            if result == 0:
                print("port {}:       open".format(port))
                sock.close()

    except  KeyboardInterrupt:
            print ("You pressed Ctrl+C")
            sys.exit() 

    t2 = datetime.now()

    total_time = t - t2

    print("Scanning completed in:", total_time)

def iphost():

    escoje = int(input("Choose option \n 1- convert host name to ip   \n 2- convert ip to host name \n Option: "))

    def hostip():
        remoteServer1 =  input("Enter host name: ")
        remoteServerIP  = socket.gethostbyname(remoteServer1)
        print(remoteServerIP)

    def iphost():
         remoteServer =  input("Enter ip name: ")
         remoteServername  = socket.gethostbyaddr(remoteServer)
         print(remoteServername)

    if escoje == 1:
        hostip()
    elif escoje == 2:
        iphost()
    else:
        print("Invalid option")

def webScrap():
    print("~" * 60)
    print("scrap phone number and email from a website!")
    print("~" * 60)

    f = urlopen(host)
    s = f.read()
    phone = re.findall(r"\+\d{2}\s?0?\d{10}",s)
    email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",s)
    print(phone, email)

def signature(): 
    escoje = int(input("Choose option \n 1- generate a signature for a file   \n 2- varify a file with a signature \n Option: "))

    def signiture():
        public_key, private_key = rsa.newkeys(1024)

        with open("public.pem", "wb") as f:
            f.write(public_key.save_pkcs1("PEM"))

        with open("private.pem", "wb") as f:
            f.write(private_key.save_pkcs1("PEM"))

        with open ("public.pem", "rb") as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read())

        with open ("private.pem", "rb") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())

        def e_file(file_path , public_key_path, output_path):
            with open(file_path, 'rb') as file:
                data = file.read()

        file_path = input("Enter the name of the file with its extension: ")
        public_key_path = 'public.pem'
        output_path = 'encrypted_file.bin'


        signature = rsa.sign(file_path.encode(), private_key, "SHA-256")

        with open("signature", "wb") as f:
           f.write(signature)



        e_file(file_path, public_key_path, output_path)

    def varify():
        with open ("public.pem", "rb") as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read())

        with open ("private.pem", "rb") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())

        e_file = input("Enter the name of the file with its extension you created a signature for: ")

        with open("signature", "rb") as f:
            signature = f.read()

        print(rsa.verify(e_file.encode(), signature, public_key))

    if escoje == 1:
        signiture()
    elif escoje == 2:
        varify()
    else:
        print("Invalid option")

if escoje == 1:
    allport()
elif escoje == 2:
    host = input("provide the ip address you wanted to scan?\n Host-name or IP-address: ")
    port = int(input("What port do you want to see the status of? \n Port: "))
    un_puerto(port)
elif escoje == 3:
    host = input("provide the ip address you wanted to scan?\n Host: ")
    hosts1 = input("Your subnet (with CIDR x.x.x.x/CIDR) \n Subnet: ")
    host_discover()
elif escoje == 4:
    iphost()
elif escoje == 5:
    host = input("provide the full hostname you wanted to scan?\n Host: ")
    webScrap()
elif escoje == 6:
    signature()
else:
    print("Invalid option")