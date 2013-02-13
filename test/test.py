import os,sys
sys.path.append(os.getcwd())
import nf

nf.ip('100.101.102.103')
nf.ip('111.112.113.114')

nf.start('eth')
nf    .byte(1)
nf    .byte(2)
nf    .length(1)
nf    .byte(3)
nf    .byte(4)
nf    .start('ip')
nf        .ip('1.2.3.4')
nf        .length(4)
nf        .ip('5.6.7.8')
nf        .ip('100.101.102.103')
nf    .end()
nf    .length(4)
nf.end()


