import sys
import pandas as pd

if __name__ == '__main__':

    path = '123.xlsx' if len(sys.argv) <= 1 else sys.argv[1]
    df = pd.read_excel(path)
    df = df[:1000]
    code_name_map = {}
    name_code_map = {}
    for item in df.itertuples():
        index, code, name = item
        code_name_map.setdefault(code, [])
        name_code_map.setdefault(name, set())
        code_name_map[code].append(name)
        name_code_map[name].add(code)
    indexs = list(name_code_map.keys())
    column_order = indexs
    csv_data = {name: [] for name in indexs}
    for row, row_name in enumerate(indexs):
        print(f'row: {row}')
        for col_name in indexs:
            if row_name == col_name:
                csv_data[col_name].append('')
                continue
            row_code_set = name_code_map[row_name]
            col_code_set = name_code_map[col_name]
            # 判断是否存在联合
            if row_code_set & col_code_set:
                csv_data[col_name].append('1')
            else:
                csv_data[col_name].append('0')

    df = pd.DataFrame(csv_data, index=indexs)
    df.to_csv('martix_A.csv', columns=column_order)




    


