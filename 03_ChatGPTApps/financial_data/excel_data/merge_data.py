import os
import pandas as pd

# フォルダ内のエクセルファイルを結合する関数
def merge_excel_files(folder_path):
    merged_data = None

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".xlsx"):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_excel(file_path, skiprows=2)  # 3行目以降を読み込み

            if merged_data is None:
                merged_data = df
            else:
                merged_data = pd.merge(
                    merged_data, df, on=["コード", "年度"], how="outer")

    return merged_data

# 使用例
if __name__ == "__main__":
    folder_path = "03_ChatGPTApps/financial_data/excel_data"
    merged_data = merge_excel_files(folder_path)

    output_path = os.path.join(folder_path, "merged_result.xlsx")
    merged_data.to_excel(output_path, index=False)
    print(f"結合したデータを保存しました: {output_path}")
