#!/home/tops/bin/python

class Configuration:
    mt4shotpath = [
        '/home/yuting/project/yuting/Alpari/experts/files/shots',
        '/home/yuting/project/yuting/MTidx/experts/files/shots',
        ]

    #mt4shotpath = [
    #    '/home/yuting/project/yuting/Alpari.dev/tester/files/shots'
    #    ]
    forexbase      = '/home/forexchart'
    ticketbase     = '/home/yuting/project/yuting/Alpari/experts/files/shots'
    ffmpegbin      = '/home/yuting/tmp/ffmpeg-0.11.1/ffmpeg'
    #ticketbase     = '/home/yuting/project/yuting/Alpari.dev/tester/files/shots'
    convertbin     = '/usr/bin/convert'
    rsyncbin       = '/usr/bin/rsync'
    timeframe_list = ['5','15','60','240','1440','10080','43200']
    timeframe_col  = ['60','240','1440','10080','43200']
    currency_row   = ['eurusd','gbpusd','usdchf','audusd','usdcad','usdjpy']
    currency_flip  = ['usdcad','usdjpy','usdchf']
    
    def __init__(self):
        pass
