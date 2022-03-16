import pandas as pd
from pytrends.request import TrendReq
import psycopg2
import xlsxwriter
pytrends = TrendReq(tz=360)
    
# Connect to sql
con = psycopg2.connect(database="postgres", user="postgres", password="05092001thang", host="localhost", port="2001")
cur = con.cursor()

# Read key words from excel
df = pd.read_excel('keytrends.xlsx', engine='openpyxl')
# Get the header of all columns
columns_name = list(df.columns)

# Creat a new table in sql
def create_table(table_name) :
    cur.execute("CREATE TABLE {}(id SERIAL,keyword TEXT NOT NULL,date DATE NOT NULL, Value INT NOT NULL, trend_type TEXT NOT NULL)".format(table_name))
    con.commit()

# Query get top 10 records and put it to excel
def get_top_10(table_name, excel_name):
    writer = pd.ExcelWriter('{}'.format(excel_name), engine='xlsxwriter')
    cur.execute('''
        select *
        FROM( SELECT 
                keyword,
		        SUM (value)
	        FROM {}
	        GROUP BY keyword ) AS n1
        order by n1.sum desc
        limit 10  
    '''.format(table_name))
    with xlsxwriter.Workbook('{}'.format(excel_name)) as workbook:
        worksheet = workbook.add_worksheet()

        for row_num, data in enumerate(cur.fetchall()):
            worksheet.write_row(row_num, 0, data)

# Get data from Google trends
def trending(geo, table_name, excel_name):
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
                timeframe='2020-01-01 2020-12-31',
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

# Geo = ""
create_table("global_trending")
trending("", "global_trending",'global_trending.xlsx')
get_top_10("global_trending",'vn_trending_result.xlsx')

# Geo = "VN"
create_table("vn_trending")
trending("VN","vn_trending", 'vn_trending.xlsx')
get_top_10("vn_trending", 'vn_top_ten.xlsx')