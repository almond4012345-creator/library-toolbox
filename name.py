import pandas as pd
import os

def run_author_code(input_file):
    try:
        download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        output_file = os.path.join(download_path, "著者號結果.xlsx")

        def generate_author_code(full_name):
            if pd.isna(full_name):
                return '?', '?'
            name_str = str(full_name).strip()
            if not name_str or name_str == '?' or name_str.lower() == 'nan':
                return '?', '?'
            parts = name_str.split()
            surname = parts[-1] if parts else '?'
            conversion_table = {
                'aoh': '0', 'bp': '1', 'ck': '2', 'dt': '3', 
                'eijy': '4', 'fuvw': '5', 'go': '6', 
                'lr': '7', 'mn': '8', 'sxz': '9'
            }??
            clean_surname = ''.join(filter(str.isalpha, surname.lower()))
            if not clean_surname:
                return surname, '?'
            first_four = clean_surname[:4]
            result_nums = []
            for char in first_four:
                found = False
                for key, value in conversion_table.items():
                    if char in key:
                        result_nums.append(value)
                        found = True
                        break
                if not found:
                    result_nums.append('?') 
            return surname, ''.join(result_nums)

        df = pd.read_excel(input_file)
        if 'au_nam1' not in df.columns:
            return False, "找不到 au_nam1 欄位"

        df['au_nam1'] = df['au_nam1'].fillna('?')
        results = df['au_nam1'].apply(generate_author_code)
        df['姓氏'] = [r[0] for r in results]
        df['作者號'] = [r[1] for r in results]
        df.to_excel(output_file, index=False)
        return True, output_file
    except Exception as e:
        return False, str(e)
