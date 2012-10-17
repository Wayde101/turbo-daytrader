#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os, re, sys
import urllib,urllib2

from  xml.dom import minidom as pydom

class QueryResComp:
    def __init__(self, serviceName):
        self.serviceName    = serviceName
        self.queryString    = ''

        self.leftagg        = 'http://10.249.84.102:9000'
        self.rightagg        = 'http://aggregator.daogou.yh.vip.aliyun.com:9090'

        qStr = ()

        self.leftXmlRes    = ''
        self.rightXmlRes   = ''

    def fetchResult(self,queryString):
        qStr = (('shortcut','--Method=Search --Parameter="'+queryString+'"'),)
        print urllib.urlencode(qStr)
        # req=urllib2.Request(self.rightagg,urllib.urlencode(qStr))
        # u=urllib2.urlopen(req)
        # print u.read()
        
    def parseUrlList(self,xmlRes):
        res = []
        sec = ''
                
        if self.serviceName == 'daogou_auction':
            sec = 'nid'
        else:
            sec = 'url'

        dom = pydom.parseString(xmlRes)
        for ele in dom.getElementsByTagName(sec):
            res.append(ele.firstChild.wholeText)

        return res
    
    def isEqual(self):
        if(len(self.leftXmlRes)==0 or len(self.rightXmlRes)==0):
            print "Query[%s] got 0result" % self.queryString
            return False


        leftUrlArray= self.parseUrlList(self.leftXmlRes)
        rightUrlArray= self.parseUrlList(self.rightXmlRes)
        
        if(leftUrlArray == rightUrlArray):
            return True
        else:
            return False


    
            
    
        


