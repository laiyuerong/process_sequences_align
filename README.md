# process_sequences_align
# 处理当前文件夹下所有fasta文件，处理后的fasta文件在./clean文件夹目录下，同时，./clean目录下还有一个./clean/logs文件，用来储存处理日志。
# 需要索引文件在当前文件夹下 ./index/index/fasta

python align.py

# 帮助
python align.py -h


# 修改参数

# 修改阈值，-x 10，去除X占比超过10%的序列；-g 20，去除-占比超过20%的序列  
python auto_process.py -x 10 -g 20
# 指定索引文件位置  
python auto_process.py --index /home/user/data/ref_index.fasta
