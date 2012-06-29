#!/home/tops/bin/python

class Configuration:
    mt4shotpath = [
        '/home/yuting/project/yuting/Alpari/experts/files/shots'
        ]

    imgbakuppath   = '/home/forexchart/'
    convertbin     = '/usr/bin/convert'
    rsyncbin       = '/usr/bin/rsync'
    timeframe_col  = ['60','240','1440','10080','43200']
    currency_row   = ['eurusd','gbpusd','usdchf','audusd','usdcad','usdjpy']
    currency_flip  = ['usdcad','usdjpy','usdchf']
    
    def __init__(self):
        pass

