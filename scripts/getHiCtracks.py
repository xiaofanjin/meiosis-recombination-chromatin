import pandas as pd
import numpy as np
import cooltools.eigdecomp
import cooltools.insulation
import cooltools.coverage
import cooler
import os

def main(coolerFile, bedNamePrefix, chunkBinBed):

    if not os.path.exists(os.path.dirname(bedNamePrefix)):
        os.mkdir(os.path.dirname(bedNamePrefix))

    try:
        clr=cooler.Cooler(coolerFile)
    except:
        clr=cooler.Cooler(f'{coolerFile}::resolutions/5000')

    makeCoverageBeds(clr, bedNamePrefix)
    makeInsulationBeds(clr, bedNamePrefix)
    makeChunkEigenvectorBeds(clr, bedNamePrefix, chunkBinBed)

def getEigChunk(clr,chrom,start,end):
    eigDf=cooltools.eigdecomp.cooler_cis_eig(clr, clr.bins()[:], regions=[(chrom,start,end)],n_eigs=1, phasing_track_col='GC', sort_metric='pearsonr')[1]
    eigDf=eigDf.loc[(eigDf.chrom==chrom)&(eigDf.start>=start)&(eigDf.end<=end),:]
    return eigDf

def getChunkEig(clr,chunkDf):
    eigDf=pd.DataFrame([])
    for row in chunkDf.index:
        chrom=chunkDf.iloc[row,0]
        start=chunkDf.iloc[row,1]
        end=chunkDf.iloc[row,2]
        try:
            eigDf=pd.concat([eigDf, getEigChunk(clr=clr,chrom=chrom,start=start,end=end)])
        except:
            pass
    return eigDf

def makeChunkEigenvectorBeds(clr, bedNamePrefix, chunkBinBed): #implement fine grain eigenvectors compartment scores (as per Wang et al 2019)    
    binsDf10Mb=pd.read_csv(chunkBinBed, delim_whitespace=True, header=None, names=['chrom','start','end']) #chunkBinBed file can be made using cooler makebins, using binsize of 10000000

    df=getChunkEig(clr,binsDf10Mb)
    df.to_csv(f'{bedNamePrefix}_E1chunks.bg', header=False, index=False, sep="\t", columns=['chrom','start','end','E1'])

def makeEigenvectorBeds(clr, bedNamePrefix): #implement traditional eigenvector compartment scores
    df=cooltools.eigdecomp.cooler_cis_eig(clr, clr.bins()[:], phasing_track_col='GC')[1]

    df.to_csv(f'{bedNamePrefix}_E1.bg', header=False, index=False, columns=['chrom','start','end','E1'], sep='\t')

def makeInsulationBeds(clr, bedNamePrefix):
    import cooltools.insulation
    
    windowSize=10*clr.binsize
    
    df=cooltools.insulation.find_boundaries(cooltools.insulation.calculate_insulation_score(clr, window_bp=[windowSize]))
    df.rename(columns={f'log2_insulation_score_{windowSize}': 'logInsScore', f'boundary_strength_{windowSize}': 'boundaryStrength'}, inplace=True)

    df.to_csv(f'{bedNamePrefix}_logInsScore.bg', header=False, index=False, columns=['chrom','start','end','logInsScore'], sep='\t')

def makeCoverageBeds(clr, bedNamePrefix):
    import cooltools.coverage

    cisTotal=cooltools.coverage.get_coverage(clr)
    cisTotal[cisTotal==0]=np.nan

    df=clr.bins()[:]
    df['cisCov']=np.transpose(cisTotal[0,:])
    df['totalCov']=np.transpose(cisTotal[1,:])
    df['cisTotalRatio']=df.cisCov/df.totalCov
  
    for headerString in df.columns[-3:]:
        df.to_csv(f'{bedNamePrefix}_{headerString}.bg', header=False, index=False, columns=['chrom','start','end',headerString], sep='\t')

if __name__=='__main__':
    import sys
#    example arguments: python makeCoolerBeds.py /path/to/data/hic_dataset.mcool::resolutions/5000 /path/to/outputs/hic_dataset /path/to/data/mm10_10Mb_bins.bed
#    mm10_10Mb_bins.bed would be a bed file with 10000000 fixed size bins, which is recommended bin size for 'fine grain eigenvector' analysis (Wang et al 2019)
    assert(len(sys.argv)==4), 'needs 3 arguments, usage: python makeCoolerBeds.py /path/to/coolerURIstring /path/to/outputBedPrefix /path/to/fineGrainEigenvectorBinBed'
    main(*sys.argv[1:])
