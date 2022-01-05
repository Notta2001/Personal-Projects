import pandas as pd
from pytrends.request import TrendReq
import psycopg2
import xlsxwriter
import matplotlib.pyplot as plt
pytrends = TrendReq(tz=360)
    
# Connect to sql
con = psycopg2.connect(database="postgres", user="postgres", password="05092001thang", host="localhost", port="2001")
cur = con.cursor()

# Read key words from excel
df = pd.read_excel('keytrends.xlsx', engine='openpyxl')
# Get the header of all columns
columns_name = list(df.columns)

def searching_by_month(keyword, field) :
    cur.execute('''
    SELECT  EXTRACT(
    MONTH FROM date
    ) AS "Month", sum(value) 
    from vn_trending
    WHERE keyword = '{}' and trend_type = '{}'
    GROUP BY EXTRACT(
    MONTH FROM date
    )
    '''.format(keyword, field))
    data = cur.fetchall()
    return data

# Creat a new table in sql
def create_table(table_name) :
    cur.execute("CREATE TABLE {}(id SERIAL,keyword TEXT NOT NULL,date DATE NOT NULL, Value INT NOT NULL, trend_type TEXT NOT NULL)".format(table_name))
    print("Table create sucessfully!")
    con.commit()

# Draw table
def line_chart(keyword, searches) :
    plt.plot(keyword, searches, label="Data")
    plt.legend()
    plt.title('TỪ KHÓA TÌM KIẾM NHIỀU NHẤT VIỆT NAM 2020')
    plt.show()

def bar_chart(keyword, searches) :
    plt.bar(keyword, searches,label="Data")
    plt.legend()
    plt.title('TỪ KHÓA TÌM KIẾM NHIỀU NHẤT VIỆT NAM 2019')
    plt.show()

# Query get top k records and put it to excel
def get_top_k(table_name, excel_name, k):
    writer = pd.ExcelWriter('{}'.format(excel_name), engine='xlsxwriter')
    cur.execute('''
        select *
        FROM( SELECT 
                keyword,
		        SUM (value)
	        FROM {}
	        GROUP BY keyword, trend_type) AS n1
        order by n1.sum desc
        limit {}
    '''.format(table_name, k))
    data_top = cur.fetchall()

    with xlsxwriter.Workbook('{}'.format(excel_name)) as workbook:
        worksheet = workbook.add_worksheet()

        for row_num, data in enumerate(data_top):
            worksheet.write_row(row_num, 0, data)
    return data_top

# Get data from Google trends
def trending_year(geo, table_name, excel_name, year):
    writer = pd.ExcelWriter('{}'.format(excel_name), engine='xlsxwriter', datetime_format='DD-MM-YYYY')
    for col in columns_name:
        df_=df[col]
        # Drop NULL and duplicate values in each column
        df_.dropna(inplace=True)
        df_.drop_duplicates()

        # Get list of keywords in each column
        keywords = df_.values.tolist()
        datasets = []
        for kw in keywords:
            pytrends.build_payload(
                kw_list=[kw],
                cat=0,
                timeframe='{}-01-01 {}-12-31'.format(year, year),
                geo=geo,
                gprop=''
            )
            data = pytrends.interest_over_time()

            # Change time format and drop isPartial column, NULL values
            data.index = pd.to_datetime(data.index)
            if not data.empty:
                data = data.drop(labels=['isPartial'], axis='columns')
                data.dropna(inplace=True)
                for i in range(data[kw].values.shape[0]):
                    cur.execute("INSERT INTO {}(keyword, date, value, trend_type) VALUES('{}', '{}', {}, '{}')".format(table_name,kw,data.index[i],data.values[i][0],col))
                    con.commit()
            datasets.append(data)

        # Make complete sheet and put it into excel
        sheet = pd.concat(datasets, axis=1)
        print(sheet)
        sheet.to_excel(writer, sheet_name=col.replace('/', '_'))
    writer.save()

def trending_monthly():
    workbook = xlsxwriter.Workbook('vn_trending_search_keyword_2020.xlsx')
    for col in columns_name:
        worksheet = workbook.add_worksheet(col)
        cur_column = 0
        header = ['keyword', 'THÁNG 1', 'THÁNG 2', 'THÁNG 3', 'THÁNG 4', 'THÁNG 5', 'THÁNG 6', 'THÁNG 7', 'THÁNG 8', 'THÁNG 9', 'THÁNG 10', 'THÁNG 11', 'THÁNG 12']
        for col_num, data in enumerate(header):
            worksheet.write(cur_column, col_num, data)
        cur_column += 1
        df_ = df[col]
        # Drop NULL and duplicate values in each column
        df_.dropna(inplace=True)
        df_.drop_duplicates()

        # Get list of keywords in each column
        keywords = df_.values.tolist()
        for kw in keywords :
            data = []
            data = searching_by_month(kw, col)
            if data :
                kw_data = [kw, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                for i in range(len(data)):
                    kw_data[int(data[i][0])] = data[i][1]
                for col_num, data in enumerate(kw_data):
                    worksheet.write(cur_column, col_num, data)
                cur_column += 1
        bold = workbook.add_format({'bold': True, 'border': True})
        worksheet.set_row(0, cell_format=bold)
        worksheet.set_column('A:A', cell_format=bold)
    workbook.close()

# Geo = ""
create_table("global_trending")
trending_year("", "global_trending",'global_trending.xlsx',2020)
get_top_k("global_trending",'vn_trending_result.xlsx',10)

# Geo = "VN"
create_table("vn_trending")
trending_year("VN","vn_trending", 'vn_trending.xlsx', 2020)

create_table("vn_trending_2019")
trending_year("VN","vn_trending_2019", 'vn_trending_2019.xlsx', 2019)

# Phase 2
get_top_k("vn_trending", 'vn_top_ten.xlsx',10)

# Task1 phase 3
trending_monthly()

# Task2 phase 3
k = get_top_k("vn_trending", 'vn_2020_top_five.xlsx', 5)
x = []
y = []
for i in range(len(k)) :
    x.append(k[i][0])
    y.append(k[i][1])
line_chart(x, y)

# Task 3 phase 3
k = get_top_k("vn_trending_2019", 'vn_2019_top_five.xlsx', 5)
x = []
y = []
for i in range(len(k)) :
    x.append(k[i][0])
    y.append(k[i][1])
bar_chart(x, y)

