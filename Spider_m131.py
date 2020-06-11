import os
import requests
from lxml import etree

class Spider_mm(object):
    """爬取妹子图"""

    def __init__(self,page_num):
        self.page_num = page_num

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
            'referer': 'https://www.m131.cc/xinggan/'
        }


    def get_page_urls(self):
        """获取指定页数的套图列表地址"""

        # 先放入第一页地址
        page_urls = ['https://www.m131.cc/xinggan/']

        if int(self.page_num) > 1:
            for n in range(2, int(self.page_num)+1):
                # 后续页码地址
                page_url = 'https://www.m131.cc/xinggan/' + str(n) + '.html'
                page_urls.append(page_url)
        elif int(self.page_num) == 1:
            pass

        return page_urls


    def get_pic_set_urls(self, page_url):
        """传入套图列表页地址，返回套图地址"""

        response = requests.get(page_url, headers=self.headers)
        html = etree.HTML(response.content)

        # 套图标题
        pic_set_titles = html.xpath(r'//div[@class="item masonry_brick masonry-brick"]//div[@class="ABox"]/a/img/@alt')

        temp_urls = html.xpath(r'//div[@class="item masonry_brick masonry-brick"]//div[@class="ABox"]/a/@href')
        # 完整套图地址
        pic_set_urls = list(map(lambda url: 'https://www.m131.cc' + url, temp_urls))

        return pic_set_titles, pic_set_urls


    def get_pic_urls(self, pic_set_url):
        """传入套图地址，返回套图所有图片地址"""

        response = requests.get(pic_set_url, headers = self.headers)
        html = etree.HTML(response.content)

        # 套图页码数，每页一张图
        total_page = html.xpath(r'//span[@class="totalpage"]/text()')[0]

        pic_page_urls = [pic_set_url]

        for n in range(2, int(total_page)+1):
            url = pic_set_url[:-5] + '_' + str(n) + '.html'
            pic_page_urls.append(url)
        
        pic_urls = []

        for pic_page_url in pic_page_urls:
            response = requests.get(pic_page_url, headers = self.headers)
            html = etree.HTML(response.content)

            pic_url = html.xpath(r'//p[@align="center"]/a/img/@src')[0]
            pic_urls.append(pic_url)

        return pic_urls


    def download_pic(self, pic_urls, pic_set_path):
        """传入套图图片地址列表及存储路径，将图片下载到传入的路径中"""

        img_name = 0
        for pic_url in pic_urls:
            img_name += 1
            img_data =requests.get(pic_url, headers = self.headers)
            pic_path = pic_set_path + '/' + str(img_name) + '.jpg'

            with open(pic_path, 'wb') as f:
                f.write(img_data.content)
                f.close



def main():
    print('开始啦')

    PICTURE_PATH = os.path.join(os.getcwd(), 'pictures/')
    try:
        os.mkdir(PICTURE_PATH)
    except:
        pass

    # 爬取页数
    page_num = 50

    spider = Spider_mm(page_num)


    page_urls = spider.get_page_urls()
    for page_url in page_urls:

        # 获取套图标题及地址
        [pic_set_titiles, pic_set_urls] = spider.get_pic_set_urls(page_url)

        for n, pic_set_url in enumerate(pic_set_urls):

            # 套图存储路径
            set_pic_path = PICTURE_PATH + pic_set_titiles[n]
            try:
                os.mkdir(set_pic_path)
            except:
                print('文件夹已存在')
                continue

            pic_urls =spider.get_pic_urls(pic_set_url)
            spider.download_pic(pic_urls, set_pic_path)

    print('结束啦')

if __name__ == '__main__':
    main()



    




