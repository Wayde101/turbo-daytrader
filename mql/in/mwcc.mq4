#property copyright "Copyright (c) 2011, TingYu"
#property link      "http://www.17forex.com"

#property indicator_chart_window

// global object
// MW / MW_up / MW_down 

extern int g_cc_min_k=11,
	   g_mw_width=55;    // global Window Width

int init()
{
  return(0);
}

int start()
{
  MW_set(Period(),Yellow,g_mw_width);
  MW_prop_set();
  CC_set(Period(),get_nearest_zpoint(),g_cc_min_k);
  CC_prop_set();
  return(0);
}

// ret code: 
// 0: 成功的旗形
// 1: 旗形雏形不够 least k线根数。 不进行旗形测试
// 2: 当 a点时间大于 b 点的时候，旗形失败. 并且清除之. ret code : 2
// 3: MW最近的顶点和CC的顶点不一致，说明,MW的顶点已经发生变化，rm_obj(CC).
int CC_set(int tf,string zpoint,int least)
{
  int flag_len = iBarShift(NULL,tf,ObjectGet(zpoint,OBJPROP_TIME1));
  if ( flag_len < least ) {
    rm_obj("CC","MW new zpoint updated. remove_if CC");
    return(1);
  }

  datetime z1_time = ObjectGet(zpoint,OBJPROP_TIME1),
	   za_time,
           zb_time;

  double   z1_price= ObjectGet(zpoint,OBJPROP_PRICE1),
	   za_price,
	   zb_price,
	   swa_price = 0,
	   swb_price = 0;

  string   cc_desc = "";


  if(ObjectFind("CC") == -1 ) {
    za_time  = z1_time;
    za_price = z1_price;
    zb_price = iClose(NULL,tf,1);
    zb_time  = iTime(NULL,tf,1);

    ObjectCreate("CC",OBJ_CHANNEL,0,z1_time,z1_price,zb_time,zb_price,za_time,za_price);
    // 取 b 点的时间. 为最近一个 bar 的最高点.
    ObjectSet("CC",OBJPROP_COLOR,Red);
    ObjectSet("CC",OBJPROP_TIME2,zb_time);
    ObjectSet("CC",OBJPROP_PRICE2,zb_price);
  } else {
    za_time  = ObjectGet("CC",OBJPROP_TIME3);
    za_price = ObjectGet("CC",OBJPROP_PRICE3);
    zb_time  = ObjectGet("CC",OBJPROP_TIME2);
    zb_price = ObjectGet("CC",OBJPROP_PRICE2);
  }
  

  // 选举 a 点. 
  // 选举 b 点. 在 0 点和当前价格点位中间选取 
  //     diff 最大(上升旗形的时候)或者最小(下降旗型的时候)的点.
  // sfa/sfb  : shift_a shift_b
  for(int i=0; i < flag_len; i++) {
    double width = GetChannelDist("CC");
    double sfb_price = ObjectGetValueByShift("CC",i),
	   sfa_price,
	   mva_price,
           mvb_price,
	   factor=1;

    if(zpoint == "MW_up") {
      factor = 1;
      mvb_price = iHigh(NULL,tf,i);
      mva_price = iLow(NULL,tf,i);
    } else {
      factor = -1;
      mvb_price = iLow(NULL,tf,i);
      mva_price = iHigh(NULL,tf,i);
    }

    
    sfa_price = sfb_price - (factor * width);

    if(0 < (factor * (mvb_price - sfb_price))) {
       zb_price  = mvb_price;
       zb_time   = iTime(NULL,tf,i);
    }
    
    if(0 > (factor * (mva_price - sfa_price))) {
      za_price   =  mva_price;
      za_time    = iTime(NULL,tf,i);
    }
    
    ObjectSet("CC",OBJPROP_COLOR,Blue);
    ObjectSet("CC",OBJPROP_TIME2,zb_time);
    ObjectSet("CC",OBJPROP_PRICE2,zb_price);
    ObjectSet("CC",OBJPROP_TIME3,za_time);
    ObjectSet("CC",OBJPROP_PRICE3,za_price);
  }

  // 当 a点时间大于 b 点的时候，旗形失败. 并且清除之. ret code : 2
  if(za_time > zb_time ) {
    rm_obj("CC","a point time great than b point aaaaaaaa");
    return(2);
  }

  return(0);

  // 选举 a 点. a
}

double GetChannelDist(string cn)
{
  // get A point 's shift number
  int    s3  = iBarShift(Symbol(),Period(),ObjectGet(cn,OBJPROP_TIME3)); 
  // get A point 's price.
  double p3  = ObjectGet(cn,OBJPROP_PRICE3);
  // get CN channel's price value by A point's shift number.
  double sp1 = ObjectGetValueByShift(cn,s3);
   return(MathAbs(sp1-p3));
}

