"""
数据清洗模块
功能：读取CSV文件 → 清洗 → 写入SQLite数据库
"""

import pandas as pd
import sqlite3
import os


def clean_csv_to_sqlite(csv_dir: str, db_path: str):
    """
    读取CSV目录下所有文件，清洗后写入SQLite数据库
    
    Args:
        csv_dir: CSV文件目录
        db_path: 输出数据库路径
    """
    if not os.path.exists(csv_dir):
        print(f"❌ 目录不存在: {csv_dir}")
        return
    
    conn = sqlite3.connect(db_path)
    csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"❌ 目录下没有CSV文件: {csv_dir}")
        conn.close()
        return
    
    for csv_file in csv_files:
        table_name = os.path.splitext(csv_file)[0]
        file_path = os.path.join(csv_dir, csv_file)
        
        print(f"📄 处理: {csv_file} → 表 {table_name}")
        
        df = pd.read_csv(file_path, encoding='utf-8')
        
        # 基础清洗
        df.columns = [col.strip() for col in df.columns]  # 列名去空格
        df = df.drop_duplicates()  # 去重
        df = df.where(pd.notnull(df), None)  # NaN → None
        
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"  ✅ 写入 {len(df)} 条记录")
    
    conn.close()
    print(f"\n✅ 数据库生成完成: {db_path}")


if __name__ == "__main__":
    clean_csv_to_sqlite(
        csv_dir="../../data/raw",
        db_path="crm_data.db"
    )
