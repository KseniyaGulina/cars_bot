import sqlite3


async def find(item):
    print(item)
    connect = sqlite3.connect('cars.db')
    cursor = connect.cursor()
    query = 'SELECT * FROM cars WHERE marka = ?'
    cursor.execute(query, (item, ))
    data = cursor.fetchall()
    return data
