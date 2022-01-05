import pandas as pd
from pytrends.request import TrendReq
import psycopg2
import xlsxwriter
import datetime

now = datetime.datetime.now()
print(type(now.year))

s1 = "1. Lấy dữ liệu trending từ file."
s2 = "2. Xuất báo cáo top 10 trending."
s3 = "3. Xuất báo cáo search keyword in 2020."
s4 = "4. Vẽ biểu đồ line chart top 5 trending các từ khóa tìm kiếm nhiều nhất 2020."
s5 = "5. Vẽ biểu đồ bar chart top 5 trending các từ khóa tìm kiếm nhiều nhất 2019."
s6 = "6. Thống kê tìm kiếm top trending 5 từ khóa trong 2 năm 2020, 2019"
s7 = "7. Thống kê các từ khóa tìm kiếm nhiều nhất tại Việt Nam hiện tại"
s8 = "99. Thoát"

def get_data_from_file():
    print("Input START TIME(Note that input data has only from start year 2019, to now)")
    start_day = 0
    start_year = 0
    start_month = 0
    end_year = 0
    end_month = 0
    end_day = 0

    run = True
    while run:
        start_year = int(input("Year: "))
        start_month = int(input("Month: "))
        start_day = int(input("Day: "))
        if start_year < 2019 or start_year > now.year or start_month < 1 or start_month > 12 or start_day < 1 or start_day > 31:
            print("     Please input your start date again!")
        else:
            print("So that start date is " + str(start_year) + "-" + str(start_month) + "-" + str(start_day))
            print("     1. Yes")
            print("     2. No, input again!")
            yn = int(input("    You choose :"))
            if yn == 1:
                run = False
            elif yn == 2:
                pass
            else:
                print("     We can't accept that input! Please do it again.")
    print("Input END TIME(Note that input data has only from start year 2019, to now). You can choose")
    run = True
    while run:
        end_year = int(input("Year: "))
        end_month = int(input("Month: "))
        end_day = int(input("Day: "))
        if end_year < 2019 or end_year > now.year or end_month < 1 or end_month > 12 or end_day < 1 or end_day > 31 or start_year > end_year or start_year <= end_year and end_month < start_month or start_year <= end_year and start_month <= end_month and start_day > end_day:
            print("     Please input your end date again!")
        else:
            print("So that end date is " + str(end_year) + "-" + str(end_month) + "-" + str(end_day))
            print("     1. Yes")
            print("     2. No, input again!")
            yn = int(input("    You choose :"))
            if yn == 1:
                run = False
            elif yn == 2:
                pass
            else:
                print("     We can't accept that input! Please do it again.")
    s_time_frame = str(start_year) + "-" + str(start_month) + "-" + str(start_day) + " " + str(end_year) + "-" + str(
        end_month) + "-" + str(end_day)
    f_name = str(input("Key words file name :"))
    if f_name == "":
        f_name = "keytrends.xlsx"
    input_data(s_time_frame, f_name, "", "trending")

def add_highest_month(rd, year):
    conn, cur = connect(local_host, port, database, user, password)
    df = pd.DataFrame(rd, columns=['keyword', 'value', 'trend_type'])
    max_month = []
    rd = [list(ele) for ele in rd]
    for i in range(len(df['keyword'])):
        print(df['keyword'][i])
        cur.execute('''
                            SELECT EXTRACT (month from date) as mon, 
                            sum(value) 
                            from trending
                            WHERE keyword = '{}' and trend_type = '{}' and EXTRACT(YEAR FROM date::DATE) = {}
                            GROUP BY 1
                            ORDER BY 2 DESC
                            LIMIT 1
                            '''.format(df['keyword'][i], df['trend_type'][i], year))
        data_month = cur.fetchall()
        rd[i].append( data_month [0][0])
    df = pd.DataFrame(rd, index=['1', '2', '3', '4', '5'],
                      columns=['Keyword', 'Số lần tìm kiếm', 'trend_type', 'Tháng tìm kiếm nhiều nhất'])
    df = df.drop(labels=['trend_type'], axis='columns')
    return df

