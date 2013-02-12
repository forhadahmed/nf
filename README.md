Python Network Message Formatter (NF)
=====================================

* Python library for generating binary network/packet data for protocol testing.
* Allows for writing network messages in a very human-readable form. 
* Writes raw bytes to `stdout` which can be piped to tools such as `netcat`

Methods
=======

* `byte(b)`   - write 1 byte value 
* `word(w)`   - write 2 byte value
* `dword(dw)` - write 4 byte value
* `qword(qw)` - write 8 byte value
* `bytes(b)`  - write an arbitrary list of bytes
* `text(t)`   - write arbitrary text
* `file(f)`   - write contents of file 

* `ip(ip)`    - write an IP address value represented as a string (with optional padding)
* `mac(mac)`  - write a mac address value represented as a string

Examples
========

BGP Example (`bgp.py'):

        import nf

        #
        #  Write a BGP common header followed by an OPEN message
        #
        #  BGP Common Header Format
        #
        #      0                   1                   2                   3
        #      0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        #     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #     |                                                               |
        #     +                                                               +
        #     |                                                               |
        #     +                                                               +
        #     |                           Marker                              |
        #     +                                                               +
        #     |                                                               |
        #     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #     |          Length               |      Type     |
        #     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

        
        nf.qword(0xffffffffffffffff)  # Marker (bytes 0-8)
        nf.qword(0xffffffffffffffff)  # Marker (bytes 8-16)
        nf.word(13)                   # Length 
        nf.byte(1)                    # Type


        #
        #  BGP OPEN Message Format
        #
        #      0                   1                   2                   3
        #      0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        #      +-+-+-+-+-+-+-+-+
        #      |    Version    |
        #      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #      |     My Autonomous System      |
        #      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #      |           Hold Time           |
        #      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #      |                         BGP Identifier                        |
        #      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #      | Opt Parm Len  |
        #      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #      |                                                               |
        #      |             Optional Parameters (variable)                    |
        #      |                                                               |
        #      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #
        
        nf.byte(0)       # Version
        nf.word(34232)   # Autonomous System
        nf.word(120)     # Hold Time
        nf.ip('1.1.1.1') # BGP Identifier
        nf.byte(0)       # Optional Paremeters Length

 
Verify that the script generates the correct sequence of bytes
 
    python bgp.py | hexdump -C  


Feed the output of this python script to a netcat pipe connected to a BGP router:

    python bgp.py | netcat 192.168.1.1 179












