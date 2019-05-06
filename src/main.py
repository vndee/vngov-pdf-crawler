from src.spy import Spy

if __name__ == '__main__':
    spy = Spy('http://vanban.chinhphu.vn/portal/page/portal/chinhphu/hethongvanban', '../output')
    spy.crawl()
    spy.__del__()