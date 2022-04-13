import numpy as np

#Define function for CX gate (applied when control qudits are simultaneously in 1 state) of arbitrary d, nq.
#d is dimension of qudits, nq is number of qudits, and index is the index of target qudit (default equal to n)
def CX_dn(d, n, index=None):
    #Define relevant gates from parameters
    I_dn=np.eye(d**n)
    I_d=np.eye(d)
    X_d=np.roll(I_d,1,0)
    
    #Create matrix with elements M=delta(1,1) 
    #(starting counting from 0) state for d-dimensional matrix
    d1=[0,1]
    for i in range(d-2):
        d1.append(0)
        d1arr=np.array(d1)
    diag1=np.diag(d1arr)    
    
    #Out of range
    if index > n or index <= 0:
        print("Index of target qudit out of range of n!")
        
    #Create (default) CX with last (bottom in circuit) qudit as target
    elif index==n or index==None:
        diagph=diag1
        for i in range(n-2):
            diagph=np.kron(diagph,diag1)
        CX_dn=np.kron(diagph,X_d)-np.kron(diagph,I_d)+I_dn
       
    #Create CX with first qudit as target
    elif index ==1:
        diagph=diag1
        diagph=np.kron(X_d,diag1)
        diagph2 = np.kron(I_d,diag1)
        for i in range(n-2):
            diagph=np.kron(diagph,diag1)
            diagph2 = np.kron(diagph2,diag1)
        CX_dn=diagph - diagph2 + I_dn
        
    #Create CX with any other qudit as target 
    else:
        diagph1=diag1
        for i in range(index-(n-1)):
            diagph1=np.kron(diagph,diag1)
        diagph=np.kron(diagph1,X_d)
        diagph2=np.kron(diagph1,I_d)
        for i in range(index-(n-1)+1,n-1):
            diagph=np.kron(diagph,diag1)
            diagph2=np.kron(diagph2,diag1)
        CX_dn=diagph -diagph2 + I_dn
    return CX_dn
