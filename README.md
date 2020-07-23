# 安装依赖
```
pip3 install BeautifulSoup4
pip3 install requests
```
# 使用
修改main.py
当前域名的https链接，sitemap.xml路径，抓取的最大栈深度，支持1-3，建议设置为。
```
crawl = crawler.Crawler("https://91biquge.cc", "sitemap.xml", 2)
crawl.run()
```
修改完了之后执行main.py

抓取深度为2，耗时测试如下：
```
07/23/2020 20:59:30 PM - INFO - generate sitemap for https://91biquge.cc
07/23/2020 20:59:30 PM - INFO - sitemap generate take: 91 s
07/23/2020 20:59:30 PM - INFO - sitemap urls size is 98233 urls
07/23/2020 21:00:21 PM - INFO - generate sitemap for https://maddogreading.cc
07/23/2020 21:00:21 PM - INFO - sitemap generate take: 50 s
07/23/2020 21:00:21 PM - INFO - sitemap urls size is 142365 urls
07/23/2020 21:05:39 PM - INFO - generate sitemap for https://youku.91biquge.cc
07/23/2020 21:05:39 PM - INFO - sitemap generate take: 317 s
07/23/2020 21:05:39 PM - INFO - sitemap urls size is 150261 urls
```

# 存在的问题
当设置抓取深度为3时，耗时非常长。
