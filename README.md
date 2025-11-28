# process_sequences_align
tube of sequence alignment
current directory/
├── process_sequences.py
├── rmxg.py
├── sample1.fasta
├── sample2.fasta
├── index/
    └── index.fasta

It need an index file in current directory, several sample.fasta files, and importantly, two python files: process_sequences.py + rmxg.py.

command:
>python process_sequences.py


├── process_sequences.py
├── rmxg.py
├── sample1.fasta
├── sample2.fasta
├── index/
│   └── index.fasta
└── clean/
    ├── sample1.fasta
    ├── sample2.fasta
    └── logs/
        ├── sample1_removed.log
        └── sample2_removed.log
