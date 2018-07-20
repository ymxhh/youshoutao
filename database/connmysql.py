# coding: utf-8
'''
Created on 2018年7月16日

@author: 27419
'''
import pymysql

def conntaoshouyou():
    tsy_db = pymysql.connect(
        host='172.0.0.11', 
        port=3306, 
        user='root', 
        passwd='123456', 
        db='taoshouyou'
        )
    return tsy_db

def get_data(tsy_db): 
    cursor = tsy_db.cursor()
    cursor.execute(r'select * from u_user where id=1992663')
    data = cursor.fetchone()
    print(data)
    
def close(tsy_db):
    tsy_db.close()


if '__name__' == '__main__':
    tsy_db = conntaoshouyou()
    get_data(tsy_db)
    close(tsy_db)