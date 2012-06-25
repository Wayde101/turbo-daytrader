#!/home/tops/bin/python

class Configuration:
    mt4shotpath = [
        '/home/yuting/project/yuting/Alpari/experts/files/shots'
        ]
    
    webgallerypath = '/home/yuting/src/3.0.5/examples'
    convertbin     = '/usr/bin/convert'
    template_list  = ['5m.tpl','1h.tpl']
    currency_list  = ['eurusd','gbpusd','usdchf','audusd','usdcad','usdjpy']
    timeframe_list = ['60','240','1440','10080','43200']

    webgallery_map = {
        "eurusd_60"    : '001',
        "eurusd_240"   : '002',
        "eurusd_1440"  : '003',
        "eurusd_10080" : '004',
        "eurusd_43200" : '005',
        "gbpusd_60"    : '006',
        "gbpusd_240"   : '007',
        "gbpusd_1440"  : '008',
        "gbpusd_10080" : '009',
        "gbpusd_43200" : '010',
        "usdchf_60"    : '011',
        "usdchf_240"   : '012',
        "usdchf_1440"  : '013',
        "usdchf_10080" : '014',
        "usdchf_43200" : '015',
        "audusd_60"    : '016',
        "audusd_240"   : '017',
        "audusd_1440"  : '018',
        "audusd_10080" : '019',
        "audusd_43200" : '020',
        "usdcad_60"    : '021',
        "usdcad_240"   : '022',
        "usdcad_1440"  : '023',
        "usdcad_10080" : '024',
        "usdcad_43200" : '025',
        "usdjpy_60"    : '026',
        "usdjpy_240"   : '027',
        "usdjpy_1440"  : '028',
        "usdjpy_10080" : '029',
        "usdjpy_43200" : '030'
        }
    
    def __init__(self):
        pass

