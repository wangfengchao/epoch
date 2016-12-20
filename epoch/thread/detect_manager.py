# -*-coding:utf-8 -*-
import time
from threading import Thread

from epoch.thread.detect_proxy import DetectProxy

'''
定义一个管理线程,来管理产生的线程
'''


class Detect_Manager(Thread):

    def __init__(self, threadNum):
        Thread.__init__(self)
        self.pool = []
        for i in range(threadNum):
            self.pool.append(DetectProxy(i + 1, threadNum, "Thread-" + bytes(i + 1)))

    def run(self):
        self.startManager()
        self.checkState()

    def startManager(self):
        print len(self.pool)
        count = 1
        for thread in self.pool:
            count += 1
            thread.start()

    def checkState(self):
        print 'checkState.....'
        now = 0
        while now < len(self.pool):
            for thread in self.pool:
                if thread.isAlive():
                    now = 0
                    break
                else:
                    now += 1
            time.sleep(0.1)

        goodNum = 0
        badNum = 0
        for i in self.pool:
            goodNum += i.getGoodNum
            badNum += i.getBadNum

        print 'proxy good Num ---', goodNum
        print 'proxy bad Num ---', badNum