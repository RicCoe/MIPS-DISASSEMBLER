
import binascii
def leArquivo(nome):
    with open(nome,'r') as file:
        t=1
        s=[]
        k=[]
        stream=list(file.read())
        for e in stream:
            k.append(e)
            if t%32==0:
                s.append(''.join(k))
                k=[]
            t+=1
        return s
def convert(string):#str eh uma string binaria para ser convertida para dec
    k=0
    string=list(string)
    d=len(string)-1
    while(string !=[]):
        k+=int(string[0])*2**d
        d=d-1
        del string[0]
    return k

def descobreReg(string):
    s=convert(string)
    if s==0:
        return '$zero'
    if s==2:
		return '$v0'
    if s==3:
		return '$v1'
    if (s>=4 and s<=7):
		s=s-4
		return ('$a'+str(s))
    if (s>=8 and s<=15):
        s=s-8
        return ('$t'+str(s))
    if(s>=16 and s<=23):
        s=s-16
        return ('$s'+str(s))
    if(s==24 or s==25):
        s=s-16
        return ('$t'+str(s))
    if s==28:
        return '$gp'
    if s==29:
        return  '$sp'
    if s==30:
        return '$fp'
    if s==31:
        return '$ra'

def descobreInst(inst):
    print(inst)
    if inst[0:6]=='000000':
        if (inst[26:32]=='100000' and inst[21:26]=='00000'):#ADD
            return ('add '+descobreReg(inst[16:21])+', '+descobreReg(inst[6:11])+', '+descobreReg(inst[11:16])+'\n')
        if inst[26:32]=='100010':#SUB
            return  ('sub '+descobreReg(inst[6:11])+', '+descobreReg(inst[11:16])+', '+descobreReg(inst[16:21])+'\n')
        if(inst[26:32]=='100101'):#OR
            return ('or '+descobreReg(inst[6:11])+', '+descobreReg(inst[11:16])+', '+descobreReg(inst[16:21])+'\n')
        if(inst[26:32]=='101010'):#SLT
            return ('slt '+descobreReg(inst[6:11])+', '+descobreReg(inst[11:16])+', '+descobreReg(inst[16:21])+'\n')
    if(inst[0:6]=='000100'):#BEQ
        return ('beq '+descobreReg(inst[6:11])+', '+descobreReg(inst[11:16])+', '+str(convert(inst[16:32]))+'\n')
    if(inst[0:6]=='000010'):#J
        return ('j '+str(convert(inst[6:32]))+'\n')
    if(inst[0:6]=='100000'):#LB
        return ('lb '+descobreReg(inst[6:11])+', '+str(convert(inst[16:32]))+'('+descobreReg(inst[11:16])+')\n')
    if(inst[0:6]=='101000'):#SB
        return ('sb '+descobreReg(inst[11:16])+', '+str(convert(inst[16:32]))+'('+descobreReg(inst[6:11])+')\n')
    if(inst[0:6]=='000011'):#JAL
        return ('jal '+str(convert(inst[6:32]))+'\n')
    if(inst[0:6]=='000001' and inst[11:16]=='000001'):#BGEZ
        return ('bgez '+descobreReg(inst[6:11])+', '+str(convert(inst[16:32]))+'\n')
    if(inst[0:6]=='001000'):#BGT
        return ('bgt '+descobreReg(inst[6:11])+', '+descobreReg(inst[11:16])+', '+str(convert(inst[16:32]))+'\n') 
    if(inst[0:6]=='000000'):    
        if(inst[26:32]=='001110'):#LI
            return ('li '+descobreReg(inst[6:11])+', '+str(convert(inst[6:26]))+'\n')
        if(inst[26:32]=='001111'):#LA
            return ('la '+descobreReg(inst[6:11])+', '+str(convert(inst[11:26]))+'\n')
        if(inst[26:32]=='010000'):#MOVE
            return ('move '+descobreReg(inst[6:11])+', '+descobreReg(inst[11:16])+'\n')
    if(inst[0:6]=='100011'):
        return ('lw '+descobreReg(inst[11:16])+', '+str(convert(inst[26:32]))+'('+descobreReg(inst[6:11])+')\n')
    


def decodifica(t):
    s=[]
    for k in t:
        s.append(descobreInst(k))
    print(s)
    return s

def escreveAssembly(instrucoes):
    with open('traduzido.asm','w') as file:
        for i in instrucoes:
            file.write(str(i))
escreveAssembly(decodifica(leArquivo('mips.txt')))









