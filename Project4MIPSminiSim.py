# ECE 366 Project 4
# Created by: Jessica Vargas, Vaishnavi Medikundam
# The program takes in MIPS instruction memory in hex and returns data

def MIPSsim(HexInstr, BinInstr, Part2):
    size_of_mem = 1024                      # NOT SURE IF FOR SURE CORRECT
    print("-------------------------\nBeginning MIPS simulation...\n-------------------------")
    
    Reg = [0,0,0,0,0,0,0,0]                # the $0-$7 registers initialized to 0
    Mem = [0 for i in range(size_of_mem)]   # creates memory array initialized to 0's
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
            if(Part2):
                print("deadloop")
            end = True
            
        elif(fetch[0:6] == '000000'): # R-type instructions
            Rs = int(fetch[6:11],2)
            Rt = int(fetch[11:16],2)
            Rd = int(fetch[16:21],2)

            if(fetch[26:32] == '100000'): # 'add'
                PC += 1
                Reg[Rd] = Reg[Rs] + Reg[Rt]
                if(Part2):
                    print("add $"+str(Rd)+",$"+str(Rs)+",$"+str(Rt))

            elif(fetch[26:32] == '100010'): # 'sub'
                PC += 1
                Reg[Rd] = Reg[Rs] - Reg[Rt]
                if(Part2):
                    print("sub $"+str(Rd)+",$"+str(Rs)+",$"+str(Rt))
                
            elif(fetch[26:32] == '100110'): # 'xor'
                PC += 1
                Reg[Rd] = Reg[Rs] ^ Reg[Rt]
                if(Part2):
                    print("xor $"+str(Rd)+",$"+str(Rs)+",$"+str(Rt))
                
            elif(fetch[26:32] == '101010'): # 'slt'
                PC += 1
                if(Reg[Rs] < Reg[Rt]):
                    Reg[Rd] = 1
                else:
                    Reg[Rd] = 0
                if(Part2):
                    print("slt $"+str(Rd)+",$"+str(Rs)+",$"+str(Rt))
            else:
                end = True
                
        else:   #I-type instructions
            Rs = int(fetch[6:11],2)
            Rt = int(fetch[11:16],2)
            if(fetch[16] == '0'):
                Imm = int(fetch[16:32],2)
            else:
                Imm = -(65535 -int(fetch[16:32],2)+1)

            if(fetch[0:6] == '001000'): # 'addi'
                PC += 1
                Reg[Rt] = Reg[Rs] + Imm
                if(Part2):
                    print("addi $"+str(Rt)+",$"+str(Rs)+","+str(Imm))

            elif(fetch[0:6] == '000100'): # 'beq'
                if(Reg[Rs] == Reg[Rt]):
                    PC = PC + Imm + 1 
                else:
                    PC += 1
                if(Part2):
                    print("beq $"+str(Rs)+",$"+str(Rt)+","+str(Imm))
                
            elif(fetch[0:6] == '000101'): # 'bne'
                if(Reg[Rs] != Reg[Rt]):
                    PC = PC + Imm + 1 
                else:
                    PC += 1
                if(Part2):
                    print("bne $"+str(Rs)+",$"+str(Rt)+","+str(Imm))
                
            elif(fetch[0:6] == '100011'): # 'lw'
                PC += 1
                Reg[Rt] = Mem[((Reg[Rs] + Imm)-8192)]
                if(Part2):
                    print("lw $"+str(Rt)+","+str(Imm)+"($"+str(Rs)+")")
                
            elif(fetch[0:6] == '101011'): # 'sw'
                PC += 1
                Mem[((Reg[Rs] + Imm)-8192)] = Reg[Rt]
                if(Part2):
                    print("sw $"+str(Rt)+","+str(Imm)+"($"+str(Rs)+")")
                
            else:
                end = True

    print("-------------------------\nSimulation done...\n-------------------------")
    print("*Results*:")
    print("Dynamic Instruction Count: " + str(DIC))
    print("PC: " + str(PC*4))
    print("Registers: ")
    print("   $1 = " + str(Reg[1]))
    print("   $2 = " + str(Reg[2]))
    print("   $3 = " + str(Reg[3]))
    print("   $4 = " + str(Reg[4]))
    print("   $5 = " + str(Reg[5]))
    print("   $6 = " + str(Reg[6]))
    print("   $7 = " + str(Reg[7]))
    
def main():
    i_memfile = open("i_mem.txt", "r")
    HexInstr = [] #array for instructions in hex
    BinInstr = [] #array for instructions in binary
    Part2 = True if int(input("1 = Part 1\n2 = Part 1&2\n>>")) == 2 else False
    for l in i_memfile: #reading each line in txt file
        if (l == "\n" or l[0] == '#'): #skips over empty lines and comments
            continue
        l = l.replace('\n','')
        HexInstr.append(l)
        l = format(int(l,16),"032b")
        BinInstr.append(l)

    MIPSsim(HexInstr, BinInstr, Part2) #MIPSsim function

if __name__ == "__main__": #NOT SURE HOW THIS WORKS BUT HERE IN CASE
    main()
