#!/usr/bin/env python3
# coding=utf-8
# -*- coding: utf-8 -*-
import requests
import datetime
import re
import logging
import datetime
from bs4 import BeautifulSoup

class Crawler:
    domain = ""
    #url_root = 'https://91biquge.cc'
    #url_mine_list = [
    #    'https://91biquge.cc',
    #]
    
    file = None
    output_file = ""

    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    url_res_final = []
    max_depth = 2
    current_depth = 1
    times = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    url_robot_arr = [
        '/user/sign_up',
        '/user/login',
        '/user/forgot_password'
    ]
    url_static_arr = [
        '.js',
        '.css',
        '.cscc',
        'None',
        'about:blank'
    ]

    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

    def __init__(self, domain="", output="sitemap.xml", depth=1):
        self.domain = domain
        self.output_file = output
        self.max_depth = depth
        logging.basicConfig(filename='sitemap_generator.log', level=logging.INFO, format=self.LOG_FORMAT, datefmt=self.DATE_FORMAT)
        logging.debug('domain: %s', self.domain)
        logging.debug('output: %s', self.output_file)
        logging.debug('depth: %s', self.max_depth)
        if self.max_depth <= 0 or self.max_depth > 3:
            raise IllegalArgumentError("Depth must be 1 - 3")

    def is_static(self, url):
        url = str(url)
        for static in self.url_static_arr:
            if url.endswith(static):
                return True
        return False

    def is_robot(self, url):
        url = str(url)
        for robot in self.url_robot_arr:
            if url.startswith(robot):
                return True
        return False

    def getlinks(self, url):
        pages = requests.get(url)
        html = pages.text
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a')
        return self.filterlinks(links)

    def filterlinks(self, links):
        tmplinks = []
        for link in links:
            url = str(link.get('href'))
            if url is None or url == '':
                continue
            ishttp = url.startswith('http')
            ismine = url.startswith(self.domain)
            if ishttp and (not ismine):
                continue
            if url.startswith('#') or '/' == url.strip():
                continue
            if url.startswith("?"):
                continue
            if self.is_static(url):
                continue
            if self.is_robot(url):
                continue
            if not ishttp and url.startswith("/"):
                url = self.domain  + url
            elif not ishttp:
                url = self.domain + '/'  + url
            tmplinks.append(url)
        reslinks = list(set(tmplinks))
        return reslinks

    def parser(self, url_arr, depth):
        logging.debug('sitemap depth %s start', depth)
        url_tmp = []
        for urlmine in url_arr:
            links = self.getlinks(urlmine)
            url_tmp.extend(links)
            logging.debug('processing: %s get %s urls', urlmine, len(links))
        url_tmp = list(set(url_tmp).difference(set(self.url_res_final)))
        self.url_res_final.extend(url_tmp)
        self.sitemap_add_urls(url_tmp, depth)
        depth += 1
        if(depth > self.max_depth):
            return
        self.parser(url_tmp, depth)

    def sitemap_header(self):
        header = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        self.file = open(self.output_file, 'w', encoding='utf-8')
        self.file.writelines(header)
        
        url = self.domain
        urls = re.sub(r"&", "&amp;", url)
        ment = "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>1.00</priority>\n  </url>\n" % (urls, self.times)
        self.file.writelines(ment)
        self.file.flush
        #self.file.close()
        
    def sitemap_add_urls(self, url_list, depth):
        priority = self.get_priority(depth)
        frequency = self.get_frequency(depth)
        logging.debug('depth is %s, priority: %s, frequency: %s',depth, priority, frequency)
        for url in url_list:
            urls = re.sub(r"&", "&amp;", url)
            ment = "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>\n" % (urls, self.times, frequency,priority)
            logging.debug('add url into xml: %s \n', ment)
            self.file.writelines(ment)
        self.file.flush
        
    def sitemap_end(self):
        last = "</urlset>"
        self.file.writelines(last)
        self.file.flush
        self.file.close()
        
    def get_priority(self, depth):
        priority = '0'
        if depth == 1:
            priority = '1.00'
        elif depth == 2:
            priority = '0.90'
        elif depth == 3:
            priority = '0.80'
        else:
            priority = '0'
        return priority
        
    def get_frequency(self, depth):
        frequency = 'weekly'
        if depth == 1:
            frequency = 'daily'
        return frequency
        
    def run(self):
        starttime = datetime.datetime.now()
        self.times = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
        url_tmp = []
        url_tmp.append(self.domain)
        self.url_res_final.append(self.domain)
        logging.debug('parser domain: %s', url_tmp)
        self.sitemap_header()
        self.parser(url_tmp, 1)
        self.sitemap_end()
        endtime = datetime.datetime.now()
        logging.debug('sitemap generate take: %s s', (endtime - starttime).seconds)
        logging.debug('sitemap size is %s urls', len(self.url_res_final))