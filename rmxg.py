#!/usr/bin/env python3
"""
FASTA序列质量过滤脚本 - 无依赖版本
支持同时过滤X和-字符过多的序列，并记录删除的序列信息
"""

import argparse
import sys

def read_fasta(file_path):
    """读取FASTA文件，返回序列记录列表"""
    sequences = []
    current_header = ""
    current_sequence = ""
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('>'):
                    # 保存前一个序列
                    if current_header and current_sequence:
                        sequences.append((current_header, current_sequence))
                    
                    # 开始新序列
                    current_header = line
                    current_sequence = ""
                else:
                    current_sequence += line
            
            # 保存最后一个序列
            if current_header and current_sequence:
                sequences.append((current_header, current_sequence))
                
    except FileNotFoundError:
        print(f"错误: 找不到文件 {file_path}")
        sys.exit(1)
    
    return sequences

def calculate_issue_percentage(sequence):
    """计算序列中X和-字符的比例"""
    total_length = len(sequence)
    if total_length == 0:
        return 0.0, 0.0
    
    upper_seq = sequence.upper()
    x_count = upper_seq.count('X')
    gap_count = upper_seq.count('-')
    
    x_percentage = (x_count / total_length) * 100
    gap_percentage = (gap_count / total_length) * 100
    
    return x_percentage, gap_percentage

def write_fasta(sequences, output_file):
    """将序列写入FASTA文件"""
    with open(output_file, 'w') as file:
        for header, sequence in sequences:
            file.write(header + '\n')
            # 每行写60个字符，保持标准FASTA格式
            for i in range(0, len(sequence), 60):
                file.write(sequence[i:i+60] + '\n')

def filter_fasta_by_issues(input_file, output_file, x_threshold=5.0, gap_threshold=5.0, log_file=None):
    """
    过滤FASTA文件，去除X或-比例超过阈值的序列
    """
    print(f"正在处理文件: {input_file}")
    print(f"X比例阈值: > {x_threshold}% 的序列将被移除")
    print(f"-比例阈值: > {gap_threshold}% 的序列将被移除")
    
    # 读取序列
    sequences = read_fasta(input_file)
    total_count = len(sequences)
    
    # 过滤序列
    filtered_sequences = []
    removed_count = 0
    
    # 记录删除的序列信息
    removed_sequences_info = []
    
    for header, sequence in sequences:
        x_percentage, gap_percentage = calculate_issue_percentage(sequence)
        
        if x_percentage <= x_threshold and gap_percentage <= gap_threshold:
            filtered_sequences.append((header, sequence))
        else:
            removed_count += 1
            # 从header中提取序列ID（去除'>'符号）
            seq_id = header[1:].split()[0] if header.startswith('>') else header
            removal_info = f"移除序列: {seq_id} (X比例: {x_percentage:.2f}%, -比例: {gap_percentage:.2f}%)"
            print(removal_info)
            removed_sequences_info.append(removal_info)
    
    # 写入过滤后的序列
    if filtered_sequences:
        write_fasta(filtered_sequences, output_file)
        print(f"\n处理完成!")
        print(f"总序列数: {total_count}")
        print(f"保留序列数: {len(filtered_sequences)}")
        print(f"移除序列数: {removed_count}")
        print(f"输出文件: {output_file}")
        
        # 如果指定了日志文件，写入删除的序列信息
        if log_file:
            with open(log_file, 'w') as log:
                log.write(f"# 序列过滤日志 - {input_file}\n")
                log.write(f"# X阈值: {x_threshold}%, -阈值: {gap_threshold}%\n")
                log.write(f"# 总序列数: {total_count}\n")
                log.write(f"# 保留序列数: {len(filtered_sequences)}\n")
                log.write(f"# 移除序列数: {removed_count}\n")
                log.write("# 移除的序列详情:\n")
                for info in removed_sequences_info:
                    log.write(info + '\n')
            print(f"删除序列日志: {log_file}")
    else:
        print("警告: 所有序列都被移除了！请检查阈值设置。")

def main():
    parser = argparse.ArgumentParser(
        description="过滤FASTA文件中含有过多'X'字符或'-'字符的低质量序列",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
使用示例:
  python filter_fasta.py input.fasta output.fasta
  python filter_fasta.py input.fasta output.fasta -x 3.0 -g 10.0
  python filter_fasta.py input.fasta output.fasta --x_threshold 5.0 --gap_threshold 5.0 --log removal.log
        """
    )
    
    parser.add_argument("input_file", help="输入FASTA文件路径")
    parser.add_argument("output_file", help="输出FASTA文件路径")
    parser.add_argument("-x", "--x_threshold", type=float, default=5.0,
                       help="X比例阈值(百分比)，默认5.0")
    parser.add_argument("-g", "--gap_threshold", type=float, default=5.0,
                       help="-比例阈值(百分比)，默认5.0")
    parser.add_argument("--log", type=str, default=None,
                       help="记录删除序列信息的日志文件路径")
    
    args = parser.parse_args()
    
    # 检查阈值是否合理
    if args.x_threshold < 0 or args.x_threshold > 100:
        print("错误: X阈值必须在0-100之间")
        sys.exit(1)
    if args.gap_threshold < 0 or args.gap_threshold > 100:
        print("错误: -阈值必须在0-100之间")
        sys.exit(1)
    
    filter_fasta_by_issues(args.input_file, args.output_file, args.x_threshold, args.gap_threshold, args.log)

if __name__ == "__main__":
    main()
