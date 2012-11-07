#!/home/tops/bin/python

import sys
sys.path.append('/home/yuting/project/turbo-daytrader/forexsys')

from django.core.management import setup_environ
from forexsys import settings
setup_environ(settings)

from tradesys.models import *
from tradesys.views import *

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

    #ticketbase    = '/home/yuting/project/yuting/Alpari.dev/tester/files/shots'
    ticketbase     = '/home/yuting/project/yuting/Alpari/experts/files/shots'
    ffmpegbin      = '/home/tops/bin/ffmpeg'

    convertbin     = '/usr/bin/convert'
    rsyncbin       = '/usr/bin/rsync'
    pg_backup	   = '%s/pgdump' % forexbase
    pg_home        = '/home/tops/pgsql-9.1'
    pg_dump        = '%s/bin/pg_dump' % pg_home
    psql           = '%s/bin/psql' % pg_home
    forexsys_db    = settings.DATABASES['default']['NAME']
    forexsys_user  = settings.DATABASES['default']['USER']

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

    def __init__(self):
        pass


if __name__ == '__main__':
    a = Configuration()
