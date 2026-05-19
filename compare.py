import os
import pandas as pd
from rapidfuzz import process, fuzz

def run_compare(collection_file, isbn_file=None, title_file=None):
    try:
        download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        
        ??df_collection = pd.read_excel(collection_file, header=None)
        collection_titles = df_collection.iloc[:, 0].dropna().astype(str).str.upper()
        collection_isbns = df_collection.iloc[:, 1].dropna().astype(str).str.replace(r'\.0$', '', regex=True).str.upper().str.replace(r'[\s-]', '', regex=True)
        
        report_msg = []

        if isbn_file:
            df_isbn = pd.read_excel(isbn_file, header=None)
            check_isbns = df_isbn.iloc[:, 0].dropna().astype(str).str.replace(r'\.0$', '', regex=True).str.upper().str.replace(r'[\s-]', '', regex=True)
            duplicates = check_isbns[check_isbns.isin(collection_isbns)]
            if not duplicates.empty:
                out_isbn = os.path.join(download_path, "ISBN_比對結果.xlsx")
                pd.DataFrame(duplicates).to_excel(out_isbn, index=False, header=False)
                report_msg.append(f"ISBN重複量: {len(duplicates)}")

        if title_file:
            df_title = pd.read_excel(title_file, header=None)
            check_titles = df_title.iloc[:, 0].dropna().astype(str).str.upper()
            results = []
            collection_titles_list = collection_titles.tolist()
            for title in check_titles:
                match = process.extractOne(title, collection_titles_list, scorer=fuzz.partial_ratio)
                if match:
                    best_match_text, score, _ = match
                    if score >= 60:
                        results.append([title, best_match_text, score])
            if results:
                out_title = os.path.join(download_path, "書名_疑似重複對照表.xlsx")
                pd.DataFrame(results, columns=["預購書名", "圖書館現有書名", "相似度"]).to_excel(out_title, index=False)
                report_msg.append(f"書名疑似重複量: {len(results)}")

        return True, "\n".join(report_msg) if report_msg else "未發現重複"
    except Exception as e:
        return False, str(e)