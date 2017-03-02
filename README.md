# scrapy1.1.3、python3.5爬虫：爬取顶点小说网站，批量下载小说

> 使用的模块：BeautifulSoup4、re、pymysql

## 说明

<p>爬取的数据会存储于MySQL数据库中，需先在MySQL建立对应的库和表；并在sql.py文件中设置你的MySQL连接</p>
``` bash
conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='123456',
    db='xiaoshuo',
    charset='utf8'
)
```

## 运行步骤

``` bash
IDE下运行entrypoint.py (推荐使用pycharm)

```