import urllib2
class UrlOpen:
    def __init__(self, timeout, retry):
        self.timeout = timeout
        self.retry = retry

    def GetPage(self, url):
        page = ''
        req = urllib2.Request(url)
        while self.retry:
            try:
                page = urllib2.urlopen(req, None, self.timeout).read().decode('utf-8', 'ignore')
                if page == '':
                    print '[Error]:No data got from %s ,program must be exit'% self.url
                    exit()
                return page
            except Exception,e:
                print '[Waring]:Get URL %s failed,the times of retry remain %d times' % self.url,self.retry
                self.retry -= 1
                continue
        print '[Error]:Cannot get the url %s, please check your network '% self.url
