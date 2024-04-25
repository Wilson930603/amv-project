# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#pip install mysql-connector-python
import os,csv,re
import mysql.connector
from mysql.connector import Error

class CrawldataPipeline:
    def open_spider(self,spider):
        self.DATABASE_NAME='crawler'
        self.HOST='localhost'
        self.username='root'
        self.password='Crawler@2022'
        self.TABLE={}
        try:
            spider.conn = mysql.connector.connect(host=self.HOST,database=self.DATABASE_NAME,user=self.username,password=self.password)
            if spider.conn.is_connected():
                print('Connected to DB')
                db_Info = spider.conn.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
            else:
                print('Not connect to DB')
        except Error as e:
            print("Error while connecting to MySQL", e)
            spider.conn=None
    def process_item(self, ITEM, spider):
        #print('Do with DB')
        # Check and add more field if not existed in data table
        item={}
        for K,V in ITEM.items():
            item[self.Get_Key_String(K)]=str(V).replace('\\','').replace("'","\'")
        if not 'SHEET' in item.keys():
            item['SHEET']=spider.name
        if not item['SHEET'] in self.TABLE:
            self.TABLE[item['SHEET']]=[]
            self.create_table(spider.conn,item['SHEET'],item)
            SQL="SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = Database() AND TABLE_NAME = '"+item['SHEET']+"';"
            mycursor = spider.conn.cursor()
            mycursor.execute(SQL)
            myresult = mycursor.fetchall()
            for x in myresult:
                if not x[0] in self.TABLE[item['SHEET']]:
                    self.TABLE[item['SHEET']].append(x[0])
            print('FIELDS:',self.TABLE[item['SHEET']])

        for key in item.keys():
            if not key in self.TABLE[item['SHEET']] and key!='SHEET':
                self.TABLE[item['SHEET']].append(key)
                self.add_column_to_db(spider.conn,item['SHEET'],key)
        # Insert data to table
        SQL="INSERT INTO "+item['SHEET']
        LIST_FIELDS=''
        VALUES=''
        STR_UPDATE=''
        for key in self.TABLE[item['SHEET']]:
            if LIST_FIELDS=='':
                LIST_FIELDS=key
            else:
                LIST_FIELDS+=','+key
            if key in item:
                V=str(item[key]).replace("'","''")
                if V=='None':
                    V=""
            else:
                V=""
            if VALUES=='':
                VALUES="'"+V+"'"
            else:
                VALUES+=",'"+V+"'"
            if not 'KEY_' in key:
                if STR_UPDATE=="":
                    STR_UPDATE=key+"='"+V+"'"
                else:
                    STR_UPDATE+=", "+key+"='"+V+"'"
        SQL+="("+LIST_FIELDS+") VALUES("+VALUES+") ON DUPLICATE KEY UPDATE "+STR_UPDATE+";"
        cursor = spider.conn.cursor()
        try:
            cursor.execute(SQL)
            spider.conn.commit()
            #print('Isnerted to DB')
        except:
            print('Error: ',item,'\n',SQL)
        return item
    def get_DataType(self,strtxt):
        strtxt=str(strtxt).strip()
        if len(strtxt) == 0: return 'TEXT'
        if re.match(r'([-+]\s*)?\d+[lL]?$', strtxt): 
            return 'INT'
        if re.match(r'([-+]\s*)?[1-9][0-9]*\.?[0-9]*([Ee][+-]?[0-9]+)?$', strtxt): 
            return 'FLOAT'
        if re.match(r'([-+]\s*)?[0-9]*\.?[0-9][0-9]*([Ee][+-]?[0-9]+)?$', strtxt): 
            return 'FLOAT'
        return 'TEXT'
    def create_table(self,connection,table_name,item):
        SQL='CREATE TABLE IF NOT EXISTS '+table_name+'('
        KEY=' PRIMARY KEY ('
        i=0
        for K in item.keys():
            if 'KEY_' in K:
                SQL+=K+' VARCHAR(50) NOT NULL, '
                if i==0:
                    KEY+=K
                else:
                    KEY+=', '+K
                i+=1
        KEY+=')'
        SQL+=KEY+');'
        try:
            print('Creating Table:',table_name)
            cursor = connection.cursor()
            cursor.execute(SQL)
            connection.commit()
        except:
            print(SQL)
    def add_column_to_db(self,connection,table_name,field):
        SQL="ALTER TABLE "+table_name+" ADD COLUMN "+field+" "+self.get_DataType(field)+ " DEFAULT NULL;"
        try:
            print('Adding column name:',field)
            cursor = connection.cursor()
            cursor.execute(SQL)
            connection.commit()
        except:
            print(SQL)
    def Get_Key_String(self,xau):
        KQ=re.sub(r"([^A-Za-z0-9])","_", str(xau).strip())
        return KQ