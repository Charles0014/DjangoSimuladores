# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 18:23:31 2013

@author: concert
"""

import pickle
import time
import logging
import sys
import asyncore
import os
try:
    import queue
except:
    import Queue as queue
import socket
    
class ServerSocket(asyncore.dispatcher):
    """
    
    """
    def __init__(self, address, sock=None, map=None):
        self.logger = logging.getLogger("ServerSocket")
        self.logger.debug("__init__(address={address}, sock={sock}, map={map})".format(**locals()))
        super().__init__(sock=sock, map=map)
        #self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if sys.version[0] in ("2",):
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)  
            
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind(address)

        self.tx_queue = None
        
        self.listen(10)
        
        return
        
    def set_tx_queue(self, tx_queue):
        self.tx_queue = tx_queue
        return

        
    def handle_accept(self):
        """
        called when a client connect to the listening socket
        should return a client handler
        """        
        sock, address = self.accept()
        self.logger.debug("handle_accept(address={address})".format(**locals()))
        return SocketHandler(sock=sock, map=self._map)
        
        
class SocketHandler (asyncore.dispatcher):
    """
    
    """
    def __init__(self, sock=None, map=None):
        self.logger = logging.getLogger("SocketHandler")
        self.logger.debug("__init__()")
        super().__init__(sock, map)
        self.data_to_write = [] #of bytearrays...
        return
    
    def put(self, msg):
        #debug
        self.logger.debug("msg={}, type={}".format(msg, type(msg)))
        self.data_to_write.append(msg)          
        return
        
    def writable(self):
        return bool(self.data_to_write)
        
    def readable(self):
        return True
        
    def handle_write(self):
        #data = self.data_to_write.popleft()
        data = self.data_to_write.pop(0)
        sent = self.send(data)
        if sent != len(data):
            #self.data_to_write.appendleft(data[sent:])
            self.data_to_write.insert(0, data[sent:])
        return
        
    def handle_read(self):
        data = self.recv(8192)
        #modificar de acordo com a necessidade
        if not data:
            self.logger.debug("handle_close")
            self.close()
        else:
            print('handle_read:{}'.format(data))
        return
        
    def handle_close(self):
        self.logger.debug('handle_close()')
        self.close()
        return
        
if __name__ == "__main__":

    HOST, PORT = "0.0.0.0", 5554

    PATH = os.path.abspath(os.getcwd()) 
    fname = open('{}/scripts/replayihpm/lprout.pickle'.format(PATH), "rb")

    #carrega os dados numa lista com time, data

    
    registers = []   

    PATH = os.path.abspath(os.getcwd()) 
    fd = open('{}/scripts/replayihpm/lprout.pickle'.format(PATH), "rb")

    while True:
        try:
            m = pickle.load(fd)
        except EOFError:
            break

        #timestamp, id, origin, destination, nbytes, list(int)
        if m[3] == '3.0.0.3' and m[4] >= 8:       
            registers.append((m[0], m[-1]))

    print("size={0}".format(len(registers)))
    
    t0 = registers[0][0]
    t1 = registers[-1][0]
    dif = t1 - t0
    print("t1={0}, t0={1}, dif={2}".format(t1, t0, dif))
    
    #exit(0)
    
    
    tx_queue = queue.Queue()    
    socket_map = {}
    SSock = ServerSocket((HOST, PORT), map=socket_map)
    
    
    #agora loop
    
    while True:
        
        while len(socket_map) == 1:
            asyncore.loop(timeout=1.0, count=1, map=socket_map)
            print("waiting for client connections")

        print("Starting registers")
        t0 = time.time()
        r0 = registers[0][0]
        for r in registers:
            
            if len(socket_map) == 1: #no client socket?
                break
            
            #print(r)
            tx_data = bytes(r[1]) #data                

            r1 = r[0]            
            r_dif = r1 - r0 #dif do registro
            
            t1 = time.time() 
            t_dif = t1 - t0
            #t_dif = 0
            
            rt_dif = r_dif - t_dif #dif do t_dif e r_dif

            t0, r0 = t1, r1 #save

            if rt_dif > 0:
                time.sleep(rt_dif)
                
            #print('sleep {0}'.format(rt_dif))
      
            for s in socket_map.values():
                if isinstance(s, SocketHandler):
                    s.put (tx_data)
            
            asyncore.loop(timeout=0.003, count=len(socket_map), map=socket_map)
            
            