def get_top_10_trending():
    rd = get_top_k("trending", "test.xlsx", 10)
    conn, cur = connect(local_host, port, database, user, password)
    df = pd.DataFrame(rd, columns=['keyword', 'value', 'trend_type'])
    max_month = []
    rd = [list(ele) for ele in rd]
    for i in range(len(df['keyword'])):
        cur.execute('''
                    SELECT to_char(date, 'Mon') as mon,
		            EXTRACT(year from date) as year,
		            keyword,
		            trend_type,
		            SUM(value) as "value"
                    FROM global_trending
                    WHERE keyword = '{}' and trend_type = '{}'
                    GROUP BY 1,2,3,4
                    ORDER BY value DESC
                    LIMIT 1
                    '''.format(df['keyword'][i], df['trend_type'][i]))
        data_month = cur.fetchall()
        rd[i].append(str(data_month[0][0]) + " " + str(int(data_month[0][1])))
    df = pd.DataFrame(rd, index=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
                      columns=['Keyword', 'Số lần tìm kiếm', 'trend_type', 'Tháng tìm kiếm nhiều nhất'])
    df = df.drop(labels=['trend_type'], axis='columns')
    workbook = xlsxwriter.Workbook('top_ten_tech_search.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "STT")
    worksheet.write(0, 1, "Keyword")
    worksheet.write(0, 2, "Số lần tìm kiếm")
    worksheet.write(0, 3, "Tháng tìm kiếm nhiều nhất")
    for i in range (10):
        worksheet.write(i+1, 0, i+1)
        worksheet.write(i+1, 1, df['Keyword'].values[i])
        worksheet.write(i+1, 2, df['Số lần tìm kiếm'].values[i])
        worksheet.write(i+1, 3, df['Tháng tìm kiếm nhiều nhất'].values[i])
    cell_format = workbook.add_format()
    cell_format.set_align('center')
    worksheet.set_column('A:E', 20, cell_format)
    workbook.close()

def get_top_k(table_name, excel_name, k):
    conn, cur = connect(local_host, port, database, user, password)
    cur.execute('''
        select *
        FROM( SELECT 
                keyword,
		        SUM (value),
		        trend_type
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

def connect(local_host, port, database, user, password):
    """ Connect to the PostgreSQL database server """
    conn, cur = None, None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host="{}".format(local_host), port="{}".format(port),
            database="{}".format(database),
            user="{}".format(user),
            password="{}".format(password))
        # create a cursor
        cur = conn.cursor()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while excuting SQL" + error)

    return conn, cur

def input_data(s_time_frame, f_name, geo, table_name):
    pytrend = TrendReq(tz=360)
    try:
        kw_list_file = pd.read_excel(f_name, engine='openpyxl')
        column_names = list(kw_list_file.columns[:])
        conn, cur = connect(local_host, port, database, user, password)

        cur.execute('''CREATE TABLE  IF NOT EXISTS {}(
                                   id SERIAL PRIMARY KEY,
                                   date DATE NOT NULL,
                                   keyword TEXT NOT NULL,
                                   value INTEGER NOT NULL,
                                   trend_type TEXT NOT NULL);'''.format(table_name)
                    )
        conn.commit()
        print("Table created successfully")

        columns = "keyword, date, value, trend_type"
        for column in column_names:
            dataset = []
            df = kw_list_file[column]
            df.dropna(inplace=True)
            df.drop_duplicates().reset_index()
            df_l = df.values.tolist()
            for index in range(len(df_l)):
                pytrend.build_payload(
                    kw_list=[df[index]],
                    cat=0, geo=geo,
                    timeframe=s_time_frame,
                    gprop='')
                data = pytrend.interest_over_time()
                if not data.empty:
                    data = data.drop(labels=['isPartial'], axis='columns')

                    len_dt = len(data)
                    keyw = df[index]
                    kws = keyw.replace("'", "''")
                    data.index = pd.to_datetime(data.index).strftime('%Y-%m-%d')
                    dataset.append(data)
                    dts1 = data.index
                    vl = data.values
                    insert_stmt = ''
                    for i in range(len_dt):
                        if vl[i] > 0 and df[index] != 'NaN':
                            values = "VALUES ('{}','{}','{}','{}')".format(kws, dts1[i], vl[i][0], column)
                            insert_stmt += "INSERT INTO {} ({}) ({});".format(table_name, columns, values)
                    cur.execute(insert_stmt)
                    conn.commit()
        conn.close()
        print("Lưu dữ liệu thành công.")
    except Exception as ex:
        print("Có lỗi xảy ra trong quá trình đọc file, hoặc file không tồn tại, hoặc file không đúng định dạng!")
        print(ex)

def search_key_word(table_name, excel_name):
    print(s3)
    sql = """SELECT trend_type,keyword, to_char(date::date,'mm/yyyy') monthly, sum(VALUE::INT) sum_val
                FROM {}
                WHERE EXTRACT(YEAR FROM date::DATE) = 2020
                GROUP BY trend_type,keyword,to_char(date::date,'mm/yyyy') 
                ORDER BY trend_type, keyword;
            """.format(table_name)
    conn, cur = connect(local_host, port, database, user, password)
    cur.execute(sql)
    rd = cur.fetchall()
    conn.close()
    cur.close()
    writer = pd.ExcelWriter(excel_name, engine='xlsxwriter')
    df = pd.DataFrame(rd, columns=['trend_type', 'keyword', 'monthly', 'sum_val'])
    df_types = df['trend_type'].drop_duplicates().reset_index()['trend_type']
    for trend in range(len(df_types)):
        trend_type = df_types[trend]
        df1 = df[df['trend_type'] == df_types[trend]]
        df2 = df1.pivot_table(index="keyword", columns="monthly", values='sum_val')
        df2 = df2.set_axis(
            ['THÁNG 1', 'THÁNG 2', 'THÁNG 3', 'THÁNG 4', 'THÁNG 5', 'THÁNG 6', 'THÁNG 7', 'THÁNG 8', 'THÁNG 9',
             'THÁNG 10', 'THÁNG 11', 'THÁNG 12'], axis=1, inplace=False)
        sheet_name = trend_type.replace('/', '_')
        df2.to_excel(writer, sheet_name=sheet_name)
    writer.save()

def top_five_trending(year='2019, 2020', table_name = 'global_trending'):
    conn, cur = connect(local_host, port, database, user, password)
    if year == '2020':
        print(s4)
        sql = build_sql2(year, 5, table_name)
        cur.execute(sql)
        rd = cur.fetchall()
        # df = pd.DataFrame(rd, columns=['stt', 'keyword', 'sum_val', 'monthly', 'max_val'])
        df = pd.DataFrame(rd, columns=['keyword', 'Value'])
        if len(df):
            image = df.plot(x='keyword', y='Value', legend='keyword',
                            title='TỪ KHÓA TÌM KIẾM NHIỀU NHẤT 2020')
            fig = image.get_figure()
            fig.savefig('top_search_key_2020.png')
    elif year == '2019':
        print(s5)
        sql = build_sql2(year, 5, table_name)
        cur.execute(sql)
        rd = cur.fetchall()
        df = pd.DataFrame(rd, columns=['keyword', 'Value'])
        if len(df):
            image = df.plot.bar(x='keyword', y='Value', legend='keyword',
                                title='TỪ KHÓA TÌM KIẾM NHIỀU NHẤT 2019')
            fig = image.get_figure()
            fig.savefig('top_search_key_2019.png')

def build_sql(year=2020, limit=10, table_name='global_trending'):
    sql = """SELECT keyword, sum(VALUE::INT) sum_val, trend_type
                        FROM {}
                        WHERE EXTRACT(YEAR FROM DATE) = {}
                        GROUP BY keyword, trend_type
                        ORDER BY sum(VALUE::INT) DESC
                        LIMIT {}
                    ;""".format(table_name, year, limit)

    return sql

def build_sql2(year=2020, limit=10, table_name='global_trending'):
    sql = """SELECT keyword, sum(VALUE::INT) sum_val
                        FROM {}
                        WHERE EXTRACT(YEAR FROM DATE) = {}
                        GROUP BY keyword, trend_type
                        ORDER BY sum(VALUE::INT) DESC
                        LIMIT {}
                    ;""".format(table_name, year, limit)

    return sql

def top_5_trending_2019_2020():
    conn, cur = connect(local_host, port, database, user, password)
    workbook = xlsxwriter.Workbook('top_5_trending_2019_2020.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.merge_range('A1:G1', 'Merged Range')
    worksheet.write(0, 0, "THỐNG KÊ TÌM KIẾM NHIỀU NHẤT TRONG 2 NĂM")
    worksheet.merge_range('A2:D2', 'Merged Range')
    worksheet.merge_range('E2:G2', 'Merged Range')
    worksheet.write(1, 0, "Năm 2020")
    worksheet.write(1, 4, "Năm 2019")
    cell_format = workbook.add_format()
    cell_format.set_align('center')
    worksheet.set_column('A:G', 20, cell_format)
    sql1 = build_sql(2020, 5, 'global_trending')
    cur.execute(sql1)
    rd1 = cur.fetchall()
    rd1 = add_highest_month(rd1, 2020)
    sql2 = build_sql(2019, 5, 'global_trending')
    cur.execute(sql2)
    rd2 = cur.fetchall()
    rd2 = add_highest_month(rd2, 2019)
    rd = [rd1, rd2]
    rd = pd.concat(rd, axis=1)
    cur_row = 2
    worksheet.write(cur_row, 0, "STT")
    worksheet.write(cur_row, 1, "Keyword")
    worksheet.write(cur_row, 2, 'Số lần tìm kiếm')
    worksheet.write(cur_row, 3, 'Tháng tìm kiếm nhiều nhất')
    worksheet.write(cur_row, 4, 'Keyword')
    worksheet.write(cur_row, 5, 'Số lần tìm kiếm')
    worksheet.write(cur_row, 6, 'Tháng tìm kiếm nhiều nhất')
    cur_row += 1
    for i in range(5):
        worksheet.write(cur_row, 0, i + 1)
        worksheet.write(cur_row, 1, rd['Keyword'].values[i][0])
        worksheet.write(cur_row, 2, rd['Số lần tìm kiếm'].values[i][0])
        worksheet.write(cur_row, 3, rd['Tháng tìm kiếm nhiều nhất'].values[i][0])
        worksheet.write(cur_row, 4, rd['Keyword'].values[i][1])
        worksheet.write(cur_row, 5, rd['Số lần tìm kiếm'].values[i][1])
        worksheet.write(cur_row, 6, rd['Tháng tìm kiếm nhiều nhất'].values[i][1])
        cur_row += 1

    print(rd['Keyword'].values[2][1])
    workbook.close()

def VN_trending_search():
    pytrend = TrendReq(tz=360)
    df = pytrend.trending_searches(pn='vietnam')
    workbook = xlsxwriter.Workbook('vn_search_lastest.xlsx                                             ')
    worksheet = workbook.add_worksheet()
    for i in range(20):
        worksheet.write(i, 0, i)
        worksheet.write(i, 1, df.at[i, 0])
    workbook.close()


running = True
do = 1
while(running) :
    print("WELCOME TO OUR APPLICATION!")
    print("...")
    print(s1)
    print(s2)
    print(s3)
    print(s4)
    print(s5)
    print(s6)
    print(s7)
    print("...")
    print(s8)
    while do > 0:
        print("Để truy cập vào database vui lòng nhập thông tin cần thiết")
        local_host = str(input("Local Host : "))
        port = str(input("Port : "))
        database = str(input("Database : "))
        user = str(input("User : "))
        password = str(input("Password : "))
        do -= 1
    choose = int(input("You choose : "))
    if choose == 1:
        get_data_from_file()
        input_data("2019-01-01 2020-12-30", "keytrends.xlsx", "", "global_trending")
    elif choose == 2:
        get_top_10_trending()
    elif choose == 3:
        search_key_word('global_trending', 'tech_search_2020.xlsx')
    elif choose == 4:
        top_five_trending('2020', 'global_trending')
    elif choose == 5:
        top_five_trending('2019', 'global_trending')
    elif choose == 6:
        top_5_trending_2019_2020()
    elif choose == 7:
        VN_trending_search()
    elif choose == 99:
        running = False
    else:
        print("We can't accept that input! Please do it again.")

