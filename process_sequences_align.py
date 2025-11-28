#!/usr/bin/env python3
"""
序列处理自动化脚本
自动执行MAFFT比对和序列质量过滤
"""

import os
import glob
import subprocess
import sys

def run_command(cmd, description=""):
    """运行命令并检查执行状态"""
    if description:
        print(f"正在执行: {description}")
    
    print(f"命令: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"错误: {description} 执行失败")
        print(f"错误信息: {result.stderr}")
        return False
    
    print(f"完成: {description}")
    return True

def main():
    # 创建clean目录和logs子目录
    clean_dir = "clean"
    logs_dir = os.path.join(clean_dir, "logs")
    os.makedirs(clean_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)
    
    print("开始序列处理流程...")
    
    # 第一步：MAFFT比对
    print("\n步骤1: 执行MAFFT序列比对...")
    fasta_files = glob.glob("*.fasta")
    
    if not fasta_files:
        print("未找到任何.fasta文件！")
        return
    
    for fasta_file in fasta_files:
        print(f"正在处理: {fasta_file}")
        base_name = os.path.splitext(fasta_file)[0]
        output_file = os.path.join(clean_dir, f"{base_name}_mafft.fasta")
        
        cmd = f'mafft --auto --keeplength --add "{fasta_file}" ./index/index.fasta > "{output_file}"'
        
        if not run_command(cmd, f"MAFFT比对 - {fasta_file}"):
            print(f"跳过文件 {fasta_file}")
            continue
    
    # 第二步：质量过滤
    print("\n步骤2: 执行序列质量过滤...")
    
    # 切换到clean目录
    original_dir = os.getcwd()
    os.chdir(clean_dir)
    
    try:
        mafft_files = glob.glob("*_mafft.fasta")
        
        for mafft_file in mafft_files:
            print(f"正在过滤: {mafft_file}")
            # 提取原始文件名（去掉_mafft后缀）
            original_name = mafft_file.replace("_mafft", "")
            
            # 创建日志文件名，保存在logs子目录
            log_name = original_name.replace(".fasta", "_removed.log")
            log_path = os.path.join("logs", log_name)
            
            # 使用绝对路径确保能找到rmxg.py脚本
            rmxg_script = os.path.join(original_dir, "rmxg.py")
            cmd = f'python "{rmxg_script}" "{mafft_file}" "{original_name}" -x 5.0 -g 5.0 --log "{log_path}"'
            
            if run_command(cmd, f"质量过滤 - {mafft_file}"):
                # 删除中间文件（比对结果），只保留最终结果
                os.remove(mafft_file)
                print(f"已删除中间文件: {mafft_file}")
            else:
                print(f"过滤失败: {mafft_file}")
        
        # 回到原始目录
        os.chdir(original_dir)
        
        # 显示最终结果
        print("\n" + "="*50)
        print("处理完成！所有结果保存在以下目录:")
        print(f"  - 过滤后的序列: {clean_dir}/")
        print(f"  - 删除序列日志: {logs_dir}/")
        
        # 显示过滤后的序列文件
        clean_files = glob.glob(os.path.join(clean_dir, "*.fasta"))
        print("\n过滤后的序列文件:")
        for file in clean_files:
            file_size = os.path.getsize(file)
            print(f"  {os.path.basename(file)} ({file_size} bytes)")
            
        # 显示日志文件
        log_files = glob.glob(os.path.join(logs_dir, "*.log"))
        if log_files:
            print("\n删除序列日志文件:")
            for file in log_files:
                file_size = os.path.getsize(file)
                print(f"  {os.path.basename(file)} ({file_size} bytes)")
        else:
            print("\n没有序列被删除，因此没有生成日志文件。")
            
    except Exception as e:
        # 确保回到原始目录，即使出现错误
        os.chdir(original_dir)
        print(f"处理过程中出现错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
