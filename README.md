Umberjack
------------------------------------
Umberjack is a python pipeline for calculating evolutionary statistics from populations sequenced with shotgun reads.

Next-generation shotgun sequencing can capture variation within a population for large genomic regions at extreme depths.  Although more effective than amplicon sequencing in terms of wet lab costs, shotgun sequencing lacks uniform homology across entire read lengths due to staggered alignment.  Phylogenetic tools are unable to handle the extensive gaps in multiple sequence alignment of shotgun sequences.  Umberjack collects selection profiles and overcomes the challenges of shotgun sequencing by localizing phylogenetic inference.
 
The pipeline constructs overlapping windows of multiple sequence alignment using positions from SAM files of pairwise alignment of the reads against a reference.  Each window feeds into FastTree2 for phylogenetic reconstruction.  The sequences and resulting trees from each window are processed by HyPhy to obtain various evolutionary statistics.


Caveats
=======================================
This code is a work in progress and is not yet production quality.  Please ensure you have backups of your data before you use this code.


Supported Platform Stack
=======================================
* **Sequencing**:  Illumina single-end and paired-end reads
* **OS**:  Linux 64-bit
* **[HyPhy](http://hyphy.org/w/index.php/Main_Page)**:  HYPHYMP v2.2+  (OpenMP HyPhy)
* **[FastTreeMP](http://www.microbesonline.org/fasttree/)**: FastTreeMP v2.1+  (Multithreading via OpenMP)
* **[R](http://www.r-project.org/)**:  R v3.1.2+
* **Python**:  python v2.7.x 64-bit
  * **[mpi4py](http://mpi4py.scipy.org/docs/usrman/index.html)**:  mpi4py v1.3+  (Python MPI support)



Prerequisites
=======================================
* Install 64-bit python v2.7.
* If you want to run the code on multiple nodes concurrently:
  * Install [OpenMP](http://www.open-mpi.org/) implementation of [MPI-2](http://en.wikipedia.org/wiki/Message_Passing_Interface).
  * Install python package [mpi4py](http://mpi4py.scipy.org/docs/usrman/index.html).
* Optional - Install [FastTreeMP](http://www.microbesonline.org/fasttree/FastTreeMP) and [HYPHYMP](https://github.com/veg/hyphy/releases).
  * Linux X64 binaries for FastTreeMP and HYPHYMP are included under /Umberjack/test/simulations/bin.  If you would like to use different versions, you will need to download and install them.
* Optional - Add the parent directories for the FastTreeMP and HYPHYMP executables into your PATH environment variable.
  * By default, Umberjack will look for FastTreeMP and HYPHYMP binaries from the PATH environment variable.  If you do not want to put the bin directories for FastTreeMP or HYPHYMP in your PATH, explicitly specify your desired FastTreeMP and HYPHYMP binaries in the umberjack.py commandline or config file.
* Install [R](http://www.r-project.org/).
* Install [R ggplot2](http://ggplot2.org/) package.

Visualization
=======================================
For each reference, a separate plot is generated displaying evolutionary stats across the reference.  Each plot is saved as a pdf under the output directory specified in the Umberjack configs.

Parallelization
=======================================
If you want to run the code on multiple processors on one node concurrently, ensure the "--mpi" flag is not present in the Umberjack arguments.
Ensure that Umberjack arguments "--threads_per_window" and "--concurrent_windows" are both set to values larger than 1.  
Umberjack will launch up to "--concurrent_windows" separate python processes, each handling a separate window.  
For each window, Umberjack will give up to "--threads_per_window" threads to FastTreeMP or HYPHYMP.  
The maximum number CPUs used at any one time will be "--threads_per_window" x "--concurrent_windows". 

If you want to run Umberjack on multiple nodes concurrently, you will need to launch Umberjack using [mpirun](https://www.open-mpi.org/doc/v1.8/man1/mpirun.1.php).  
Ensure the "--mpi" flag is present in the Umberjack arguments.  

Sample MPI command:

```
mpirun -machinefile my_nodes_config_file python Umberjack.py --sam_filename SAM_FILENAME --ref REF --mpi
```

If you do not have [mpi4py](http://mpi4py.scipy.org/docs/usrman/index.html) installed, then Umberjack will fall back to running multiple processors on one node.  
mpirun will handle launching Umberjack processes concurrently on your desired nodes.  
Each Umberjack process will give up to "--threads_per_window" threads to FastTreeMP or HYPHYMP to handle a window.  
Note that each FastTreeMP and HYPHYMP will only run on one node.    
The maximum number of CPUs used at any one time will be (number of CPUs given to mpirun) * "--threads_per_window".  
If you specify "--concurrent_windows" in the Umberjack arguments with "--mpi", the "--concurrent_windows" argument will be ignored.





Usage
=======================================

* Use a reference fasta where each contig starts at an open reading frame (ORF).
* Align shotgun reads against your reference with your favourite pairwise fast read aligner to produce a SAM  file of alignments.
* Clone the Umberjack github repository.
* Usage:  python umberjack.py \[arguments\]

* Arguments:
```
  -h, --help            usage message
  -f F                  Full filepath to file containing Umberjack arguments.
                        Any whitespace including newlines will be used to
                        delimit each argument.
                        If this is defined, then all other commandline arguments 
                        will be ignored.
  --sam_filename SAM_FILENAME
                        Full filepath to SAM alignment file. Must be queryname
                        sorted and must have header.
  --ref REF             Name of reference contig. Must be one of references in
                        SAM file.
  --out_dir OUT_DIR     Output directory in which the pipeline will write all
                        its results and intermediate files (default: ./)
  --map_qual_cutoff MAP_QUAL_CUTOFF
                        Mapping quality threshold below which alignments are
                        ignored. (default: 20)
  --read_qual_cutoff READ_QUAL_CUTOFF
                        Read quality threshold below which bases are converted
                        to Ns. (default: 20)
  --max_prop_n MAX_PROP_N
                        Maximum fraction of Ns allowed in single-end reads or
                        merged paired reads below which the read is ignored.
                        (default: 0.1)
  --window_size WINDOW_SIZE
                        Window size in nucleotides. (default: 300)
  --window_slide WINDOW_SLIDE
                        Number of bases to slide each window by. (default: 30)
  --window_breadth_cutoff WINDOW_BREADTH_CUTOFF
                        fraction of window that a single-end or merged paired
                        read must cover with non-gap and non-N nucleotides.
                        Below this threshold, the read is omitted from the
                        window. (default: 0.8)
  --window_depth_cutoff WINDOW_DEPTH_CUTOFF
                        Minimum number of reads within a valid window.
                        (default: 50)
  --start_nucpos START_NUCPOS
                        1-based start nucleotide position in the reference
                        contig. The first window will start at this position.
                        Default: 1 (default: 1)
  --end_nucpos END_NUCPOS
                        1-based end nucleotide position in the reference
                        contig. The last window will start at or before this
                        position. If 0, then automatically set to last
                        position in the reference contig. (default: 0)
  --insert              Whether to keep insertions with respect to the
                        reference. (default: False)
  --mask_stop_codon     Whether to mask stop codons with NNN. Automatically
                        set to True when mode is DNDS (default: False)
  --threads_per_window THREADS_PER_WINDOW
                        threads allotted per window. (default: 1)
  --concurrent_windows CONCURRENT_WINDOWS
                        Max number of windows to process concurrently. Ignored
                        when --mpi is defined. (default: 1)
  --output_csv_filename OUTPUT_CSV_FILENAME
                        In DNDS mode, the full filepath of final comma-
                        separated values file containing selection information
                        for each codon site in the reference from averaged
                        over overlapping windows. In GTR_RATE mode, the full
                        filepath of final comma-separated values file
                        containing window-specific general time reversible
                        nucleotide substitution rates. (default:
                        umberjack.out.csv)
  --hyphy_exe HYPHY_EXE
                        full filepath of HYPHYMP executable. Default: taken
                        from PATH (default: HYPHYMP)
  --hyphy_basedir HYPHY_BASEDIR
                        full filepath of HyPhy base directory containing
                        template batch files. (default:
                        /usr/local/lib/hyphy/TemplateBatchFiles/)
  --fastree_exe FASTREE_EXE
                        full filepath of FastTreeMP or FastTree executable.
                        Default: taken from PATH (default: FastTree)
  --mode {DNDS,GTR_RATE}
                        DNDS: Execute dN/dS analysis for positive
                        (diversifying selection in codon alignment. GTR_RATE:
                        Profile nucleotide substitution rate biases under
                        generalized non-reversible (6-parameter) model.
                        (default: DNDS)
  --mpi                 Runs in MPI mode with multiple processes on multiple
                        nodes. If python module mpi4py is not installed, then
                        runs multiple processes on single node. (default:
                        False)
  --debug               Whether to keep all intermediate files, generate full
                        genome multiple sequence alignment, set debug
                        logging.Overrides the logging level configured in
                        logging.conf. (default: False)
                        


```



Logging
=======================================

You may configure logging via the config file in [logging.conf](/config/logging.conf).  
This config file follows typical [python config file syntax](https://docs.python.org/2/library/configparser.html).

If you specify "--debug" in the Umberjack parameters, it will set logging to DEBUG level and override your logging.conf file.

