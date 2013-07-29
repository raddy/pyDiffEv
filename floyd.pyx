import numpy as np
cimport numpy as np

cdef extern from "floyd.h" nogil:
    cdef int* unique_indices(int,int)
def unique_dexes(num,list_len):
    cdef int [:] dexes = <int[:num]>unique_indices(num,list_len)
    return np.array(dexes) #copy is faster? (I don't get why this is true)