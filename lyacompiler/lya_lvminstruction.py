
class LyaInstruction(object):
    _code = None

    def __init__(self, arg1=None, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2

    def __str__(self):
        if self._code is '':
            pass
        elif self.arg1 is None and self.arg2 is None:
            return str(tuple([self._code]))
        elif self.arg2 is None:
            return str(tuple([self._code, self.arg1]))
        elif self.arg1 is None:
            # TODO: Error
            raise TypeError()
        else:
            return str(tuple([self._code, self.arg1, self.arg2]))

    def __repr__(self):
        return str(self)


class STP(LyaInstruction):
    """
    (’stp’)         # Start Program
                        sp=-1; D[0]=0
    """
    _code = 'stp'


class LBL(LyaInstruction):
    """
    (’lbl’, i)      # No operation
                        (define the label index i)
    """
    _code = 'lbl'


class LDC(LyaInstruction):
    """
    (’ldc’, k)     # Load constant
                      sp=sp+1;  M[sp]=k
    """
    _code = 'ldc'


class LDV(LyaInstruction):
    """
    (’ldv’, i, j)  # Load value
                      sp=sp+1;  M[sp]=M[D[i]+j]
    """
    _code = 'ldv'


class LDR(LyaInstruction):
    """
    (’ldr’, i, j)  # Load reference
                      sp=sp+1;  M[sp]=D[i]+j
    """
    _code = 'ldr'


class STV(LyaInstruction):
    """
    (’stv’, i, j)  # Store value
                      M[D[i]+j]=M[sp];  sp=sp-1
    """
    _code = 'stv'

class LRV(LyaInstruction):
    """
    (’lrv’, i, j)  # Load reference value
                      sp=sp+1;  M[sp]=M[M[D[i]+j]]
    """
    _code = 'lrv'


class SRV(LyaInstruction):
    """
    (’srv’, i, j)  # Store reference value
                      M[M[D[i]+j]]=M[sp];  sp=sp-1
    """
    _code = 'srv'


class ADD(LyaInstruction):
    """
    (’add’)        # Add
                      M[sp-1]=M[sp-1] + M[sp];  sp=sp-1
    """
    _code = 'add'


class SUB(LyaInstruction):
    """
    (’sub’)        # Subtract
                      M[sp-1]=M[sp-1] - M[sp];  sp=sp-1
    """
    _code = 'sub'


class MUL(LyaInstruction):
    """
    (’mul’)        # Multiply
                      M[sp-1]=M[sp-1] * M[sp];  sp=sp-1
    """
    _code = 'mul'


class DIV(LyaInstruction):
    """
    (’div’)        # Division
                      M[sp-1]=M[sp-1] / M[sp];  sp=sp-1
    """
    _code = 'div'


class MOD(LyaInstruction):
    """
    (’mod’)        # Modulus
                      M[sp-1]=M[sp-1] % M[sp];  sp=sp-1
    """
    _code = 'mod'


class NEG(LyaInstruction):
    """
    (’neg’)        # Negate
                      M[sp]= -M[sp]
    """
    _code = 'neg'


class AND(LyaInstruction):
    """
    (’and’)        # Logical And
                      M[sp-1]=M[sp-1] and M[sp];  sp=sp-1
    """
    _code = 'and'


class LOR(LyaInstruction):
    """
    (’lor’)        # Logical Or
                      M[sp-1]=M[sp-1] or M[sp];  sp=sp-1
    """
    _code = 'lor'


class NOT(LyaInstruction):
    """
    (’not’)        # Logical Not
                      M[sp]= not M[sp]
    """
    _code = 'not'


class LES(LyaInstruction):
    """
    (’les’)        # Less
                      M[sp-1]=M[sp-1] < M[sp];  sp=sp-1
    """
    _code = 'les'


class LEQ(LyaInstruction):
    """
    (’leq’)        # Less or Equal
                      M[sp-1]=M[sp-1] <= M[sp];  sp=sp-1
    """
    _code = 'leq'


class GRT(LyaInstruction):
    """
    (’grt’)        # Greater
                      M[sp-1]=M[sp-1] > M[sp];  sp=sp-1
    """
    _code = 'grt'


class GRE(LyaInstruction):
    """
    (’gre’)        # Greater or Equal
                      M[sp-1]=M[sp-1] >= M[sp];  sp=sp-1
    """
    _code = 'gre'


class EQU(LyaInstruction):
    """
    (’equ’)        # Equal
                      M[sp-1]=M[sp-1] == M[sp];  sp=sp-1
    """
    _code = 'equ'


class NEQ(LyaInstruction):
    """
    (’neq’)        # Not Equal
                      M[sp-1]=M[sp-1] != M[sp];  sp=sp-1
    """
    _code = 'neq'


class JMP(LyaInstruction):
    """
    (’jmp’, p)     # Jump
                      pc=p
    """
    _code = 'jmp'


class JOF(LyaInstruction):
    """
    (’jof’, p)     # Jump on False
                      if not M[sp]:
                          pc=p
                      else:
                          pc=pc+1
                      sp=sp-1
    """
    _code = 'jof'


class ALC(LyaInstruction):
    """
    (’alc’, n)     # Allocate memory
                      sp=sp+n
    """
    _code = 'alc'


class DLC(LyaInstruction):
    """
    (’dlc’, n)     # Deallocate memory
                      sp=sp-n
    """
    _code = 'dlc'


class CFU(LyaInstruction):
    """
    (’cfu’, p)     # Call Function
                      sp=sp+1; M[sp]=pc+1; pc=p
    """
    _code = 'cfu'


class ENF(LyaInstruction):
    """
    (’enf’, k)     # Enter Function
                      sp=sp+1; M[sp]=D[k]; D[k]=sp+1
    """
    _code = 'enf'


class RET(LyaInstruction):
    """
    (’ret’, k, n)  # Return from Function
                      D[k]=M[sp]; pc=M[sp-1]; sp=sp-(n+2)
    """
    _code = 'ret'


class IDX(LyaInstruction):
    """
    (’idx’, k)     # Index
                      M[sp-1]=M[sp-1] + M[sp] * k
                      sp=sp-1
    """
    _code = 'idx'


class GRC(LyaInstruction):
    """
    (’grc’)        # Get(Load) Reference Contents
                      M[sp]=M[M[sp]]
    """
    _code = 'grc'


class LMV(LyaInstruction):
    """
    (’lmv’, k)     # Load multiple values
                      t=M[sp]
                      for i in range(0,k-1):
                          M[sp+i]=M[t+i]
                      sp=sp + k - 1
    """
    _code = 'lmv'


class SMV(LyaInstruction):
    """
    (’smv’, k)     # Store multiple Values
                       for i in range(0,k-1):
                           M[M[sp-k]+i]=M[sp-k+i+1]
                       sp=sp - k - 1
    """
    _code = 'smv'


class STS(LyaInstruction):
    """
    (’sts’, k)     # Store string constant on reference
                       adr=M[sp]
                       M[adr]=len(H[k])
                       for c in H[k]:
                           adr=adr+1
                           M[adr]=c;
                       sp=sp-1
    """
    _code = 'sts'


class RDV(LyaInstruction):
    """
    (’rdv’)        # Read single Value
                       sp=sp+1;  M[sp]=input()
    """
    _code = 'rdv'


class RDS(LyaInstruction):
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
    _code = 'rds'


class PRV(LyaInstruction):
    """
    (’prv’)         # Print Value
                        print(M[sp]); sp=sp-1
    """
    _code = 'prv'


class PRC(LyaInstruction):
    """
    (’prc’, i)      # Print String constant
                        print(H(i),end="")
    """
    _code = 'prc'


class PRS(LyaInstruction):
    """
    (’prs’)         # Print contents of a string location
                        adr = M[sp]
                        len = M[adr]
                        for i in range(0,len):
                           adr = adr + 1
                           print(M(adr),end="")
                        sp=sp-1
    """
    _code = 'prs'


class PRT(LyaInstruction):
    """
    ('prt', k)      # Print Multiple Values
                        print(M[sp-k+1:sp+1]); sp-=(k-1)
    """
    _code = 'prt'


class END(LyaInstruction):
    """
    (’end’)         # Stop execution
    """
    _code = 'end'


class NOP(LyaInstruction):
    """
    # Does nothing
    """
    _code = ''