if __name__ == '__main__':
    
    xmlstr = '''<?xml version="1.0" encoding="UTF-8"?>
<Root>
<TotalTime>0.055</TotalTime>
<hits numhits="10" totalhits="117892">
	<hit hash_id="3" docid="9212704">
		<fields>
			<biz30day><![CDATA[1]]></biz30day>
			<cat_id><![CDATA[1512]]></cat_id>
			<comment0><![CDATA[超级喜欢~~~速度还很快。超值]]></comment0>
			<comment1><![CDATA[货很正。]]></comment1>
			<comment2><![CDATA[]]></comment2>
			<comment_num><![CDATA[2]]></comment_num>
			<comment_rate0><![CDATA[4]]></comment_rate0>
			<comment_rate1><![CDATA[41]]></comment_rate1>
			<comment_rate2><![CDATA[]]></comment_rate2>
			<comment_user0><![CDATA[1157saygoodbye]]></comment_user0>
			<comment_user1><![CDATA[changzheng92]]></comment_user1>
			<comment_user2><![CDATA[]]></comment_user2>
			<commercial><![CDATA[0]]></commercial>
			<desp><![CDATA[產品規格
顯示所有 隱藏所有
手機功能、電...]]></desp>
			<grade_avg><![CDATA[0]]></grade_avg>
			<nick><![CDATA[zpin10]]></nick>
			<nid><![CDATA[4052667480]]></nid>
			<people_num><![CDATA[0]]></people_num>
			<pict_url><![CDATA[i8/T1F18AXm4jXXbkT1c0_034730.jpg]]></pict_url>
			<pid><![CDATA[78348588]]></pid>
			<pidvidt><![CDATA[]]></pidvidt>
			<product_num><![CDATA[6201]]></product_num>
			<ratesum><![CDATA[9]]></ratesum>
			<reserve_price><![CDATA[2020]]></reserve_price>
			<seller_goodrate><![CDATA[9993]]></seller_goodrate>
			<title><![CDATA[*五年钻石好店三包赔付保障*<font color=red>Nokia</font>/诺基亚 X6]]></title>
			<total_sold_quantity><![CDATA[11]]></total_sold_quantity>
			<user_nid><![CDATA[22839402]]></user_nid>
			<user_strid><![CDATA[cfc07f8231e153dbdbfe872bf9f41ff0]]></user_strid>
		</fields>
		<property>
		</property>
		<sortExprValues>
			0.000210171
		</sortExprValues>
	</hit>
	<hit hash_id="0" docid="9190361">
		<fields>
			<biz30day><![CDATA[1]]></biz30day>
			<cat_id><![CDATA[50012584]]></cat_id>
			<comment0><![CDATA[给妹妹买的，她说不错，和在街上买的价格差不多，...]]></comment0>
			<comment1><![CDATA[宝贝都很不错,买家态度老好了,以后有需要还会继续...]]></comment1>
			<comment2><![CDATA[好使 没坏 就是有点贵]]></comment2>
			<comment_num><![CDATA[6]]></comment_num>
			<comment_rate0><![CDATA[501]]></comment_rate0>
			<comment_rate1><![CDATA[41]]></comment_rate1>
			<comment_rate2><![CDATA[41]]></comment_rate2>
			<comment_user0><![CDATA[空瓶子zch]]></comment_user0>
			<comment_user1><![CDATA[huihui_katrina]]></comment_user1>
			<comment_user2><![CDATA[showwinter]]></comment_user2>
			<commercial><![CDATA[0]]></commercial>
			<desp><![CDATA[<font color=red>Nokia</font>线充E65 E90 E95 N70充电器 N71 N72线充]]></desp>
			<grade_avg><![CDATA[0]]></grade_avg>
			<nick><![CDATA[taotao8601]]></nick>
			<nid><![CDATA[4042745681]]></nid>
			<people_num><![CDATA[0]]></people_num>
			<pict_url><![CDATA[i8/T1b0JBXlhyXXXSaBs2_044823.jpg]]></pict_url>
			<pid><![CDATA[23620066]]></pid>
			<pidvidt><![CDATA[]]></pidvidt>
			<product_num><![CDATA[2806]]></product_num>
			<ratesum><![CDATA[11]]></ratesum>
			<reserve_price><![CDATA[8]]></reserve_price>
			<seller_goodrate><![CDATA[9730]]></seller_goodrate>
			<title><![CDATA[<font color=red>Nokia</font>线充E65 E90 E95 N70充电器 N71 N72线充 N73线充]]></title>
			<total_sold_quantity><![CDATA[72]]></total_sold_quantity>
			<user_nid><![CDATA[74665395]]></user_nid>
			<user_strid><![CDATA[561198dfa4cd940c717cc84ca2b5fbd8]]></user_strid>
		</fields>
		<property>
		</property>
		<sortExprValues>
			0.000210171
		</sortExprValues>
	</hit>
	<hit hash_id="2" docid="9176120">
		<fields>
			<biz30day><![CDATA[1]]></biz30day>
			<cat_id><![CDATA[1512]]></cat_id>
			<comment0><![CDATA[]]></comment0>
			<comment1><![CDATA[]]></comment1>
			<comment2><![CDATA[]]></comment2>
			<comment_num><![CDATA[0]]></comment_num>
			<comment_rate0><![CDATA[]]></comment_rate0>
			<comment_rate1><![CDATA[]]></comment_rate1>
			<comment_rate2><![CDATA[]]></comment_rate2>
			<comment_user0><![CDATA[]]></comment_user0>
			<comment_user1><![CDATA[]]></comment_user1>
			<comment_user2><![CDATA[]]></comment_user2>
			<commercial><![CDATA[0]]></commercial>
			<desp><![CDATA[C 系中阶 QWERTY 款式
诺基亚于 2010 年 4 ...]]></desp>
			<grade_avg><![CDATA[0]]></grade_avg>
			<nick><![CDATA[zheng570546321]]></nick>
			<nid><![CDATA[6701442378]]></nid>
			<people_num><![CDATA[0]]></people_num>
			<pict_url><![CDATA[i2/T1ivVKXaFlXXc8A6o._113005.jpg]]></pict_url>
			<pid><![CDATA[96312365]]></pid>
			<pidvidt><![CDATA[]]></pidvidt>
			<product_num><![CDATA[6125]]></product_num>
			<ratesum><![CDATA[5]]></ratesum>
			<reserve_price><![CDATA[1800]]></reserve_price>
			<seller_goodrate><![CDATA[10000]]></seller_goodrate>
			<title><![CDATA[<font color=red>Nokia</font>/诺基亚 C6]]></title>
			<total_sold_quantity><![CDATA[1]]></total_sold_quantity>
			<user_nid><![CDATA[346568297]]></user_nid>
			<user_strid><![CDATA[a8325eb660a709ee925bc8c3928845d2]]></user_strid>
		</fields>
		<property>
		</property>
		<sortExprValues>
			0.000210171
		</sortExprValues>
	</hit>
	<hit hash_id="0" docid="9168980">
		<fields>
			<biz30day><![CDATA[1]]></biz30day>
			<cat_id><![CDATA[1512]]></cat_id>
			<comment0><![CDATA[是行货，手机还不错。第一次上手诺基亚的手机，感觉...]]></comment0>
			<comment1><![CDATA[手机是好手机，掌柜是好掌柜，别的真的没什么了。]]></comment1>
			<comment2><![CDATA[东西很好！]]></comment2>
			<comment_num><![CDATA[4]]></comment_num>
			<comment_rate0><![CDATA[91]]></comment_rate0>
			<comment_rate1><![CDATA[11]]></comment_rate1>
			<comment_rate2><![CDATA[151]]></comment_rate2>
			<comment_user0><![CDATA[奇葩famliy]]></comment_user0>
			<comment_user1><![CDATA[寻找柳如是]]></comment_user1>
			<comment_user2><![CDATA[qq_190257]]></comment_user2>
			<commercial><![CDATA[0]]></commercial>
			<desp><![CDATA[新鲜出炉的C6靓照！C 系中阶 QWERTY 款式
...]]></desp>
			<grade_avg><![CDATA[0]]></grade_avg>
			<nick><![CDATA[yw09098]]></nick>
			<nid><![CDATA[6822469113]]></nid>
			<people_num><![CDATA[0]]></people_num>
			<pict_url><![CDATA[i3/T1y2lHXfFvXXb4jYza_120258.jpg]]></pict_url>
			<pid><![CDATA[96312365]]></pid>
			<pidvidt><![CDATA[]]></pidvidt>
			<product_num><![CDATA[6125]]></product_num>
			<ratesum><![CDATA[7]]></ratesum>
			<reserve_price><![CDATA[2198]]></reserve_price>
			<seller_goodrate><![CDATA[10000]]></seller_goodrate>
			<title><![CDATA[诺基亚/<font color=red>NOKIA</font> C6-00【大陆行货+全国联保+重庆实体店+发票+包邮】]]></title>
			<total_sold_quantity><![CDATA[6]]></total_sold_quantity>
			<user_nid><![CDATA[13793617]]></user_nid>
			<user_strid><![CDATA[01c2f7bce131ce8f2b051513cf9128a1]]></user_strid>
		</fields>
		<property>
		</property>
		<sortExprValues>
			0.000210171
		</sortExprValues>
	</hit>
	<hit hash_id="2" docid="9145695">
		<fields>
			<biz30day><![CDATA[1]]></biz30day>
			<cat_id><![CDATA[50003775]]></cat_id>
			<comment0><![CDATA[]]></comment0>
			<comment1><![CDATA[]]></comment1>
			<comment2><![CDATA[]]></comment2>
			<comment_num><![CDATA[0]]></comment_num>
			<comment_rate0><![CDATA[]]></comment_rate0>
			<comment_rate1><![CDATA[]]></comment_rate1>
			<comment_rate2><![CDATA[]]></comment_rate2>
			<comment_user0><![CDATA[]]></comment_user0>
			<comment_user1><![CDATA[]]></comment_user1>
			<comment_user2><![CDATA[]]></comment_user2>
			<commercial><![CDATA[0]]></commercial>
			<desp><![CDATA[<font color=red>Nokia</font>/诺基亚 <font color=red>Nokia</font> E75 黑色手机外壳全套 ...]]></desp>
			<grade_avg><![CDATA[0]]></grade_avg>
			<nick><![CDATA[ccue163]]></nick>
			<nid><![CDATA[7883573863]]></nid>
			<people_num><![CDATA[0]]></people_num>
			<pict_url><![CDATA[i4/T1nl4NXityXXaK5EoZ_034002.jpg]]></pict_url>
			<pid><![CDATA[-7883573863]]></pid>
			<pidvidt><![CDATA[]]></pidvidt>
			<product_num><![CDATA[0]]></product_num>
			<ratesum><![CDATA[6]]></ratesum>
			<reserve_price><![CDATA[55]]></reserve_price>
			<seller_goodrate><![CDATA[9898]]></seller_goodrate>
			<title><![CDATA[<font color=red>Nokia</font>/诺基亚 <font color=red>Nokia</font> E75 黑色手机外壳全套 带按键和拆机工具]]></title>
			<total_sold_quantity><![CDATA[0]]></total_sold_quantity>
			<user_nid><![CDATA[350400477]]></user_nid>
			<user_strid><![CDATA[4e1d00e029058aaa1e1d53e9abefcab4]]></user_strid>
		</fields>
		<property>
		</property>
		<sortExprValues>
			0.000210171
		</sortExprValues>
	</hit>
	<hit hash_id="2" docid="9139861">
		<fields>
			<biz30day><![CDATA[2]]></biz30day>
			<cat_id><![CDATA[50012584]]></cat_id>
			<comment0><![CDATA[不好意思这几天挺忙 确认晚了]]></comment0>
			<comment1><![CDATA[]]></comment1>
			<comment2><![CDATA[]]></comment2>
			<comment_num><![CDATA[1]]></comment_num>
			<comment_rate0><![CDATA[11]]></comment_rate0>
			<comment_rate1><![CDATA[]]></comment_rate1>
			<comment_rate2><![CDATA[]]></comment_rate2>
			<comment_user0><![CDATA[zgqskzhifubao]]></comment_user0>
			<comment_user1><![CDATA[]]></comment_user1>
			<comment_user2><![CDATA[]]></comment_user2>
			<commercial><![CDATA[0]]></commercial>
			<desp><![CDATA[<font color=red>Nokia</font>线充E65 E90 E95 N70充电器 N71 N72...]]></desp>
			<grade_avg><![CDATA[0]]></grade_avg>
			<nick><![CDATA[路过泉城]]></nick>
			<nid><![CDATA[6698634985]]></nid>
			<people_num><![CDATA[0]]></people_num>
			<pict_url><![CDATA[i2/T105xGXlNqXXbUsE6b_095528.jpg]]></pict_url>
			<pid><![CDATA[23615829]]></pid>
			<pidvidt><![CDATA[]]></pidvidt>
			<product_num><![CDATA[6405]]></product_num>
			<ratesum><![CDATA[9]]></ratesum>
			<reserve_price><![CDATA[8]]></reserve_price>
			<seller_goodrate><![CDATA[9587]]></seller_goodrate>
			<title><![CDATA[<font color=red>Nokia</font>线充E65 E90 E95 N70充电器 N71 N72线充 N73线充]]></title>
			<total_sold_quantity><![CDATA[6]]></total_sold_quantity>
			<user_nid><![CDATA[117818253]]></user_nid>
			<user_strid><![CDATA[19d4a11e148c07ee3288ab9d96378482]]></user_strid>
		</fields>
		<property>
		</property>
		<sortExprValues>
			0.000210171
		</sortExprValues>
	</hit>
	<hit hash_id="3" docid="9137643">
		<fields>
			<biz30day><![CDATA[1]]></biz30day>
			<cat_id><![CDATA[50010614]]></cat_id>
			<comment0><![CDATA[]]></comment0>
			<comment1><![CDATA[]]></comment1>
			<comment2><![CDATA[]]></comment2>
			<comment_num><![CDATA[0]]></comment_num>
			<comment_rate0><![CDATA[]]></comment_rate0>
			<comment_rate1><![CDATA[]]></comment_rate1>
			<comment_rate2><![CDATA[]]></comment_rate2>
			<comment_user0><![CDATA[]]></comment_user0>
			<comment_user1><![CDATA[]]></comment_user1>
			<comment_user2><![CDATA[]]></comment_user2>
			<commercial><![CDATA[0]]></commercial>
			<desp><![CDATA[产品描述：蓝特（LT)<font color=red>Nokia</font>/诺基亚 3610A/...]]></desp>
			<grade_avg><![CDATA[0]]></grade_avg>
			<nick><![CDATA[杨惠茸]]></nick>
			<nid><![CDATA[6817724341]]></nid>
			<people_num><![CDATA[0]]></people_num>
			<pict_url><![CDATA[i3/T16vtHXdhfXXakivg0_035148.jpg]]></pict_url>
			<pid><![CDATA[-6817724341]]></pid>
			<pidvidt><![CDATA[]]></pidvidt>
			<product_num><![CDATA[0]]></product_num>
			<ratesum><![CDATA[3]]></ratesum>
			<reserve_price><![CDATA[20]]></reserve_price>
			<seller_goodrate><![CDATA[9655]]></seller_goodrate>
			<title><![CDATA[蓝特（LT)<font color=red>Nokia</font>/诺基亚3610A/6555带座排线]]></title>
			<total_sold_quantity><![CDATA[1]]></total_sold_quantity>
			<user_nid><![CDATA[436855978]]></user_nid>
			<user_strid><![CDATA[4b9ad1c3c7f405847c2a47815ffc08c6]]></user_strid>
		</fields>
		<property>
		</property>
		<sortExprValues>
			0.000210171
		</sortExprValues>
	</hit>
	<hit hash_id="0" docid="9128114">
		<fields>
			<biz30day><![CDATA[1]]></biz30day>
			<cat_id><![CDATA[1512]]></cat_id>
			<comment0><![CDATA[这个颜色非常漂亮，喜欢，老板服务不错，还给我安装...]]></comment0>
			<comment1><![CDATA[颜色很好看，老板还送了好多礼品，还包邮！是我在...]]></comment1>
			<comment2><![CDATA[发货很快，手机很喜欢，这个颜色很不错！老板人很...]]></comment2>
			<comment_num><![CDATA[7]]></comment_num>
			<comment_rate0><![CDATA[4]]></comment_rate0>
			<comment_rate1><![CDATA[4]]></comment_rate1>
			<comment_rate2><![CDATA[4]]></comment_rate2>
			<comment_user0><![CDATA[亲爱的囡囡88]]></comment_user0>
			<comment_user1><![CDATA[晴天妹妹8]]></comment_user1>
			<comment_user2><![CDATA[狗儿们的窝]]></comment_user2>
			<commercial><![CDATA[0]]></commercial>
			<desp><![CDATA[----------------------------------------...]]></desp>
			<grade_avg><![CDATA[0]]></grade_avg>
			<nick><![CDATA[萍萍一站式购物]]></nick>
			<nid><![CDATA[6722451228]]></nid>
			<people_num><![CDATA[0]]></people_num>
			<pict_url><![CDATA[i3/T15rpDXelyXXbTA4gV_020655.jpg]]></pict_url>
			<pid><![CDATA[72468326]]></pid>
			<pidvidt><![CDATA[]]></pidvidt>
			<product_num><![CDATA[7382]]></product_num>
			<ratesum><![CDATA[9]]></ratesum>
			<reserve_price><![CDATA[1280]]></reserve_price>
			<seller_goodrate><![CDATA[9972]]></seller_goodrate>
			<title><![CDATA[【桔子通讯】<font color=red>Nokia</font>/诺基亚6700S/Slide 智能机港行 红蓝紫粉绿银]]></title>
			<total_sold_quantity><![CDATA[4]]></total_sold_quantity>
			<user_nid><![CDATA[279716453]]></user_nid>
			<user_strid><![CDATA[95604865bdd3499532e79eec4e399401]]></user_strid>
		</fields>
		<property>
		</property>
		<sortExprValues>
			0.000210171
		</sortExprValues>
	</hit>
	<hit hash_id="1" docid="9124486">
		<fields>
			<biz30day><![CDATA[1]]></biz30day>
			<cat_id><![CDATA[150704]]></cat_id>
			<comment0><![CDATA[做工还成。但是的确偏大不少]]></comment0>
			<comment1><![CDATA[很不错的宝贝 很满意]]></comment1>
			<comment2><![CDATA[赞一个]]></comment2>
			<comment_num><![CDATA[3]]></comment_num>
			<comment_rate0><![CDATA[501]]></comment_rate0>
			<comment_rate1><![CDATA[4]]></comment_rate1>
			<comment_rate2><![CDATA[91]]></comment_rate2>
			<comment_user0><![CDATA[gegega]]></comment_user0>
			<comment_user1><![CDATA[熊熊爱吃饭]]></comment_user1>
			<comment_user2><![CDATA[小晴1799]]></comment_user2>
			<commercial><![CDATA[0]]></commercial>
			<desp><![CDATA[----------------------------------------...]]></desp>
			<grade_avg><![CDATA[0]]></grade_avg>
			<nick><![CDATA[baiyun数码]]></nick>
			<nid><![CDATA[6219039792]]></nid>
			<people_num><![CDATA[0]]></people_num>
			<pict_url><![CDATA[i1/T1RfpFXaFjXXbqLRM3_050811.jpg]]></pict_url>
			<pid><![CDATA[73686392]]></pid>
			<pidvidt><![CDATA[]]></pidvidt>
			<product_num><![CDATA[662]]></product_num>
			<ratesum><![CDATA[9]]></ratesum>
			<reserve_price><![CDATA[47]]></reserve_price>
			<seller_goodrate><![CDATA[10000]]></seller_goodrate>
			<title><![CDATA[澳洲PDair炫彩多色 <font color=red>Nokia</font> n97mini 硅胶套 品质之选 红色]]></title>
			<total_sold_quantity><![CDATA[9]]></total_sold_quantity>
			<user_nid><![CDATA[212478869]]></user_nid>
			<user_strid><![CDATA[f3327a1de93bee4398481d69f08b08e3]]></user_strid>
		</fields>
		<property>
		</property>
		<sortExprValues>
			0.000210171
		</sortExprValues>
	</hit>
	<hit hash_id="0" docid="9122611">
		<fields>
			<biz30day><![CDATA[2]]></biz30day>
			<cat_id><![CDATA[50012587]]></cat_id>
			<comment0><![CDATA[老板很厚道...]]></comment0>
			<comment1><![CDATA[老板依然厚道！]]></comment1>
			<comment2><![CDATA[]]></comment2>
			<comment_num><![CDATA[2]]></comment_num>
			<comment_rate0><![CDATA[11]]></comment_rate0>
			<comment_rate1><![CDATA[11]]></comment_rate1>
			<comment_rate2><![CDATA[]]></comment_rate2>
			<comment_user0><![CDATA[獨y無贰]]></comment_user0>
			<comment_user1><![CDATA[獨y無贰]]></comment_user1>
			<comment_user2><![CDATA[]]></comment_user2>
			<commercial><![CDATA[0]]></commercial>
			<desp><![CDATA[使用说明：
1、第一步清洁屏幕，用附赠的...]]></desp>
			<grade_avg><![CDATA[0]]></grade_avg>
			<nick><![CDATA[讨厌平安夜]]></nick>
			<nid><![CDATA[6818006015]]></nid>
			<people_num><![CDATA[0]]></people_num>
			<pict_url><![CDATA[i6/T1tUppXh0aXXbLmTo8_102003.jpg]]></pict_url>
			<pid><![CDATA[80427683]]></pid>
			<pidvidt><![CDATA[]]></pidvidt>
			<product_num><![CDATA[0]]></product_num>
			<ratesum><![CDATA[3]]></ratesum>
			<reserve_price><![CDATA[68]]></reserve_price>
			<seller_goodrate><![CDATA[10000]]></seller_goodrate>
			<title><![CDATA[阿迪普手机膜专家-<font color=red>NOKIA</font>诺基亚 5230 幻彩钻石系列套装]]></title>
			<total_sold_quantity><![CDATA[2]]></total_sold_quantity>
			<user_nid><![CDATA[56983709]]></user_nid>
			<user_strid><![CDATA[71f84a0915e9062e30df53c960641f21]]></user_strid>
		</fields>
		<property>
		</property>
		<sortExprValues>
			0.000210171
		</sortExprValues>
	</hit>
</hits>
<AggregateResults>
</AggregateResults>
<Error>
	<ErrorCode>0</ErrorCode>
	<ErrorDescription></ErrorDescription>
</Error>
</Root>
'''

    xmlstr1 = '''<?xml version="1.0" encoding="UTF-8"?>
<Root>
<TotalTime>0.055</TotalTime>
<hits numhits="10" totalhits="117892">
	<hit hash_id="3" docid="9212704">
		<fields>
			<biz30day><![CDATA[1]]></biz30day>
			<cat_id><![CDATA[1512]]></cat_id>
			<comment0><![CDATA[超级喜欢~~~速度还很快。超值]]></comment0>
			<comment1><![CDATA[货很正。]]></comment1>
			<comment2><![CDATA[]]></comment2>
			<comment_num><![CDATA[2]]></comment_num>
			<comment_rate0><![CDATA[4]]></comment_rate0>
			<comment_rate1><![CDATA[41]]></comment_rate1>
			<comment_rate2><![CDATA[]]></comment_rate2>
			<comment_user0><![CDATA[1157saygoodbye]]></comment_user0>
			<comment_user1><![CDATA[changzheng92]]></comment_user1>
			<comment_user2><![CDATA[]]></comment_user2>
			<commercial><![CDATA[0]]></commercial>
			<desp><![CDATA[產品規格
顯示所有 隱藏所有
手機功能、電...]]></desp>
			<grade_avg><![CDATA[0]]></grade_avg>
			<nick><![CDATA[zpin10]]></nick>
			<nid><![CDATA[4052667480]]></nid>
			<people_num><![CDATA[0]]></people_num>
			<pict_url><![CDATA[i8/T1F18AXm4jXXbkT1c0_034730.jpg]]></pict_url>
			<pid><![CDATA[78348588]]></pid>
			<pidvidt><![CDATA[]]></pidvidt>
			<product_num><![CDATA[6201]]></product_num>
			<ratesum><![CDATA[9]]></ratesum>
			<reserve_price><![CDATA[2020]]></reserve_price>
			<seller_goodrate><![CDATA[9993]]></seller_goodrate>
			<title><![CDATA[*五年钻石好店三包赔付保障*<font color=red>Nokia</font>/诺基亚 X6]]></title>
			<total_sold_quantity><![CDATA[11]]></total_sold_quantity>
			<user_nid><![CDATA[22839402]]></user_nid>
			<user_strid><![CDATA[cfc07f8231e153dbdbfe872bf9f41ff0]]></user_strid>
		</fields>
		<property>
		</property>
		<sortExprValues>
			0.000210171
		</sortExprValues>
	</hit>
	<hit hash_id="0" docid="9190361">
		<fields>
			<biz30day><![CDATA[1]]></biz30day>
			<cat_id><![CDATA[50012584]]></cat_id>
			<comment0><![CDATA[给妹妹买的，她说不错，和在街上买的价格差不多，...]]></comment0>
			<comment1><![CDATA[宝贝都很不错,买家态度老好了,以后有需要还会继续...]]></comment1>
			<comment2><![CDATA[好使 没坏 就是有点贵]]></comment2>
			<comment_num><![CDATA[6]]></comment_num>
			<comment_rate0><![CDATA[501]]></comment_rate0>
			<comment_rate1><![CDATA[41]]></comment_rate1>
			<comment_rate2><![CDATA[41]]></comment_rate2>
			<comment_user0><![CDATA[空瓶子zch]]></comment_user0>
			<comment_user1><![CDATA[huihui_katrina]]></comment_user1>
			<comment_user2><![CDATA[showwinter]]></comment_user2>
			<commercial><![CDATA[0]]></commercial>
			<desp><![CDATA[<font color=red>Nokia</font>线充E65 E90 E95 N70充电器 N71 N72线充]]></desp>
			<grade_avg><![CDATA[0]]></grade_avg>
			<nick><![CDATA[taotao8601]]></nick>
			<nid><![CDATA[4042745681]]></nid>
			<people_num><![CDATA[0]]></people_num>
			<pict_url><![CDATA[i8/T1b0JBXlhyXXXSaBs2_044823.jpg]]></pict_url>
			<pid><![CDATA[23620066]]></pid>
			<pidvidt><![CDATA[]]></pidvidt>
			<product_num><![CDATA[2806]]></product_num>
			<ratesum><![CDATA[11]]></ratesum>
			<reserve_price><![CDATA[8]]></reserve_price>
			<seller_goodrate><![CDATA[9730]]></seller_goodrate>
			<title><![CDATA[<font color=red>Nokia</font>线充E65 E90 E95 N70充电器 N71 N72线充 N73线充]]></title>
			<total_sold_quantity><![CDATA[72]]></total_sold_quantity>
			<user_nid><![CDATA[74665395]]></user_nid>
			<user_strid><![CDATA[561198dfa4cd940c717cc84ca2b5fbd8]]></user_strid>
		</fields>
		<property>
		</property>
		<sortExprValues>
			0.000210171
		</sortExprValues>
	</hit>
	<hit hash_id="2" docid="9176120">
		<fields>
			<biz30day><![CDATA[1]]></biz30day>
			<cat_id><![CDATA[1512]]></cat_id>
			<comment0><![CDATA[]]></comment0>
			<comment1><![CDATA[]]></comment1>
			<comment2><![CDATA[]]></comment2>
			<comment_num><![CDATA[0]]></comment_num>
			<comment_rate0><![CDATA[]]></comment_rate0>
			<comment_rate1><![CDATA[]]></comment_rate1>
			<comment_rate2><![CDATA[]]></comment_rate2>
			<comment_user0><![CDATA[]]></comment_user0>
			<comment_user1><![CDATA[]]></comment_user1>
			<comment_user2><![CDATA[]]></comment_user2>
			<commercial><![CDATA[0]]></commercial>
			<desp><![CDATA[C 系中阶 QWERTY 款式
诺基亚于 2010 年 4 ...]]></desp>
			<grade_avg><![CDATA[0]]></grade_avg>
			<nick><![CDATA[zheng570546321]]></nick>
			<nid><![CDATA[6701442378]]></nid>
			<people_num><![CDATA[0]]></people_num>
			<pict_url><![CDATA[i2/T1ivVKXaFlXXc8A6o._113005.jpg]]></pict_url>
			<pid><![CDATA[96312365]]></pid>
			<pidvidt><![CDATA[]]></pidvidt>
			<product_num><![CDATA[6125]]></product_num>
			<ratesum><![CDATA[5]]></ratesum>
			<reserve_price><![CDATA[1800]]></reserve_price>
			<seller_goodrate><![CDATA[10000]]></seller_goodrate>
			<title><![CDATA[<font color=red>Nokia</font>/诺基亚 C6]]></title>
			<total_sold_quantity><![CDATA[1]]></total_sold_quantity>
			<user_nid><![CDATA[346568297]]></user_nid>
			<user_strid><![CDATA[a8325eb660a709ee925bc8c3928845d2]]></user_strid>
		</fields>
		<property>
		</property>
		<sortExprValues>
			0.000210171
		</sortExprValues>
	</hit>
	<hit hash_id="0" docid="9168980">
		<fields>
			<biz30day><![CDATA[1]]></biz30day>
			<cat_id><![CDATA[1512]]></cat_id>
			<comment0><![CDATA[是行货，手机还不错。第一次上手诺基亚的手机，感觉...]]></comment0>
			<comment1><![CDATA[手机是好手机，掌柜是好掌柜，别的真的没什么了。]]></comment1>
			<comment2><![CDATA[东西很好！]]></comment2>
			<comment_num><![CDATA[4]]></comment_num>
			<comment_rate0><![CDATA[91]]></comment_rate0>
			<comment_rate1><![CDATA[11]]></comment_rate1>
			<comment_rate2><![CDATA[151]]></comment_rate2>
			<comment_user0><![CDATA[奇葩famliy]]></comment_user0>
			<comment_user1><![CDATA[寻找柳如是]]></comment_user1>
			<comment_user2><![CDATA[qq_190257]]></comment_user2>
			<commercial><![CDATA[0]]></commercial>
			<desp><![CDATA[新鲜出炉的C6靓照！C 系中阶 QWERTY 款式
...]]></desp>
			<grade_avg><![CDATA[0]]></grade_avg>
			<nick><![CDATA[yw09098]]></nick>
			<nid><![CDATA[6822469113]]></nid>
			<people_num><![CDATA[0]]></people_num>
			<pict_url><![CDATA[i3/T1y2lHXfFvXXb4jYza_120258.jpg]]></pict_url>
			<pid><![CDATA[96312365]]></pid>
			<pidvidt><![CDATA[]]></pidvidt>
			<product_num><![CDATA[6125]]></product_num>
			<ratesum><![CDATA[7]]></ratesum>
			<reserve_price><![CDATA[2198]]></reserve_price>
			<seller_goodrate><![CDATA[10000]]></seller_goodrate>
			<title><![CDATA[诺基亚/<font color=red>NOKIA</font> C6-00【大陆行货+全国联保+重庆实体店+发票+包邮】]]></title>
			<total_sold_quantity><![CDATA[6]]></total_sold_quantity>
			<user_nid><![CDATA[13793617]]></user_nid>
			<user_strid><![CDATA[01c2f7bce131ce8f2b051513cf9128a1]]></user_strid>
		</fields>
		<property>
		</property>
		<sortExprValues>
			0.000210171
		</sortExprValues>
	</hit>
	<hit hash_id="2" docid="9145695">
		<fields>
			<biz30day><![CDATA[1]]></biz30day>
			<cat_id><![CDATA[50003775]]></cat_id>
			<comment0><![CDATA[]]></comment0>
			<comment1><![CDATA[]]></comment1>
			<comment2><![CDATA[]]></comment2>
			<comment_num><![CDATA[0]]></comment_num>
			<comment_rate0><![CDATA[]]></comment_rate0>
			<comment_rate1><![CDATA[]]></comment_rate1>
			<comment_rate2><![CDATA[]]></comment_rate2>
			<comment_user0><![CDATA[]]></comment_user0>
			<comment_user1><![CDATA[]]></comment_user1>
			<comment_user2><![CDATA[]]></comment_user2>
			<commercial><![CDATA[0]]></commercial>
			<desp><![CDATA[<font color=red>Nokia</font>/诺基亚 <font color=red>Nokia</font> E75 黑色手机外壳全套 ...]]></desp>
			<grade_avg><![CDATA[0]]></grade_avg>
			<nick><![CDATA[ccue163]]></nick>
			<nid><![CDATA[7883573863]]></nid>
			<people_num><![CDATA[0]]></people_num>
			<pict_url><![CDATA[i4/T1nl4NXityXXaK5EoZ_034002.jpg]]></pict_url>
			<pid><![CDATA[-7883573863]]></pid>
			<pidvidt><![CDATA[]]></pidvidt>
			<product_num><![CDATA[0]]></product_num>
			<ratesum><![CDATA[6]]></ratesum>
			<reserve_price><![CDATA[55]]></reserve_price>
			<seller_goodrate><![CDATA[9898]]></seller_goodrate>
			<title><![CDATA[<font color=red>Nokia</font>/诺基亚 <font color=red>Nokia</font> E75 黑色手机外壳全套 带按键和拆机工具]]></title>
			<total_sold_quantity><![CDATA[0]]></total_sold_quantity>
			<user_nid><![CDATA[350400477]]></user_nid>
			<user_strid><![CDATA[4e1d00e029058aaa1e1d53e9abefcab4]]></user_strid>
		</fields>
		<property>
		</property>
		<sortExprValues>
			0.000210171
		</sortExprValues>
	</hit>
	<hit hash_id="2" docid="9139861">
		<fields>
			<biz30day><![CDATA[2]]></biz30day>
			<cat_id><![CDATA[50012584]]></cat_id>
			<comment0><![CDATA[不好意思这几天挺忙 确认晚了]]></comment0>
			<comment1><![CDATA[]]></comment1>
			<comment2><![CDATA[]]></comment2>
			<comment_num><![CDATA[1]]></comment_num>
			<comment_rate0><![CDATA[11]]></comment_rate0>
			<comment_rate1><![CDATA[]]></comment_rate1>
			<comment_rate2><![CDATA[]]></comment_rate2>
			<comment_user0><![CDATA[zgqskzhifubao]]></comment_user0>
			<comment_user1><![CDATA[]]></comment_user1>
			<comment_user2><![CDATA[]]></comment_user2>
			<commercial><![CDATA[0]]></commercial>
			<desp><![CDATA[<font color=red>Nokia</font>线充E65 E90 E95 N70充电器 N71 N72...]]></desp>
			<grade_avg><![CDATA[0]]></grade_avg>
			<nick><![CDATA[路过泉城]]></nick>
			<nid><![CDATA[6698634985]]></nid>
			<people_num><![CDATA[0]]></people_num>
			<pict_url><![CDATA[i2/T105xGXlNqXXbUsE6b_095528.jpg]]></pict_url>
			<pid><![CDATA[23615829]]></pid>
			<pidvidt><![CDATA[]]></pidvidt>
			<product_num><![CDATA[6405]]></product_num>
			<ratesum><![CDATA[9]]></ratesum>
			<reserve_price><![CDATA[8]]></reserve_price>
			<seller_goodrate><![CDATA[9587]]></seller_goodrate>
			<title><![CDATA[<font color=red>Nokia</font>线充E65 E90 E95 N70充电器 N71 N72线充 N73线充]]></title>
			<total_sold_quantity><![CDATA[6]]></total_sold_quantity>
			<user_nid><![CDATA[117818253]]></user_nid>
			<user_strid><![CDATA[19d4a11e148c07ee3288ab9d96378482]]></user_strid>
		</fields>
		<property>
		</property>
		<sortExprValues>
			0.000210171
		</sortExprValues>
	</hit>
	<hit hash_id="3" docid="9137643">
		<fields>
			<biz30day><![CDATA[1]]></biz30day>
			<cat_id><![CDATA[50010614]]></cat_id>
			<comment0><![CDATA[]]></comment0>
			<comment1><![CDATA[]]></comment1>
			<comment2><![CDATA[]]></comment2>
			<comment_num><![CDATA[0]]></comment_num>
			<comment_rate0><![CDATA[]]></comment_rate0>
			<comment_rate1><![CDATA[]]></comment_rate1>
			<comment_rate2><![CDATA[]]></comment_rate2>
			<comment_user0><![CDATA[]]></comment_user0>
			<comment_user1><![CDATA[]]></comment_user1>
			<comment_user2><![CDATA[]]></comment_user2>
			<commercial><![CDATA[0]]></commercial>
			<desp><![CDATA[产品描述：蓝特（LT)<font color=red>Nokia</font>/诺基亚 3610A/...]]></desp>
			<grade_avg><![CDATA[0]]></grade_avg>
			<nick><![CDATA[杨惠茸]]></nick>
			<nid><![CDATA[6817724341]]></nid>
			<people_num><![CDATA[0]]></people_num>
			<pict_url><![CDATA[i3/T16vtHXdhfXXakivg0_035148.jpg]]></pict_url>
			<pid><![CDATA[-6817724341]]></pid>
			<pidvidt><![CDATA[]]></pidvidt>
			<product_num><![CDATA[0]]></product_num>
			<ratesum><![CDATA[3]]></ratesum>
			<reserve_price><![CDATA[20]]></reserve_price>
			<seller_goodrate><![CDATA[9655]]></seller_goodrate>
			<title><![CDATA[蓝特（LT)<font color=red>Nokia</font>/诺基亚3610A/6555带座排线]]></title>
			<total_sold_quantity><![CDATA[1]]></total_sold_quantity>
			<user_nid><![CDATA[436855978]]></user_nid>
			<user_strid><![CDATA[4b9ad1c3c7f405847c2a47815ffc08c6]]></user_strid>
		</fields>
		<property>
		</property>
		<sortExprValues>
			0.000210171
		</sortExprValues>
	</hit>
	<hit hash_id="0" docid="9128114">
		<fields>
			<biz30day><![CDATA[1]]></biz30day>
			<cat_id><![CDATA[1512]]></cat_id>
			<comment0><![CDATA[这个颜色非常漂亮，喜欢，老板服务不错，还给我安装...]]></comment0>
			<comment1><![CDATA[颜色很好看，老板还送了好多礼品，还包邮！是我在...]]></comment1>
			<comment2><![CDATA[发货很快，手机很喜欢，这个颜色很不错！老板人很...]]></comment2>
			<comment_num><![CDATA[7]]></comment_num>
			<comment_rate0><![CDATA[4]]></comment_rate0>
			<comment_rate1><![CDATA[4]]></comment_rate1>
			<comment_rate2><![CDATA[4]]></comment_rate2>
			<comment_user0><![CDATA[亲爱的囡囡88]]></comment_user0>
			<comment_user1><![CDATA[晴天妹妹8]]></comment_user1>
			<comment_user2><![CDATA[狗儿们的窝]]></comment_user2>
			<commercial><![CDATA[0]]></commercial>
			<desp><![CDATA[----------------------------------------...]]></desp>
			<grade_avg><![CDATA[0]]></grade_avg>
			<nick><![CDATA[萍萍一站式购物]]></nick>
			<nid><![CDATA[6722451228]]></nid>
			<people_num><![CDATA[0]]></people_num>
			<pict_url><![CDATA[i3/T15rpDXelyXXbTA4gV_020655.jpg]]></pict_url>
			<pid><![CDATA[72468326]]></pid>
			<pidvidt><![CDATA[]]></pidvidt>
			<product_num><![CDATA[7382]]></product_num>
			<ratesum><![CDATA[9]]></ratesum>
			<reserve_price><![CDATA[1280]]></reserve_price>
			<seller_goodrate><![CDATA[9972]]></seller_goodrate>
			<title><![CDATA[【桔子通讯】<font color=red>Nokia</font>/诺基亚6700S/Slide 智能机港行 红蓝紫粉绿银]]></title>
			<total_sold_quantity><![CDATA[4]]></total_sold_quantity>
			<user_nid><![CDATA[279716453]]></user_nid>
			<user_strid><![CDATA[95604865bdd3499532e79eec4e399401]]></user_strid>
		</fields>
		<property>
		</property>
		<sortExprValues>
			0.000210171
		</sortExprValues>
	</hit>
	<hit hash_id="1" docid="9124486">
		<fields>
			<biz30day><![CDATA[1]]></biz30day>
			<cat_id><![CDATA[150704]]></cat_id>
			<comment0><![CDATA[做工还成。但是的确偏大不少]]></comment0>
			<comment1><![CDATA[很不错的宝贝 很满意]]></comment1>
			<comment2><![CDATA[赞一个]]></comment2>
			<comment_num><![CDATA[3]]></comment_num>
			<comment_rate0><![CDATA[501]]></comment_rate0>
			<comment_rate1><![CDATA[4]]></comment_rate1>
			<comment_rate2><![CDATA[91]]></comment_rate2>
			<comment_user0><![CDATA[gegega]]></comment_user0>
			<comment_user1><![CDATA[熊熊爱吃饭]]></comment_user1>
			<comment_user2><![CDATA[小晴1799]]></comment_user2>
			<commercial><![CDATA[0]]></commercial>
			<desp><![CDATA[----------------------------------------...]]></desp>
			<grade_avg><![CDATA[0]]></grade_avg>
			<nick><![CDATA[baiyun数码]]></nick>
			<nid><![CDATA[6219039792]]></nid>
			<people_num><![CDATA[0]]></people_num>
			<pict_url><![CDATA[i1/T1RfpFXaFjXXbqLRM3_050811.jpg]]></pict_url>
			<pid><![CDATA[73686392]]></pid>
			<pidvidt><![CDATA[]]></pidvidt>
			<product_num><![CDATA[662]]></product_num>
			<ratesum><![CDATA[9]]></ratesum>
			<reserve_price><![CDATA[47]]></reserve_price>
			<seller_goodrate><![CDATA[10000]]></seller_goodrate>
			<title><![CDATA[澳洲PDair炫彩多色 <font color=red>Nokia</font> n97mini 硅胶套 品质之选 红色]]></title>
			<total_sold_quantity><![CDATA[9]]></total_sold_quantity>
			<user_nid><![CDATA[212478869]]></user_nid>
			<user_strid><![CDATA[f3327a1de93bee4398481d69f08b08e3]]></user_strid>
		</fields>
		<property>
		</property>
		<sortExprValues>
			0.000210171
		</sortExprValues>
	</hit>
	<hit hash_id="0" docid="9122611">
		<fields>
			<biz30day><![CDATA[2]]></biz30day>
			<cat_id><![CDATA[50012587]]></cat_id>
			<comment0><![CDATA[老板很厚道...]]></comment0>
			<comment1><![CDATA[老板依然厚道！]]></comment1>
			<comment2><![CDATA[]]></comment2>
			<comment_num><![CDATA[2]]></comment_num>
			<comment_rate0><![CDATA[11]]></comment_rate0>
			<comment_rate1><![CDATA[11]]></comment_rate1>
			<comment_rate2><![CDATA[]]></comment_rate2>
			<comment_user0><![CDATA[獨y無贰]]></comment_user0>
			<comment_user1><![CDATA[獨y無贰]]></comment_user1>
			<comment_user2><![CDATA[]]></comment_user2>
			<commercial><![CDATA[0]]></commercial>
			<desp><![CDATA[使用说明：
1、第一步清洁屏幕，用附赠的...]]></desp>
			<grade_avg><![CDATA[0]]></grade_avg>
			<nick><![CDATA[讨厌平安夜]]></nick>
			<nid><![CDATA[6818006011]]></nid>
			<people_num><![CDATA[0]]></people_num>
			<pict_url><![CDATA[i6/T1tUppXh0aXXbLmTo8_102003.jpg]]></pict_url>
			<pid><![CDATA[80427683]]></pid>
			<pidvidt><![CDATA[]]></pidvidt>
			<product_num><![CDATA[0]]></product_num>
			<ratesum><![CDATA[3]]></ratesum>
			<reserve_price><![CDATA[68]]></reserve_price>
			<seller_goodrate><![CDATA[10000]]></seller_goodrate>
			<title><![CDATA[阿迪普手机膜专家-<font color=red>NOKIA</font>诺基亚 5230 幻彩钻石系列套装]]></title>
			<total_sold_quantity><![CDATA[2]]></total_sold_quantity>
			<user_nid><![CDATA[56983709]]></user_nid>
			<user_strid><![CDATA[71f84a0915e9062e30df53c960641f21]]></user_strid>
		</fields>
		<property>
		</property>
		<sortExprValues>
			0.000210171
		</sortExprValues>
	</hit>
</hits>
<AggregateResults>
</AggregateResults>
<Error>
	<ErrorCode>0</ErrorCode>
	<ErrorDescription></ErrorDescription>
</Error>
</Root>
'''




    if len(sys.argv) < 3:
        print >> sys.stderr, 'Usage: %s <servie_name> <queryfile>'
        sys.exit(1)

    srvn = sys.argv[1]
    qfn  = sys.argv[2]
    
    cmper = QueryResComp(srvn)

    f = open(qfn)
    try:
        for qstr in f:

            cmper.fetchResult(qstr)
            # if not cmper.isEqual():
                # print qstr
            break
    finally:
        f.close()

    

