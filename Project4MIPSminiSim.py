# ECE 366 Project 4
# Created by: Jessica Vargas, Vaishnavi Medikundam
# The program takes in MIPS instruction memory in hex and returns data

def MIPSsim(HexInstr, BinInstr):
    size_of_mem = 1024                      # NOT SURE IF FOR SURE CORRECT
    print("Beginning MIPS simulation...")
    print("Info:")
    
    Reg = [0,0,0,0,0,0,0,0]                # the $0-$7 registers initialized to 0
    Mem = [0 for i in range(size_of_mem)]   # creates memory arrary initialized to 0's
    PC =0
    DIC = 0
    numCycles = 0
    threeCyc = 0    # number of instructions that take...3 cycles   
    fourCyc = 0     # number of instructions that take...4 cycles
    fiveCyc = 0     # number of instructions that take...5 cycles

    end = False
    while(not(end)):
        DIC += 1
        fetch = BinInstr[PC]
        if(fetch[0:32] == '00010000000000001111111111111111'):
            PC += 1
            numCycles += 4
            fourCyc += 1
            Reg[int(fetch[16:21],2)] = Reg[int(fetch[6:11],2)] + Reg[int(fetch[11:16],2)] 
            print("deadloop")
            end = True
            
        elif(fetch[0:6] == '000000'): # R-type instructions
            Rs = int(fetch[6:11])
            Rt = int(fetch[11:16])
            Rd = int(fetch[16:21])

            if(fetch[26:32] == '100000'): # 'add'
                PC += 1
                Reg[Rd] = Reg[Rs] + Reg[Rt]
                print("add " + Reg[Rd])
                end = True

            elif(fetch[26:32] == '100010'): # 'sub'
                PC += 1
                Reg[Rd] = Reg[Rs] - Reg[Rt]
                print("sub")
                
            elif(fetch[26:32] == '100110'): # 'xor'
                PC += 1
                Reg[Rd] = Reg[Rs] ^ Reg[Rt]
                print("xor")
                
            elif(fetch[26:32] == '101010'): # 'slt'
                PC += 1
                if(Reg[Rs] < Reg[Rt]):
                    Reg[Rd] = 1
                else:
                    Reg[Rd] = 0
                print("slt")
                
        else:   #I-type instructions
            Rs = int(fetch[7:11],2)
            Rt = int(fetch[11:16],2)
            if(fetch[16] == '0'):
                Imm = int(fetch[16:32],2)
            else:
                Imm = -(65535 -int(fetch[16:32],2)+1)

            if(fetch[0:6] == '001000'): # 'addi'
                PC += 1
                Reg[Rt] = Reg[Rs] + Imm
                print("addi: Rt="+str(Rt)+" Rs="+str(Rs)+" Imm="+str(Imm)+" sum="+str(Reg[Rt]))

            elif(fetch[0:6] == '000001'): # 'beq'
                print("beq start")
                if(Reg[Rs] == Reg[Rt]):
                    PC = 1 + Imm #MIGHT BE WRONG (check if have to divide by 4??)
                else:
                    PC += 1
                print("beq")
                
            elif(fetch[0:6] == '000101'): # 'bne'
                if(Reg[Rs] != Reg[Rt]):
                    PC = 1 + Imm #MIGHT BE WRONG
                else:
                    PC += 1
                print("bne")
                
            elif(fetch[0:6] == '100011'): # 'lw'
                PC += 1
                Imm = int(fetch[16:32],2)
                Reg[Rt] = Mem[((Reg[Rs] + Imm)-hex(0x2000))]
                print("lw")
                
            elif(fetch[0:6] == '101011'): # 'sw'
                PC += 1
                Imm = int(fetch[16:32],2)
                print(Imm)
                Mem[((Reg[Rs] + Imm)-hex(0x2000))] = Reg[Rt]
                print("sw ")

    print("Sim done...")
    
def main():
    i_memfile = open("i_mem2.txt", "r")
    HexInstr = [] #array for instructions in hex
    BinInstr = [] #array for instructions in binary
    for l in i_memfile: #reading each line in txt file
        if (l == "\n" or l[0] == '#'): #skips over empty lines and comments
            continue
        l = l.replace('\n','')
        HexInstr.append(l)
        l = format(int(l,16),"032b")
        BinInstr.append(l)

    MIPSsim(HexInstr, BinInstr) #MIPSsim function

if __name__ == "__main__": #NOT SURE HOW THIS WORKS BUT HERE IN CASE
    main()
