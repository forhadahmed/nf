#
#  nf - [n]etwork message [f]ormatter
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
import struct
import socket


###############################################################################


nf_blocks = []

def debug_indent():
    for i in xrange(0, len(nf_blocks)): sys.stderr.write('  ')
#end def


def debug_start(block):
    debug_indent()
    sys.stderr.write("BEG [%s:%02d]\n" % (block['name'], block['length']))
#end def


def debug_end(block):
    for r in block['rewrites']:
        debug_indent()
        sys.stderr.write("LEN [%d:%d]\n" % (r['offset'], r['length']))
    #end for
    debug_indent()
    sys.stderr.write("END [%s:%02d]\n" % (block['name'], block['length']))
#end def



def nf_length(buffer):
    return len(buffer)
#end def


def nf_rewrite_(buffer, replace, offset, length):
    buffer = buffer[:offset] + replace + buffer[offset+length:]
    return buffer
#end def


def nf_int_buffer(value, length):
    buffer = ''
    if length == 1:
        buffer = struct.pack("!B", value)
    elif length == 2:
        buffer = struct.pack("!H", value)
    elif length == 4:
        buffer = struct.pack("!L", value)
    elif length == 8:    
        buffer = struct.pack("!Q", value)
    else:
        raise Exception, "invalid rewrite length: %d" % length
    #end if
    return buffer
#end def


def nf_rewrite(block):

    buffer = block['buffer']

    for r in block['rewrites']:
        offset = r['offset']
        length = r['length']
        value  = r['func'](block['buffer'])            
        if type(value) is int:
            value = nf_int_buffer(value, length)
            buffer = nf_rewrite_(buffer, value, offset, length)
        elif type(value) is str:
            if len(value) != length:
                raise Exception, "rewrite length mismatch %s", r['func']
            #end if
            buffer = nf_rewrite_(buffer, value, offset, length)
        else:
            raise Exception, "invalid value from  %s" % r['func']
        #end if
    #end for

    block['buffer'] = buffer

#end def


def nf_buffer(hex):
    top = nf_blocks[-1]
    top['buffer'] += hex
    top['length'] += 1
#end def


def nf_write(b):
    hex = struct.pack("!B", b)
    if len(nf_blocks) == 0:
        sys.stdout.write(hex)
        sys.stdout.flush()
        return
    #end if
    nf_buffer(hex)
#end def


###############################################################################


def start(name=''):
    top = dict()
    top['name'] = name
    top['length'] = 0
    top['buffer'] = ''
    top['rewrites'] = []

    #debug_start(top)
 
    nf_blocks.append(top)
#end def 


def end():
    pop = nf_blocks.pop()
 
    #debug_end(pop)

    nf_rewrite(pop)

    if len(nf_blocks) > 0:
        top = nf_blocks[-1]
        top['buffer'] += pop['buffer']
        top['length'] += pop['length']
    else:
        sys.stdout.write(pop['buffer'])
        sys.stdout.flush()
    #end if
#end def


def length(size):
    if len(nf_blocks) == 0:
        raise Exception, "nf.length() used outside start/end block"
    #end if

    if size < 0 or size > 8:
        raise Exception, "nf.length() size '%d' invalid" % size
    #end if

    top = nf_blocks[-1]
    rewrite = dict()
    rewrite['func'] = nf_length 
    rewrite['offset'] = top['length']
    rewrite['length'] = size
    top['rewrites'].append(rewrite)
    
    # fill the buffer space with blank bytes
    for i in xrange(0,size): byte(0xff)
#end def


###############################################################################


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

