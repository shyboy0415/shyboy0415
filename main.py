#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os

import json

import crawler

crawl = crawler.Crawler("https://91biquge.cc", "test.xml", 3)
crawl.run()