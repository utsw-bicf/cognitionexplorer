
broad_peaks_targets = [
    'H3K4me1-mouse',
    'H3K36me3-mouse',
    'H3K79me2-mouse',
    'H3K27me3-mouse',
    'H3K9me1-mouse',
    'H3K9me3-mouse',
    'H3K4me1-human',
    'H3K36me3-human',
    'H3K79me2-human',
    'H3K27me3-human',
    'H3K9me1-human',
    'H3K9me3-human',
    'H3F3A-human',
    'H4K20me1-human',
    'H3K79me3-human',
    'H3K79me3-mouse',
    ]

pipelines_with_read_depth = {
    'Small RNA-seq single-end pipeline': 30000000,
    'RNA-seq of long RNAs (paired-end, stranded)': 30000000,
    'RNA-seq of long RNAs (single-end, unstranded)': 30000000,
    'RAMPAGE (paired-end, stranded)': 25000000,
    'Histone ChIP-seq': {
        'narrow': 20000000,
        'broad': 45000000
        }
    }

special_assays_with_read_depth = {
    'shRNA knockdown followed by RNA-seq': 10000000,
    'single cell isolation followed by RNA-seq': 5000000
    }
