import struct
#
#typedef struct T_Header {
#    struct timespec ts_;            16
#    uint32_t size_;                  4 20
#    uint32_t prev_;                  4 24
#    uint32_t next_;                  4 28
#                                     4 32 //auto filler            
#    struct sockaddr_in sockaddr_;  //from 16 48
#} T_Header;


import socket
import time
import os

def replay_file(fname):
    f = open (fname, "rb")
    fmt = "LLIIII4I"
    while True:
        try:
            h = f.read(48)
            hv = struct.unpack(fmt, h)
            #print hv
            size = hv[2]
            #print size, type(size)
            buf = f.read(size)
            #print "len", len(buf)
        except EOFError:
            break


def replay_file_to_socket(fname, sock, addr):
    f = open (fname, "rb")
    fmt = "4I4I4I"
    t0 = 0
    while True:
        try:
            h = f.read(48)
            hv = struct.unpack(fmt, h)
            #print hv
            size = hv[4] # ts_sec, 0, ts_nsec, 0, size, prev, next 
            t = hv[0] + hv[2]/1e9 
            #print size, type(size)
            buf = f.read(size)
            mstr = ""
            if size == 60:
                for i in range(0, 30):
                    mstr += " " + str(ord(buf[i]))
                #print mstr
            #print "len", len(buf)
            csock.sendto(buf, addr)
            if t0:
                dif = t - t0
                time.sleep (dif)
            t0 = t

        except EOFError:
            break
    replay_file_to_socket(fname, sock, addr);

addr = ('127.0.0.1', 1200)
csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
csock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
csock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#fname = "E:/Maycon/Projetos/SITDR/documentacao/desenvolvimento/sisrot/Sisrot/134156.bin"


PATH = os.path.abspath(os.getcwd())
fname = "{}/scripts/sisrot/lancamento.bin".format(PATH)
while True:
    print "looping"
    replay_file_to_socket(fname, csock, addr)
    
