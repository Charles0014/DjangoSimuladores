#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 14 10:12:04 2014

@author: pedro
"""

import socket
import select
import subprocess
#import netifaces

_CALL_CMDS = {'server_top_reset': 'kill -s USR1 $(pidof mtr_server)',
         'interface_top_reset':   'kill -s USR1 $(pidof mtr_ep_interface)',
         'server_top_simulate':   'kill -s URG  $(pidof mtr_server)',
         'time_sync_seconds':     'kill -s USR2 $(pidof mtr_server)',
         'time_sync_full':        'kill -s ALRM $(pidof mtr_server)',
         'server_top_clear':      'kill -s TSTP $(pidof mtr_server)',
}
            
_POPEN_CMDS = {'list': 'ls',
                'firefox_ps': 'pidof firefox',
                'ifconfig': 'ip addr show | grep "inet "',
                'date': 'date',
               
}

txSock = None
rxSock = None

_HOST_IP = '127.0.0.1' 
_BCAST_IP = None
_BCAST_ADDR = None

#def load_this_host_ip():
#    cmd1 = 'ip addr show'
#    cmd2 = 'grep "inet "'
#    cmd3 = 'grep global'
#    pipe1 = subprocess.Popen(list(cmd1.split(' ')), stdout=subprocess.PIPE)
#    pipe2 = subprocess.Popen(list(csv.reader([cmd2,], delimiter=' '))[0],
#                             stdin=pipe1.stdout,
#                             stdout=subprocess.PIPE)
#    pipe3 = subprocess.Popen(list(cmd3.split(' ')), 
#                             stdin=pipe2.stdout,                             
#                             stdout=subprocess.PIPE)
#    for s in pipe3.stdout:
#        print(s)
#        lst = s.decode('us-ascii').strip().split(' ')
#        
#        saddr = lst[1]
#        print('lst', lst, 'saddr', saddr)
#        addr=saddr[:saddr.index('/')]
#        print('ADDR=', addr)       
#    # algo como:
#    #inet 192.168.0.59/24 brd 192.168.0.255 scope global dynamic wlp3s0\n
#

def load_this_host_ip(ifname='eth0', host_addr='127.0.0.1', bcast_addr='127.0.0.1'):
    global _HOST_IP, _BCAST_IP
    _HOST_IP = host_addr
    _BCAST_IP = bcast_addr
    
    
def ninstances():
    cmd1 = 'ps aux | grep python3 | grep -v grep | grep CtrlClient.py | wc -l'
    pipe = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE)
    s = ''
    for l in pipe.stdout:
        s += l.decode('us-ascii')
    n = int(s, 10)
    return n
    
def process_call_command(key, mydict, txSock):
    cmd = _CALL_CMDS.get(key, None)
    ret = subprocess.call(cmd, shell=True)
    msg = "host='{}'\ncmd='{}'\nerror={}".format(_HOST_IP, key,ret)
    print("msg", msg)
    txSock.sendto(msg.encode('us-ascii'), _BCAST_ADDR)
    
def process_popen_command(key, mydict, txSock):
    cmd = _POPEN_CMDS.get(key, None)
    pipe = subprocess.Popen(cmd,
                            shell=True,
                            stdout=subprocess.PIPE)
    
    header = "host='{}'\ncommand='{}'\nresult='".format(_HOST_IP,key)  
    s = header.encode('us-ascii')
    for line in pipe.stdout:
        s += line
    s += b'\'\n'            

    dicts = '\n'.join(["{}={}".format(a,b) for a,b in mydict.items()])
    s += "#request\n".encode('us-ascii')                          
    s += dicts.encode('us-ascii')
    print('s=', s)                                        
    txSock.sendto(s, _BCAST_ADDR)
    
def process_commands(lst_cmds, mydict, txSock):
    """
    lst_cdms should be a list of known commands.
    Ex.: ['top_reset', 'top_simulate']
    """
    for key in lst_cmds:
        #ex. cmd: top_reset
        # procurar no dict _CMDS
        if key in _CALL_CMDS:
            print("call key=", key)
            process_call_command(key, mydict, txSock)
        elif key in _POPEN_CMDS:
            print("popen key=", key)            
            process_popen_command(key, mydict, txSock)
            
        
def process_message(s, data, txSock):
    d = {}
    try:
        exec(s, None, d)
        data.update(d)
        print('data', d, data)
        
        # Executar so for broadcast
        # ou se for enderecado a este host
        host = d.get('host', None)
        if not host or host == _HOST:
            for key in d:
                if key in ('commands', ):
                    scmd = d[key]
                    print('scmd=', scmd)
                    process_commands(scmd, d, txSock)
                
    except SyntaxError as e:
        print(e)   
    except NameError as e:
        print(e)


def loop(eth='eth0', udp_bind_port=45678, udp_bcast_port=45679, host_addr='127.0.0.1', bcast_addr='127.0.0.1'):

    global _BCAST_ADDR
    
    print('eth', eth)
    print('udp_bind_port', udp_bind_port)
    print('udp_bcast_port', udp_bcast_port)
    print('host_addr', host_addr)
    print('bcast_addr', bcast_addr)

    
    load_this_host_ip(ifname=eth, host_addr=host_addr, bcast_addr=bcast_addr)
    
    UDP_LISTEN_PORT = udp_bind_port
    UDP_BCAST_PORT = udp_bcast_port
   
     
    _BCAST_ADDR=(bcast_addr, UDP_BCAST_PORT)
    
    print('bcast_addr', _BCAST_ADDR)
    
    print('udp_listen_port', UDP_LISTEN_PORT, 'udp_bcast_addr', UDP_BCAST_PORT)

    #_BCAST_ADDR=('127.0.0.1', UDP_BCAST_PORT)
    
    rxSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    txSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    
    #make both a bcast_aware and reuse_addr
    rxSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    rxSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    rxSock.bind(('0.0.0.0', UDP_LISTEN_PORT))
    
    txSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    txSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    print('txSock', txSock)
    print('rxSock', rxSock)

    epoll = select.epoll()
    epoll.register(rxSock.fileno(), select.EPOLLIN)
    
    data = {}    
    while True:
        events = epoll.poll(timeout=1)
        if len(events) == 0:
            pass
            #print('loop timeout')
        else:
            for fd, event in events:
                if fd == rxSock.fileno() and event & select.EPOLLIN:
                    msg,remaddr = rxSock.recvfrom(1024)
                    print(remaddr, msg)
                    s = msg.decode('us-ascii')
                    process_message (s, data, txSock)

    print("Leaving loop, bye!")

# usar main para debug
if __name__ == "__main__":
    try:
        loop(eth='eth0', udp_bind_port=45678, udp_bcast_port=45679, host_addr='127.0.0.1', bcast_addr='127.0.0.1')
    except KeyboardInterrupt as e:
        print("   Bye!")
        exit(0)


                        
