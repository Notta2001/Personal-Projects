import pandas as pd
from pytrends.request import TrendReq
pytrend = TrendReq()
key_word = pd.read_csv('keytrends.csv', header=None)
key_word = key_word.fillna(0)
writer = pd.ExcelWriter('vn_trend_2020.xlsx', datetime_format='DD-MM-YYYY')

for i in range(key_word.shape[1]):
    l = []
    n = 0
    for j in range(1, key_word.shape[0]):
        if key_word[i][j] == 0:
            break
        else :
            n += 1
        pytrend.build_payload(
            kw_list=[key_word[i][j]],
            cat=0,
            timeframe='2020-01-01 2020-12-31',
            geo='',
            gprop='')
        interest_over_time_df = pytrend.interest_over_time()
        interest_over_time_df.reset_index()
        if 'isPartial' in interest_over_time_df :
            l.append(interest_over_time_df.drop(['isPartial'], axis=1))
    interest = pd.concat(l, axis=1)
    interest.to_excel(writer, sheet_name=key_word[i][0])

    workbook = writer.book
    worksheet = writer.sheets[key_word[i][0]]  # pull worksheet object
    worksheet.set_column(0, n, 13)
    print(interest)
writer.save()