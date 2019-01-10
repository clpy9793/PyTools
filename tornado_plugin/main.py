import sys
import pandas as pd


def read_log(path):
    with open(path, 'r') as f:
        for line in f.readlines():
            row = line.split(' ')
            ts = " ".join(row[:2])
            ts = ts.split(',')[0]
            method = row[-3]
            cost = row[-1]
            cost = cost.split('ms')[0]
            yield ts, cost, method


def get_dataframe(path):
    ts_li = []
    cost_li = []
    for ts, cost, _ in read_log(path):
        ts_li.append(ts)
        cost_li.append(cost)
    df = pd.DataFrame({"ts": ts_li, "cost": cost_li})
    return df


def main(path='./webhook.log'):
    df = get_dataframe(path)
    df['ts'] = pd.to_datetime(df['ts'])
    df = df.set_index(['ts'])
    df_T = df.to_period('T')
    gp_T = df_T.groupby(by=lambda x: x)
    print(gp_T.size())


if __name__ == '__main__':
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        sys.exit(110)
    main(path=path)
