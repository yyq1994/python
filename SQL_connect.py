import pymssql

# 服务器名[端口],账户,密码,数据库名
with pymssql.connect('localhost:1433', 'sa', 'admin', 'test') as connect:
    if connect:
        print("连接成功!")

    cur = connect.cursor()
    sql = 'select * from test'
    cur.execute(sql)

    #读取查询结果,
    row = cur.fetchone()

    # 循环读取所有结果
    while row:
        print("Name=%s, Sex=%s" % (row[0],row[1]))
        row = cur.fetchone()
    connect.commit()

