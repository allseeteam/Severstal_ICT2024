import pandas as pd


def save_excel_report(tables, output_path):
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        for i, df in enumerate(tables):
            sheet_name = f'Лист {i + 1}'
            df.to_excel(writer, sheet_name=sheet_name)
