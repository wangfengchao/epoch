import os

from epoch import settings


class DaomubijiPipeline(object):
    def process_item(self, item, spider):
        dir_path = '%s/%s/%s' % (settings.FILES_STORE, spider.name, item['bookName']+'_'+item['bookTitle'])
        print 'dir_path', dir_path
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        file_path = '%s/%s' % (dir_path, item['chapterNum']+'_'+item['chapterName']+'.txt')
        with open(file_path, 'w') as file_writer:
            file_writer.write(item['chapterContent'].encode('utf-8'))
            file_writer.write('\r\n'.encode('utf-8'))

        file_writer.close()
        return item