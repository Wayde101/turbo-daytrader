#!/home/tops/bin/python

import sys
sys.path.append('/home/yuting/project/turbo-daytrader/forexsys')

from django.core.management import setup_environ
from forexsys import settings
setup_environ(settings)

class Configuration:
    mt4shotpath = [
        '/home/yuting/project/yuting/Alpari/experts/files/shots',   #for trade
        '/home/yuting/project/yuting/MTidx/experts/files/shots',    #for usdx
        ]
    # for test.
    #mt4shotpath = [
    #    '/home/yuting/project/yuting/Alpari.dev/tester/files/shots'
    #    ]

    forexbase      = '/home/forexchart'
    ticketbase     = '/home/yuting/project/yuting/Alpari/experts/files/shots'
    ffmpegbin      = '/home/tops/bin/ffmpeg'
    #ticketbase     = '/home/yuting/project/yuting/Alpari.dev/tester/files/shots'
    convertbin     = '/usr/bin/convert'
    rsyncbin       = '/usr/bin/rsync'
    pg_backup	   = '%s/pgdump' % forexbase
    pg_home        = '/home/tops/pgsql-9.1'
    pg_dump        = '%s/bin/pg_dump' % pg_home
    psql           = '%s/bin/psql' % pg_home
    forexsys_db    = 'forexsys'
    forexsys_user  = 'forexsys'
    timeframe_map  = {'5':'5M',
                      '15':'15M',
                      '60':'1H',
                      '240':'4H',
                      '1440':'1D',
                      '10080':'1W',
                      '43200':'1Mon'}
    
    timeframe_list = ['5','15','60','240','1440','10080','43200']
    timeframe_col  = ['60','240','1440','10080','43200']
    currency_row   = ['eurusd','gbpusd','usdchf','audusd','usdcad','usdjpy']
    currency_flip  = ['usdcad','usdjpy','usdchf']
    database = settings.DATABASES
    
    def __init__(self):
        pass


if __name__ == '__main__':
    a = Configuration()
    print a.database
