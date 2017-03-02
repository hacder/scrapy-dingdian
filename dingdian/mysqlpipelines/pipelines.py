from .sql import Sql
from dingdian.items import DingdianItem, DcontentItem


class DingdianPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, DingdianItem):
            name_id = item['name_id']
            ret = Sql.select_name(name_id)
            if ret[0] == 1:
                print('已经存在了')
                pass
            else:
                print('开始存小说标题')
                xs_author = item['author']
                xs_name = item['name']
                category = item['category']
                Sql.insert_dd_name(xs_name, xs_author, category, name_id)

        if isinstance(item, DcontentItem):
            chapterurl = item['chapterurl']
            rets = Sql.select_chapter(chapterurl)
            if rets[0] == 1:
                print('章节已存在')
            else:
                print('开始存章节内容')
                url = item['chapterurl']
                name_id = item['id_name']
                num = item['num']
                xs_chaptername = item['chaptername']
                xs_content = item['chaptercontent']
                Sql.insert_dd_chaptername(xs_chaptername, xs_content, name_id, num, url)
                return item
