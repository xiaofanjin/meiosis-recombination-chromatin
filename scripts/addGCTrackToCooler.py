import cooltools
import cooler
import bioframe
import h5py
import sys

if __name__=="__main__":
    mcoolFile=sys.argv[1]
    resolution=sys.argv[2]
    fastaFile=sys.argv[3]

    c=cooler.Cooler(mcoolFile+'::resolutions/'+resolution)
    bins=c.bins()[:]
    fasta_records = bioframe.load_fasta(fastaFile)
    bins['GC'] = bioframe.tools.frac_gc(bins, fasta_records)

    coolerHandle=h5py.File(mcoolFile,'r+')
    try:
        del coolerHandle['resolutions/'+resolution+'/bins/GC']
    except:
        pass
    coolerHandle.create_dataset('resolutions/'+resolution+'/bins/GC', data=bins['GC'].values)
    coolerHandle.close()
