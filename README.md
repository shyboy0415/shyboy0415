# 安装依赖
```
pip3 install BeautifulSoup4
pip3 install requests
```
# 使用
修改main.py
当前域名的https链接，sitemap.xml路径，抓取的最大栈深度，支持1-3，建议设置为2，设置为3时，抓取时间非常长。
```
crawl = crawler.Crawler("https://91biquge.cc", "sitemap.xml", 2)
crawl.run()
```
修改完了之后执行main.py

# 存在的问题
当设置抓取深度为3时，耗时非常长。
