
class LyaInstruction(object):
    _mnemonic = None

    def __init__(self, arg1=None, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2
        self.index = None

    def __str__(self):
        if self._mnemonic is '':
            pass
        elif self.arg1 is None and self.arg2 is None:
            return str(tuple([self._mnemonic]))
        elif self.arg2 is None:
            return str(tuple([self._mnemonic, self.arg1]))
        elif self.arg1 is None:
            # TODO: Error
            raise TypeError()
        else:
            return str(tuple([self._mnemonic, self.arg1, self.arg2]))

    def __repr__(self):
        return str(self)

    @property
    def class_name(self):
        return self.__class__.__name__


class STP(LyaInstruction):
    """
    (’stp’)         # Start Program
                        sp=-1; D[0]=0
    """
    _mnemonic = 'stp'


class LBL(LyaInstruction):
    """
    (’lbl’, i)      # No operation
                        (define the label index i)
    """
    _mnemonic = 'lbl'

    def __init__(self, i):
        super().__init__(i)
        self.i = i


class LDC(LyaInstruction):
    """
    (’ldc’, k)     # Load constant
                      sp=sp+1;  M[sp]=k
    """
    _mnemonic = 'ldc'

    def __init__(self, k):
        super().__init__(k)
        self.k = k


class LDV(LyaInstruction):
    """
    (’ldv’, i, j)  # Load value
                      sp=sp+1;  M[sp]=M[D[i]+j]
    """
    _mnemonic = 'ldv'

    def __init__(self, i, j):
        super().__init__(i, j)
        self.i = i
        self.j = j


class LDR(LyaInstruction):
    """
    (’ldr’, i, j)  # Load reference
                      sp=sp+1;  M[sp]=D[i]+j
    """
    _mnemonic = 'ldr'

    def __init__(self, i, j):
        super().__init__(i, j)
        self.i = i
        self.j = j


class STV(LyaInstruction):
    """
    (’stv’, i, j)  # Store value
                      M[D[i]+j]=M[sp];  sp=sp-1
    """
    _mnemonic = 'stv'

    def __init__(self, i, j):
        super().__init__(i, j)
        self.i = i
        self.j = j


class LRV(LyaInstruction):
    """
    (’lrv’, i, j)  # Load reference value
                      sp=sp+1;  M[sp]=M[M[D[i]+j]]
    """
    _mnemonic = 'lrv'

    def __init__(self, i, j):
        super().__init__(i, j)
        self.i = i
        self.j = j


class SRV(LyaInstruction):
    """
    (’srv’, i, j)  # Store reference value
                      M[M[D[i]+j]]=M[sp];  sp=sp-1
    """
    _mnemonic = 'srv'

    def __init__(self, i, j):
        super().__init__(i, j)
        self.i = i
        self.j = j


class ADD(LyaInstruction):
    """
    (’add’)        # Add
                      M[sp-1]=M[sp-1] + M[sp];  sp=sp-1
    """
    _mnemonic = 'add'


class SUB(LyaInstruction):
    """
    (’sub’)        # Subtract
                      M[sp-1]=M[sp-1] - M[sp];  sp=sp-1
    """
    _mnemonic = 'sub'


class MUL(LyaInstruction):
    """
    (’mul’)        # Multiply
                      M[sp-1]=M[sp-1] * M[sp];  sp=sp-1
    """
    _mnemonic = 'mul'


class DIV(LyaInstruction):
    """
    (’div’)        # Division
                      M[sp-1]=M[sp-1] / M[sp];  sp=sp-1
    """
    _mnemonic = 'div'


class MOD(LyaInstruction):
    """
    (’mod’)        # Modulus
                      M[sp-1]=M[sp-1] % M[sp];  sp=sp-1
    """
    _mnemonic = 'mod'


class NEG(LyaInstruction):
    """
    (’neg’)        # Negate
                      M[sp]= -M[sp]
    """
    _mnemonic = 'neg'


class AND(LyaInstruction):
    """
    (’and’)        # Logical And
                      M[sp-1]=M[sp-1] and M[sp];  sp=sp-1
    """
    _mnemonic = 'and'


class LOR(LyaInstruction):
    """
    (’lor’)        # Logical Or
                      M[sp-1]=M[sp-1] or M[sp];  sp=sp-1
    """
    _mnemonic = 'lor'


class NOT(LyaInstruction):
    """
    (’not’)        # Logical Not
                      M[sp]= not M[sp]
    """
    _mnemonic = 'not'


class LES(LyaInstruction):
    """
    (’les’)        # Less
                      M[sp-1]=M[sp-1] < M[sp];  sp=sp-1
    """
    _mnemonic = 'les'


class LEQ(LyaInstruction):
    """
    (’leq’)        # Less or Equal
                      M[sp-1]=M[sp-1] <= M[sp];  sp=sp-1
    """
    _mnemonic = 'leq'


class GRT(LyaInstruction):
    """
    (’grt’)        # Greater
                      M[sp-1]=M[sp-1] > M[sp];  sp=sp-1
    """
    _mnemonic = 'grt'


class GRE(LyaInstruction):
    """
    (’gre’)        # Greater or Equal
                      M[sp-1]=M[sp-1] >= M[sp];  sp=sp-1
    """
    _mnemonic = 'gre'


class EQU(LyaInstruction):
    """
    (’equ’)        # Equal
                      M[sp-1]=M[sp-1] == M[sp];  sp=sp-1
    """
    _mnemonic = 'equ'


class NEQ(LyaInstruction):
    """
    (’neq’)        # Not Equal
                      M[sp-1]=M[sp-1] != M[sp];  sp=sp-1
    """
    _mnemonic = 'neq'


class JMP(LyaInstruction):
    """
    (’jmp’, p)     # Jump
                      pc=p
    """
    _mnemonic = 'jmp'

    def __init__(self, p):
        super().__init__(p)
        self.p = p


class JOF(LyaInstruction):
    """
    (’jof’, p)     # Jump on False
                      if not M[sp]:
                          pc=p
                      else:
                          pc=pc+1
                      sp=sp-1
    """
    _mnemonic = 'jof'

    def __init__(self, p):
        super().__init__(p)
        self.p = p


class ALC(LyaInstruction):
    """
    (’alc’, n)     # Allocate memory
                      sp=sp+n
    """
    _mnemonic = 'alc'

    def __init__(self, n):
        super().__init__(n)
        self.n = n


class DLC(LyaInstruction):
    """
    (’dlc’, n)     # Deallocate memory
                      sp=sp-n
    """
    _mnemonic = 'dlc'

    def __init__(self, n):
        super().__init__(n)
        self.n = n


class CFU(LyaInstruction):
    """
    (’cfu’, p)     # Call Function
                      sp=sp+1; M[sp]=pc+1; pc=p
    """
    _mnemonic = 'cfu'

    def __init__(self, p):
        super().__init__(p)
        self.p = p


class ENF(LyaInstruction):
    """
    (’enf’, k)     # Enter Function
                      sp=sp+1; M[sp]=D[k]; D[k]=sp+1
    """
    _mnemonic = 'enf'

    def __init__(self, k):
        super().__init__(k)
        self.k = k


class RET(LyaInstruction):
    """
    (’ret’, k, n)  # Return from Function
                      D[k]=M[sp]; pc=M[sp-1]; sp=sp-(n+2)
    """
    _mnemonic = 'ret'

    def __init__(self, k, n):
        super().__init__(k, n)
        self.k = k
        self.n = n


class IDX(LyaInstruction):
    """
    (’idx’, k)     # Index
                      M[sp-1]=M[sp-1] + M[sp] * k
                      sp=sp-1
    """
    _mnemonic = 'idx'

    def __init__(self, k):
        super().__init__(k)
        self.k = k


class GRC(LyaInstruction):
    """
    (’grc’)        # Get(Load) Reference Contents
                      M[sp]=M[M[sp]]
    """
    _mnemonic = 'grc'


class LMV(LyaInstruction):
    """
    (’lmv’, k)     # Load multiple values
                      t=M[sp]
                      for i in range(0,k-1):
                          M[sp+i]=M[t+i]
                      sp=sp + k - 1
    """
    _mnemonic = 'lmv'

    def __init__(self, k):
        super().__init__(k)
        self.k = k


class SMV(LyaInstruction):
    """
    (’smv’, k)     # Store multiple Values
                        t = M[sp-k]
                        M[t:t+k] =M[sp-k+1:sp+1]
                        sp -= (k+1)
    """
    _mnemonic = 'smv'

    def __init__(self, k):
        super().__init__(k)
        self.k = k


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
    _mnemonic = 'sts'

    def __init__(self, k):
        super().__init__(k)
        self.k = k


class RDV(LyaInstruction):
    """
    (’rdv’)        # Read single Value
                       sp=sp+1;  M[sp]=input()
    """
    _mnemonic = 'rdv'


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
    _mnemonic = 'rds'


class PRV(LyaInstruction):
    """
    (’prv’)         # Print Value
                        print(M[sp]); sp=sp-1
    """
    _mnemonic = 'prv'


class PRC(LyaInstruction):
    """
    (’prc’, i)      # Print String constant
                        print(H(i),end="")
    """
    _mnemonic = 'prc'

    def __init__(self, i):
        super().__init__(i)
        self.i = i


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
    _mnemonic = 'prs'


class PRT(LyaInstruction):
    """
    ('prt', k)      # Print Multiple Values
                        print(M[sp-k+1:sp+1]); sp-=(k-1)
    """
    _mnemonic = 'prt'

    def __init__(self, k):
        super().__init__(k)
        self.k = k


class END(LyaInstruction):
    """
    (’end’)         # Stop execution
    """
    _mnemonic = 'end'


class NOP(LyaInstruction):
    """
    # Does nothing
    """
    _mnemonic = ''
