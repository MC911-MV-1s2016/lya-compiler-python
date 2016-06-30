# ------------------------------------------------------------
# MC911 - Compiler construction laboratory.
# IC - UNICAMP
#
# RA094139 - Marcelo Mingatos de Toledo
# RA093175 - Victor Fernando Pompeo Barbosa
#
# lya_virtualmachine.py
# Lya Virtual Machine that executes LyaInstructions.
#
# ------------------------------------------------------------

from typing import List

from .lya_lvminstruction import *
from .lya_errors import *


class LyaVirtualMachine(object):
    """The Lya VirtualMachine class.

    Based on the Visitor design pattern, the LVM executes instructions
    from the Lya scripting language (program).

    The instructions should be groups in a ordered list where the first instruction
    signalizes the start of the program (STP). Any string constants should also be
    passed to the machine in a list. The execution is controlled by a set of pointers,
    stacks and heaps.

    Instance variables:
        :ivar pc: int The program counter. Points at the next instruction to be executed.
        :ivar program: List[LyaInstruction] The Program Stack P.
        :ivar bp: int The base register.
        :ivar display: list The Display Stack D.
        :ivar sp: int The stack pointer.
        :ivar memory: list The Memory Stack M
        :ivar string_heap: list[str] The String Constants Heap.

    The program terminates when a END instruction is executed.

    The complete specifications of the virtual machine can be found at
    https://iviarcio.wordpress.com/semantic-code-gen-part-2/.
    """
    def __init__(self):
        self.pc = 0
        self.program = []
        self.program_size = 0
        self.bp = 0
        self.display = [None] * 10000     # TODO: Make it dynamic.
        self.sp = 0
        self.memory = [None] * 10000
        self.string_heap = []
        self.label_pc_map = {}

    @property
    def current_instruction(self) -> LyaInstruction:
        if self.pc < self.program_size:
            return self.program[self.pc]

    def execute(self, instructions: List['LyaInstruction'],
                labels_map: dict,
                string_constants: List[str]):
        self.program = instructions
        self.program_size = len(instructions)
        self.label_pc_map = labels_map
        self.string_heap = string_constants
        while not isinstance(self.current_instruction, END):

            try:
                next_pc = self._execute_current_instruction()
            except LyaError as err:
                print(err)
                exit()

            if next_pc is None:
                self.pc += 1
            else:
                self.pc = next_pc
        pass

    def _execute_current_instruction(self) -> int:
        if self.current_instruction is not None:
            exec_method = 'execute_' + self.current_instruction.class_name
            exec = getattr(self, exec_method, None)
            if exec is not None:
                return exec(self.current_instruction)
            else:
                raise LyaLVMError(self.pc, self.current_instruction, "Missing execution method.")
        else:
            raise LyaLVMError(self.pc, None, "Program counter {0} "
                                             "out or range ({1}).".format(self.pc, self.program_size))

    # Lya Instructions execution visitation methods.

    def execute_STP(self, stp: STP):
        """
        (’stp’)         # Start Program
                            sp=-1; D[0]=0
        """
        self.sp = -1
        self.display[0] = 0

    def execute_LBL(self, lbl: LBL):
        """
        (’lbl’, i)      # No operation
                            (define the label index i)
        """
        # self.label_pc_map[lbl.i] = self.pc
        pass

    def execute_LDC(self, ldc: LDC):
        """
        (’ldc’, k)     # Load constant
                          sp=sp+1;  M[sp]=k
        """
        self.sp += 1
        self.memory[self.sp] = ldc.k

    def execute_LDV(self, ldv: LDV):
        """
        (’ldv’, i, j)  # Load value
                          sp=sp+1;  M[sp]=M[D[i]+j]
        """
        self.sp += 1
        self.memory[self.sp] = self.memory[self.display[ldv.i] + ldv.j]

    def execute_LDR(self, ldr: LDR):
        """
        (’ldr’, i, j)  # Load reference
                          sp=sp+1;  M[sp]=D[i]+j
        """
        self.sp += 1
        self.memory[self.sp] = self.display[ldr.i] + ldr.j

    def execute_STV(self, stv: STV):
        """
        (’stv’, i, j)  # Store value
                          M[D[i]+j]=M[sp];  sp=sp-1
        """
        self.memory[self.display[stv.i] + stv.j] = self.memory[self.sp]
        self.sp -= 1

    def execute_LRV(self, lrv: LRV):
        """
        (’lrv’, i, j)  # Load reference value
                          sp=sp+1;  M[sp]=M[M[D[i]+j]]
        """
        self.sp += 1
        self.memory[self.sp] = self.memory[self.memory[self.display[lrv.i] + lrv.j]]

    def execute_SRV(self, srv: SRV):
        """
        (’srv’, i, j)  # Store reference value
                          M[M[D[i]+j]]=M[sp];  sp=sp-1
        """
        self.memory[self.memory[self.display[srv.i] + srv.j]] = self.memory[self.sp]
        self.sp -= 1

    def execute_ADD(self, add: ADD):
        """
        (’add’)        # Add
                          M[sp-1]=M[sp-1] + M[sp];  sp=sp-1
        """
        self.memory[self.sp - 1] += self.memory[self.sp]
        self.sp -= 1

    def execute_SUB(self, sub: SUB):
        """
        (’sub’)        # Subtract
                          M[sp-1]=M[sp-1] - M[sp];  sp=sp-1
        """
        self.memory[self.sp - 1] -= self.memory[self.sp]
        self.sp -= 1

    def execute_MUL(self, mul: MUL):
        """
        (’mul’)        # Multiply
                          M[sp-1]=M[sp-1] * M[sp];  sp=sp-1
        """
        self.memory[self.sp - 1] *= self.memory[self.sp]
        self.sp -= 1

    def execute_DIV(self, div: DIV):
        """
        (’div’)        # Division
                          M[sp-1]=M[sp-1] / M[sp];  sp=sp-1
        """
        self.memory[self.sp - 1] //= int(self.memory[self.sp])
        self.sp -= 1

    def execute_MOD(self, mod: MOD):
        """
        (’mod’)        # Modulus
                          M[sp-1]=M[sp-1] % M[sp];  sp=sp-1
        """
        self.memory[self.sp - 1] %= self.memory[self.sp]
        self.sp -= 1

    def execute_NEG(self, neg: NEG):
        """
        (’neg’)        # Negate
                          M[sp]= -M[sp]
        """
        self.memory[self.sp] = -self.memory[self.sp]

    def execute_AND(self, and_i: AND):
        """
        (’and’)        # Logical And
                          M[sp-1]=M[sp-1] and M[sp];  sp=sp-1
        """
        self.memory[self.sp - 1] = self.memory[self.sp - 1] and self.memory[self.sp]
        self.sp -= 1

    def execute_LOR(self, lor: LOR):
        """
        (’lor’)        # Logical Or
                          M[sp-1]=M[sp-1] or M[sp];  sp=sp-1
        """
        self.memory[self.sp - 1] = self.memory[self.sp - 1] or self.memory[self.sp]
        self.sp -= 1

    def execute_NOT(self, not_i: NOT):
        """
        (’not’)        # Logical Not
                          M[sp]= not M[sp]
        """
        self.memory[self.sp] = not self.memory[self.sp]

    def execute_LES(self, les: LES):
        """
        (’les’)        # Less
                          M[sp-1]=M[sp-1] < M[sp];  sp=sp-1
        """
        self.memory[self.sp - 1] = self.memory[self.sp - 1] < self.memory[self.sp]
        self.sp -= 1

    def execute_LEQ(self, leq: LEQ):
        """
        (’leq’)        # Less or Equal
                          M[sp-1]=M[sp-1] <= M[sp];  sp=sp-1
        """
        self.memory[self.sp - 1] = self.memory[self.sp - 1] <= self.memory[self.sp]
        self.sp -= 1

    def execute_GRT(self, grt: GRT):
        """
        (’grt’)        # Greater
                          M[sp-1]=M[sp-1] > M[sp];  sp=sp-1
        """
        self.memory[self.sp - 1] = self.memory[self.sp - 1] > self.memory[self.sp]
        self.sp -= 1

    def execute_GRE(self, gre: GRE):
        """
        (’gre’)        # Greater or Equal
                          M[sp-1]=M[sp-1] >= M[sp];  sp=sp-1
        """
        self.memory[self.sp - 1] = self.memory[self.sp - 1] >= self.memory[self.sp]
        self.sp -= 1

    def execute_EQU(self, equ: EQU):
        """
        (’equ’)        # Equal
                          M[sp-1]=M[sp-1] == M[sp];  sp=sp-1
        """
        self.memory[self.sp - 1] = self.memory[self.sp - 1] == self.memory[self.sp]
        self.sp -= 1

    def execute_NEQ(self, neq: NEQ):
        """
        (’neq’)        # Not Equal
                          M[sp-1]=M[sp-1] != M[sp];  sp=sp-1
        """
        self.memory[self.sp - 1] = self.memory[self.sp - 1] != self.memory[self.sp]
        self.sp -= 1

    def execute_JMP(self, jmp: JMP):
        """
        (’jmp’, p)     # Jump
                          pc=p
        """
        return self.label_pc_map[jmp.p]

    def execute_JOF(self, jof: JOF):
        """
        (’jof’, p)     # Jump on False
                          if not M[sp]:
                              pc=p
                          else:
                              pc=pc+1
                          sp=sp-1
        """
        sp = self.sp
        self.sp -= 1
        if not self.memory[sp]:
            return self.label_pc_map[jof.p]

    def execute_ALC(self, alc: ALC):
        """
        (’alc’, n)     # Allocate memory
                          sp=sp+n
        """
        # self.memory.extend([None] * alc.n)
        self.sp += alc.n

    def execute_DLC(self, dlc: DLC):
        """
        (’dlc’, n)     # Deallocate memory
                          sp=sp-n
        """
        self.sp -= dlc.n

    def execute_CFU(self, cfu: CFU):
        """
        (’cfu’, p)     # Call Function
                          sp=sp+1; M[sp]=pc+1; pc=p
        """
        self.sp += 1
        self.memory[self.sp] = self.pc + 1
        return self.label_pc_map[cfu.p]

    def execute_ENF(self, enf: ENF):
        """
        (’enf’, k)     # Enter Function
                          sp=sp+1; M[sp]=D[k]; D[k]=sp+1
        """
        self.sp += 1
        self.memory[self.sp] = self.display[enf.k]
        self.display[enf.k] = self.sp + 1

    def execute_RET(self, ret: RET):
        """
        (’ret’, k, n)  # Return from Function
                          D[k]=M[sp]; pc=M[sp-1]; sp=sp-(n+2)
        """
        self.display[ret.k] = self.memory[self.sp]
        pc = self.memory[self.sp - 1]
        self.sp -= ret.n + 2
        return pc

    def execute_IDX(self, idx: IDX):
        """
        (’idx’, k)     # Index
                          M[sp-1]=M[sp-1] + M[sp] * k
                          sp=sp-1
        """
        self.memory[self.sp - 1] += self.memory[self.sp] * idx.k
        self.sp -= 1

    def execute_GRC(self, grc: GRC):
        """
        (’grc’)        # Get(Load) Reference Contents
                          M[sp]=M[M[sp]]
        """
        self.memory[self.sp] = self.memory[self.memory[self.sp]]

    def execute_LMV(self, lmv: LMV):
        """
        (’lmv’, k)     # Load multiple values
                          t=M[sp]
                          for i in range(0,k-1):
                              M[sp+i]=M[t+i]
                          sp=sp + k - 1
        """
        pass

    def execute_SMV(self, smv: SMV):
        """
        (’smv’, k)     # Store multiple Values
                        t = M[sp-k]
                        M[t:t+k] =M[sp-k+1:sp+1]
                        sp -= (k+1)
        """
        t = self.memory[self.sp - smv.k]
        self.memory[t:t+smv.k] = self.memory[self.sp-smv.k+1:self.sp+1]
        self.sp = self.sp - smv.k - 1
        # for i in range(0, smv.k):
        #     self.memory[self.memory[self.sp - smv.k] + i] = self.memory[self.sp - smv.k + i + 1]
        # self.sp -= smv.k + 1

    def execute_STS(self, sts: STS):
        """
        (’sts’, k)     # Store string constant on reference
                           adr=M[sp]
                           M[adr]=len(H[k])
                           for c in H[k]:
                               adr=adr+1
                               M[adr]=c;
                           sp=sp-1
        """
        adr = self.memory[self.sp]
        self.memory[adr] = len(self.string_heap[sts.k])
        for c in self.string_heap[sts.k]:
            adr += 1
            self.memory[adr] = c
        self.sp -= 1

    @staticmethod
    def check_int(s):
        if len(s) == 0:
            return False
        if s[0] in ('-', '+'):
            return s[1:].isdigit()
        return s.isdigit()

    def execute_RDV(self, rdv: RDV):
        """
        (’rdv’)        # Read single Value
                           sp=sp+1;  M[sp]=input()
        """
        self.sp += 1
        single_value = input()
        if single_value == "true":
            single_value = True
        elif single_value == "false":
            single_value = False
        elif self.check_int(single_value):
            single_value = int(single_value)
        elif len(single_value) != 1:
            raise LyaLVMError(self.pc, rdv, "Invalid single value input '{0}'.".format(single_value))
        self.memory[self.sp] = single_value

    def execute_RDS(self, rds: RDS):
        """
        (’rds’)        # Read String and store it on stack reference
                           str=input()
                           adr=M[sp]
                           M[adr] = len(str)
                           for k in str:
                               adr=adr+1
                               M[adr]=k
                           sp=sp-1
        """
        string = input()
        adr = self.memory[self.sp]
        self.memory[adr] = len(string)
        for k in string:
            adr += 1
            self.memory[adr] = k
        self.sp -= 1

    def execute_PRV(self, prv: PRV):
        """
        (’prv’)         # Print Value
                            print(M[sp]); sp=sp-1
        """
        print(self.memory[self.sp])
        self.sp -= 1

    def execute_PRC(self, prc: PRC):
        """
        (’prc’, i)      # Print String constant
                            print(H(i),end="")
        """
        print(self.string_heap[prc.i], end="")

    def execute_PRS(self, prs: PRS):
        """
        (’prs’)         # Print contents of a string location
                            adr = M[sp]
                            len = M[adr]
                            for i in range(0,len):
                               adr = adr + 1
                               print(M(adr),end="")
                            sp=sp-1
        """
        adr = self.memory[self.sp]
        length = self.memory[adr]
        for i in range(0, length):
            adr += 1
            print(self.memory(adr), end="")
        self.sp -= 1

    def execute_PRT(self, prt: PRT):
        """
        ('prt', k)      # Print Multiple Values
                            print(M[sp-k+1:sp+1]); sp-=(k-1)
        """
        print(self.memory[self.sp-prt.k+1:self.sp+1])
        self.sp -= (prt.k-1)

    def execute_END(self, end: END):
        """
        (’end’)         # Stop execution
        """
        pass

    def execute_NOP(self, nop: NOP):
        """
        # Does nothing
        """
        pass
