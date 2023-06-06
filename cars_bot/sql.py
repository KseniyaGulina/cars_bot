import sqlite3


async def find(info):
    connect = sqlite3.connect('cars.db')
    cursor = connect.cursor()
    query = 'SELECT * FROM cars'
    where = []
    where_ans = []
    if info[0]:
        where.append("country = ?")
        where_ans.append(info[0])
    if info[1]:
        where.append("type = ?")
        where_ans.append(info[1])
    if info[2]:
        where.append("price >= ?")
        where_ans.append(info[2])
    if info[3]:
        where.append("price < ?")
        where_ans.append(info[3])
    if info[4]:
        where.append("year >= ?")
        where_ans.append(info[4])
    if info[5]:
        where.append("marka = ?")
        where_ans.append(info[5])
    if info[6]:
        where.append("model = ?")
        where_ans.append(info[6])
    if len(where):
        query += " WHERE " + 'AND '.join(i for i in where)
    cursor.execute(query, where_ans)
    data = cursor.fetchall()
    return data
