import numpy as np
import pandas as pd
import cooler
import sys

if __name__=="__main__":
    coolerFile=sys.argv[1]
    fireFolder=sys.argv[2]
    c=cooler.Cooler(f'{coolerFile}::resolutions/5000')

    for chrom in c.chromnames: 
        arr=c.matrix(balance=False).fetch(chrom)
        np.savetxt(f'{fireFolder}/rawMatrix_{chrom}', arr)
