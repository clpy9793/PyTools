import sys
import pandas as pd


def run(path):
    data = {}
    with open(path, 'r', encoding='utf8') as f:
        for line in f:
            items = line.split(' ')
            if len(items) != 10:
                continue
            status_code = int(items[5])
            method = items[6]
            uri = items[7].split('?')[0]
            ip_from = items[8]
            cost = float(items[9].replace('ms', '').strip())
            data.setdefault(uri, {'success': [], 'fail': []})
            if 200 <= status_code < 300:
                data[uri]['success'].append(cost)
            else:
                data[uri]['fail'].append(cost)
    df = analysis(data)
    df.to_csv('~/Desktop/api.csv')

def analysis(data):
    resp = {}
    columns = [
        '调用次数', '成功率', '成功次数', '失败次数',
        '最大响应时间', '最小响应时间(ms)', '平均响应时间(ms)',
    ]
    for uri, call_res in data.items():
        # 初始化参数
        success = call_res.get('success')
        fail = call_res.get('fail')
        success_call_num = 0
        success_call_max = 0
        success_call_min = 0
        
        success_call_avg = 0        
        fail_call_num = 0
        fail_call_max = 0
        fail_call_avg = 0
        fail_call_min = 0

        if success:
            success_call_num = len(call_res['success'])
            success_call_max = max(call_res['success'])
            success_call_min = min(call_res['success'])
            success_call_avg = sum(call_res['success']) / success_call_num
            

        if fail:
            fail_call_num = len(call_res['fail'])
            fail_call_max = max(call_res['fail'])
            fail_call_min = min(call_res['fail'])
            fail_call_avg = sum(call_res['fail']) / fail_call_num
            

        call_num = success_call_num + fail_call_num
        success_rate = success_call_num / call_num
        call_max = max(success_call_max, fail_call_max)
        if success_call_max == 0 or fail_call_min == 0:
            call_min = max(success_call_min, fail_call_min)
        else:
            call_min = min(success_call_min, fail_call_min)
        call_avg = sum([sum(call_res['success']), 
                        sum(call_res['fail'])]) / call_num
        resp[uri] = [
            call_num, success_rate, success_call_num, fail_call_num,
            call_max, call_min, call_avg,
        ]
    df = pd.DataFrame.from_dict(resp, orient='index', columns=columns)
    return df

if __name__ == '__main__':
    path = sys.argv[1]
    run(path)