int MW_set(int tf,int Color ,int n)
{
  int ret_code = Color;
  if(ObjectFind("MW") == -1) {
    ObjectCreate("MW",
		 OBJ_RECTANGLE,
		 0,
		 Time[n],
		 High[iHighest(NULL,tf,MODE_HIGH,n,0)],
		 Time[0],
		 Low[iLowest(NULL,tf,MODE_LOW,n,0)]);
    ObjectSet("MW",OBJPROP_COLOR,Color);
    ObjectCreate("MW_up",
		 OBJ_ARROW,
		 0,
		 Time[iHighest(NULL,tf,MODE_HIGH,n,0)],
		 High[iHighest(NULL,tf,MODE_HIGH,n,0)]);

    ObjectCreate("MW_down",
		 OBJ_ARROW,
		 0,
		 Time[iLowest(NULL,tf,MODE_HIGH,n,0)],
		 Low[iLowest(NULL,tf,MODE_HIGH,n,0)]);

    ObjectSet("MW_down",OBJPROP_ARROWCODE,242);
  }
  if(ObjectGet("MW",OBJPROP_COLOR) == Yellow) {
    int HighestN=iHighest(NULL,tf,MODE_HIGH,n,0);
    int LowestN =iLowest(NULL,tf,MODE_LOW,n,0);

    ObjectSet("MW",OBJPROP_TIME1,Time[n]);
    ObjectSet("MW",OBJPROP_PRICE1,High[HighestN]);
    ObjectSet("MW",OBJPROP_TIME2,Time[0]);
    ObjectSet("MW",OBJPROP_PRICE2,Low[LowestN]);

    ObjectSet("MW_up",
	      OBJPROP_TIME1,
	      Time[HighestN]);
    ObjectSet("MW_up",
	      OBJPROP_PRICE1,
	      High[HighestN]);

    ObjectSet("MW_down",
	      OBJPROP_TIME1,
	      Time[LowestN]);
    ObjectSet("MW_down",
	      OBJPROP_PRICE1,
	      Low[LowestN]);

    ret_code = 0 ;    // 0 : mw is 
    ret_code = Yellow;
  }

  okv("MW_WIDTH",n);
  okv("MW_NAME","MW");
  return(ret_code);
}

void MW_prop_set() {
  string mw_desc = "";

  if(ObjectFind("MW") == -1) {
    return;
  }

  // ATR status part.  取最近14天的 ATR 值.
  mw_desc = StringConcatenate("atr55=" , iATR(NULL,0,55,0));
  ObjectSetText("MW",mw_desc,10,"Times New Roman",Green);
}

void CC_prop_set() {
  string cc_desc =  "";
  string zpoint  =  get_nearest_zpoint();
  double width   =  GetChannelDist("CC");
  int	 factor  = 1;
  
  if(ObjectFind("CC") == -1) {
    return(1);
  }
  
  if(zpoint == "MW_down") {
    factor = -1; 
  }
  
  cc_desc = StringConcatenate("CCDIST=",width,";",
			      "CC0P=",ObjectGetValueByShift("CC",0), ";",
			      "CC1P=",ObjectGetValueByShift("CC",0) - width * factor, ";" ,
			      "ZPOINT=",zpoint);
  ObjectSetText("CC",cc_desc,10,"Times New Roman",Green);
  return;
}


string get_nearest_zpoint()
{
  string ret="none";
  if(ObjectGet("MW_up",OBJPROP_TIME1) > ObjectGet("MW_down",OBJPROP_TIME1)) {
    ret="MW_up";
  } else {
    ret="MW_down";
  }
  return(ret);
}

int rm_obj(string objname,string rmsg="")
{
  if(ObjectFind(objname) == -1) {
    d(StringConcatenate("no [",objname,"]","exists:",rmsg));
    return(-1);
  }
  ObjectDelete(objname);
  d(StringConcatenate("remove[",objname,"]",rmsg));
  return(0);
}

void okv(string k, string v) {
  //Print("jSend Zero: do not set [", k ,"]","  [",v,"]");
  return;
}

//+------------------------------------------------------------------+
string d(string s1,
	 string s2="",
	 string s3="",
	 string s4="",
	 string s5="",
	 string s6="",
	 string s7="",
	 string s8="",
	 string s9="",
	 string s10="")  {
//+------------------------------------------------------------------+
  string out = StringTrimRight(StringConcatenate(s1, " ", 
						 s2, " ", 
						 s3, " ", 
						 s4, " ", 
						 s5, " ", 
						 s6, " ", 
						 s7, " ", 
						 s8, " ",
						 s9, " ",
						 s10," "));
  Print(out);
  //  int h = FileOpen("debug.txt",FILE_CSV|FILE_READ|FILE_WRITE,'~');
  //  FileSeek(h,0,SEEK_END);
  //  FileWrite(h,out);
  //  FileClose(h);
  return(0);
}

