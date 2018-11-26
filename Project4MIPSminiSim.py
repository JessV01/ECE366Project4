# ECE 366 Project 4
# Created by: Jessica Vargas, Vaishnavi Medikundam
# The program takes in MIPS instruction memory in hex and returns data

def MIPSsim(HexInstr, BinInstr, Part2, Multi, Pipe):
   
    size_of_mem = 1024                      # NOT SURE IF FOR SURE CORRECT
    print("-------------------------\nBeginning MIPS simulation...\n-------------------------")
    
    Reg = [0,0,0,0,0,0,0,0]                # the $0-$7 registers initialized to 0
    Mem = [0 for i in range(size_of_mem)]   # creates memory array initialized to 0's
    PC = 0
    DIC = 0
    multi_cycles = 0 # total number of cycles for multicycle CPU
    pipe_cycles = 0  # total number of cycles for pipeplined CPU
    threeCyc = 0    # number of instructions that take...3 cycles   
    fourCyc = 0     # number of instructions that take...4 cycles
    fiveCyc = 0     # number of instructions that take...5 cycles
    hazz = 0             # checks on the number of hazards when goes through
    
    end = False
    while(not(end)):
        DIC += 1
        fetch = BinInstr[PC]
        fetch2 = HexInstr[PC]
        if(fetch[0:32] == '00010000000000001111111111111111'):
            threeCyc += 1
            multi_cycles += 3
            if(PC == 0):
                pipe_cycles += 5
            else:
                pipe_cycles += 1
            if(Part2):
                if (Multi):
                    print("*CYCLE "+str(multi_cycles-2)+"*")
                    print("PC = "+str(PC*4)) 
                    print(str(fetch2[0:16])+" --> beq $0,$0,-1")
                    print("Takes 3 cycles...")
                    print("Deadloop Reached")
                if (Pipe): 
            end = True
            
        elif(fetch[0:6] == '000000'): # R-type instructions
            Rs = int(fetch[6:11],2)
            Rt = int(fetch[11:16],2)
            Rd = int(fetch[16:21],2)
            fourCyc += 1 # all R-type instructions take 4 cycles in multicycle CPU
            multi_cycles += 4
            if(PC == 0):
                pipe_cycles += 5
            else:
                pipe_cycles += 1
            
            if(fetch[26:32] == '100000'): # 'add'
                PC += 1
                Reg[Rd] = Reg[Rs] + Reg[Rt]
                if(Part2):
                    if (Multi):
                        print("*CYCLE "+str(multi_cycles-3)+"*")
                        print("PC = "+str((PC-1)*4)) 
                        print(str(fetch2[0:16])+" --> add $"+str(Rd)+",$"+str(Rs)+",$"+str(Rt))
                        print("Takes 4 cycles...\n")
                    if (Pipe): 
                        
            elif(fetch[26:32] == '100010'): # 'sub'
                PC += 1
                Reg[Rd] = Reg[Rs] - Reg[Rt]
                if(Part2):
                    if (Multi): 
                        print("*CYCLE "+str(multi_cycles-3)+"*")
                        print("PC = "+str((PC-1)*4)) 
                        print(str(fetch2[0:16])+" --> sub $"+str(Rd)+",$"+str(Rs)+",$"+str(Rt))
                        print("Takes 4 cycles...\n")
                    if (Pipe):
                        
            elif(fetch[26:32] == '100110'): # 'xor'
                PC += 1
                Reg[Rd] = Reg[Rs] ^ Reg[Rt]
                if(Part2):
                    if (Multi): 
                        print("*CYCLE "+str(multi_cycles-3)+"*")
                        print("PC = "+str((PC-1)*4)) 
                        print(str(fetch2[0:16])+" --> xor $"+str(Rd)+",$"+str(Rs)+",$"+str(Rt))
                        print("Takes 4 cycles...\n")
                    if (Pipe): 
                        
            elif(fetch[26:32] == '101010'): # 'slt'
                PC += 1
                if(Reg[Rs] < Reg[Rt]):
                    Reg[Rd] = 1
                else:
                    Reg[Rd] = 0
                if(Part2):
                    if (Multi): 
                        print("*CYCLE "+str(multi_cycles-3)+"*")
                        print("PC = "+str((PC-1)*4)) 
                        print(str(fetch2[0:16])+" --> slt $"+str(Rd)+",$"+str(Rs)+",$"+str(Rt))
                        print("Takes 4 cycles...\n")
                    if (Pipe): 
                        
            else:
                end = True
                
        else:   #I-type instructions
            Rs = int(fetch[6:11],2)
            Rt = int(fetch[11:16],2)
            if(fetch[16] == '0'):
                Imm = int(fetch[16:32],2)
            else:
                Imm = -(65535 -int(fetch[16:32],2)+1)
            if(PC == 0):
                pipe_cycles += 5
            else:
                pipe_cycles += 1

            if(fetch[0:6] == '001000'): # 'addi'
                fourCyc += 1
                multi_cycles += 4
                PC += 1
                Reg[Rt] = Reg[Rs] + Imm
                if(Part2):
                    if (Multi): 
                        print("*CYCLE "+str(multi_cycles-3)+"*")
                        print("PC = "+str((PC-1)*4)) 
                        print(str(fetch2[0:16])+" --> addi $"+str(Rt)+",$"+str(Rs)+","+str(Imm))
                        print("Takes 4 cycles...\n")
                    if (Pipe): 

            elif(fetch[0:6] == '000100'): # 'beq'
                threeCyc += 1
                multi_cycles += 3
                get = BinInstr[PC-1]
                if(get[0:6] == '000000'): #checking for stall
                    prev_Rd = int(get[16:21],2)
                    if((prev_Rd == Rs) | (prev_Rd == Rt)):
                        pipe_cycles += 1
                        hazz +=1
                if(Reg[Rs] == Reg[Rt]):
                    PC = PC + Imm + 1
                    pipe_cycles += 1 #branch flush
                    hazz += 1
                    
                else:
                    PC += 1
                if(Part2):
                    if (Multi): 
                        print("*CYCLE "+str(multi_cycles-2)+"*")
                        print("PC = "+str((PC-1)*4)) 
                        print(str(fetch2[0:16])+" --> beq $"+str(Rs)+",$"+str(Rt)+","+str(Imm))
                        print("Takes 3 cycles...\n")
                    if (Pipe): 
                        
            elif(fetch[0:6] == '000101'): # 'bne'
                threeCyc += 1
                multi_cycles += 3
                get = BinInstr[PC-1]
                if(get[0:6] == '000000'): #checking for stall
                    prev_Rd = int(get[16:21],2)
                    if((prev_Rd == Rs) | (prev_Rd == Rt)):
                        pipe_cycles += 1
                        hazz +=1
                if(Reg[Rs] != Reg[Rt]):
                    PC = PC + Imm + 1 
                    pipe_cycles += 1 #branch flush
                    hazz += 1
                else:
                    PC += 1
                if(Part2):
                    if (Multi): 
                        print("*CYCLE "+str(multi_cycles-2)+"*")
                        print("PC = "+str((PC-1)*4)) 
                        print(str(fetch2[0:16])+" --> bne $"+str(Rs)+",$"+str(Rt)+","+str(Imm))
                        print("Takes 3 cycles...\n")
                    if (Pipe): 
                        
            elif(fetch[0:6] == '100011'): # 'lw'
                fiveCyc += 1
                multi_cycles += 5
                PC += 1
                Reg[Rt] = Mem[((Reg[Rs] + Imm)-8192)]
                get = BinInstr[PC+1]
                if(get[0:6] == '000000'): #checking for stall
                    prev_Rs = int(get[6:11],2)
                    prev_Rt = int(get[11:16],2)
                    if((prev_Rs == Rs) | (prev_Rs == Rt) | (prev_Rt == Rs) | (prev_Rt == Rt)):
                        pipe_cycles += 1
                        hazz += 1
                else:
                    prev_Rt = int(get[11:16],2)
                    if((prev_Rt == Rs) | (prev_Rt == Rt)):
                        pipe_cycles += 1
                if(Part2):
                    if (Multi):
                        print("*CYCLE "+str(multi_cycles-4)+"*")
                        print("PC = "+str((PC-1)*4)) 
                        print(str(fetch2[0:16])+" --> lw $"+str(Rt)+","+str(Imm)+"($"+str(Rs)+")")
                        print("Takes 5 cycles...\n")
                    if (Pipe): 
                        
            elif(fetch[0:6] == '101011'): # 'sw'
                fourCyc += 1
                multi_cycles += 4
                PC += 1
                Mem[((Reg[Rs] + Imm)-8192)] = Reg[Rt]
                if(Part2):
                    if (Multi): 
                        print("*CYCLE "+str(multi_cycles-3)+"*")
                        print("PC = "+str((PC-1)*4)) 
                        print(str(fetch2[0:16])+" --> sw $"+str(Rt)+","+str(Imm)+"($"+str(Rs)+")")
                        print("Takes 4 cycles...\n")
                    if (Pipe):
                        
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
    if(Part2):
        print("For Multicycle CPU:")
        print("   Total Cycle Count = "+str(multi_cycles))
        print("   Number of 3-cycle Instructions: "+str(threeCyc))
        print("   Number of 4-cycle Instructions: "+str(fourCyc))
        print("   Number of 5-cycle Instructions: "+str(fiveCyc))
        print("For Pipelined CPU:")
        print("   Total Cycle Count = "+str(pipe_cycles))
        print("   Breakdown of hazards = "+str(hazz))
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
    Multi = True 
    Pipe = False
    MIPSsim(HexInstr, BinInstr, Part2, Multi, Pipe) #MIPSsim function
    Multi = False
    Pipe = True 

if __name__ == "__main__": #NOT SURE HOW THIS WORKS BUT HERE IN CASE
    main()
