# sitemap-generator
安装依赖：
pip3 install BeautifulSoup4
pip3 install requests

修改main.py
# 当前域名的http链接, sitemap.xml路径，抓取的最大栈深度，支持1-3，建议设置为2，设置为3时，抓取时间非常长。
crawl = crawler.Crawler("https://91biquge.cc", "test.xml", 3)
crawl.run()

修改完了之后执行
main.py