#
#  NF - [N]etwork message [F]ormatter
#   
#  Usage:
# 
#    byte()
#    bytes()
#    word()
#    dword()
#    qword()
#    text()
#    ip()
#    mac()
#

import sys
import socket

nfblocks = []

def debug_start(block):
    for i in xrange(0,len(nfblocks)):
        sys.stderr.write('  ')
    #end for
    sys.stderr.write("START [%s]\n" % block['name'])
#end def


def debug_end(block):
    for i in xrange(0, len(nfblocks)):
        sys.stderr.write('  ')
    #end for
    sys.stderr.write("END [%s:%d]\n" % (block['name'], block['length']))
#end def


def start(name=''):
    top = dict()
    top['name'] = name
    top['length'] = 0
    top['buffer'] = ''

    debug_start(top)
 
    nfblocks.append(top)
#end def 


def end():
    pop = nfblocks.pop()
 
    debug_end(pop)

    if len(nfblocks) > 0:
        top = nfblocks[-1]
        top['buffer'] += pop['buffer']
        top['length'] += pop['length']
    else:
        sys.stdout.write(pop['buffer'])
    #end if
#end def


def nf_buffer(hex):
    top = nfblocks[-1]
    top['buffer'] += hex
    top['length'] += 1
#end def


def nf_write(b):
    hex = ('\\x%02x' % b).decode('string_escape')
    if len(nfblocks) == 0:
        sys.stdout.write(hex)
        return
    #end if
    nf_buffer(hex)
#end def


def byte (b):
    if b > 0xFF:
        raise Exception, 'byte value > 0xFF';
    #end if
    nf_write(b)
#end def


def word (w):
    if w > 0xFFFF:
        raise Exception, 'word value > 0xFFFF'
    #end if
    byte((w & 0xFF00) >> 8)
    byte((w & 0x00FF) >> 0)
#end def


def dword (dw):
    if dw > 0xFFFFFFFF:
        raise Exception, 'dword value > 0xFFFFFFFF'
    #end if
    word((dw & 0xFFFF0000) >> 16)
    word((dw & 0x0000FFFF) >> 00)
#end def


def qword (qw):
    if qw > 0xFFFFFFFFFFFFFFFF:
        raise Exception, 'qword value > 0xFFFFFFFFFFFFFFFF'
    #end if
    dword((qw & 0xFFFFFFFF00000000) >> 32)
    dword((qw & 0x00000000FFFFFFFF) >> 00)
#end def


def bytes (*bytes):
    for b in bytes:
        byte(b)
    #end for
#end def
 

def ip (ip, pad=0):
    try: # IPv4
        addr = socket.inet_pton(socket.AF_INET, ip)
        if pad: 
            for i in xrange(4,pad): byte(0)
        #endif
    except socket.error:
        try: # IPv6
            addr = socket.inet_pton(socket.AF_INET6, ip)
            if pad: 
                for i in xrange(16,pad): byte(0)
            #endif
        except socket.error:
            raise Exception, "invalid address [%s]" % ip
        #end try IPv6
    #end try IPv4
    for b in addr: byte(ord(b))
#end def






