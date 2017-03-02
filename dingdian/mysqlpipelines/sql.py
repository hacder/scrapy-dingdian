import pymysql

conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='123456',
    db='xiaoshuo',
    charset='utf8'
)
cursor = conn.cursor()


class Sql:

    @classmethod
    def insert_dd_name(cls, xs_name, xs_author, category, name_id):
        cursor.execute('insert into dd_name(xs_name,xs_author,category,name_id) values(%s,%s,%s,%s)',
                       (xs_name, xs_author, category, name_id))
        conn.commit()

    @classmethod
    def select_name(cls, name_id):
        # name_id='name_id'存在返回1，不存在返回0
        cursor.execute(
            'select exists(select 1 from dd_name where name_id=%s)', (name_id))
        return cursor.fetchall()[0]

    @classmethod
    def insert_dd_chaptername(cls, xs_chaptername, xs_content, id_name, num, url):
        cursor.execute('insert into dd_chaptername(xs_chaptername,xs_content,id_name,num,url) values(%s,%s,%s,%s,%s)',(xs_chaptername, xs_content, id_name, num, url))
        conn.commit()

    @classmethod
    def select_chapter(cls, url):
        cursor.execute(
            'select exists(select 1 from dd_chaptername where url=%s)', (url))
        return cursor.fetchall()[0]
