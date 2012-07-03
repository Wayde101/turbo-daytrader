#property copyright "Copyright (c) 2011, TingYu"
#property link      "http://www.17forex.com"

#property indicator_chart_window

int counted_bars = 0;
int img_width = 1024;
int img_high  = 768;
int init()
{
  return(0);
}

int start()
{
  int    lasterror    = 0;
  int    handle;
  string snapfile     = StringConcatenate("shots\\",
					  Symbol(), "_" ,
					  Period(), "\\" , 
					  iTime(NULL,0,0),
					  ".gif");

  string csvfile      = StringConcatenate("shots\\",
					  Symbol(), "_" ,
					  Period(), "\\" , 
					  "status",
					  ".csv");

  if (counted_bars != Bars ) {
    counted_bars = Bars;
    if(!WindowScreenShot(snapfile,img_width,img_high)) {
      Print("save faild with msg:",GetLastError());
    }
  }

  handle = FileOpen(csvfile,FILE_CSV|FILE_WRITE,";");

  if( handle >0 ) {
    FileWrite(handle,GetObjCsv("CC"));
    FileWrite(handle,GetObjCsv("MW"));
    FileWrite(handle,GetObjCsv("MW_up"));
    FileWrite(handle,GetObjCsv("MW_down"));
    DumpOrderTicket(handle);
    DumpAccountInfo(handle);
    DumpTrendSys(handle);
    DumpMarketInfo(handle);
    FileClose(handle);
  }
}

string GetObjCsv(string ObjName)
{
  string rtcsvstr=StringConcatenate("OBJNAME=",ObjName,";","STATUS=NA");
  if(ObjectFind(ObjName) == -1) {
    return(rtcsvstr);
  }

  rtcsvstr=StringConcatenate("OBJNAME=",ObjName,";",
			     "OBJPROP_TIME1=",ObjectGet(ObjName,OBJPROP_TIME1),  ";",
			     "OBJPROP_PRICE1=",ObjectGet(ObjName,OBJPROP_PRICE1),";",
			     "OBJPROP_TIME2=",ObjectGet(ObjName,OBJPROP_TIME2),  ";",
			     "OBJPROP_PRICE2=",ObjectGet(ObjName,OBJPROP_PRICE2),";",
			     "OBJPROP_TIME3=",ObjectGet(ObjName,OBJPROP_TIME3),  ";",
			     "OBJPROP_PRICE3=",ObjectGet(ObjName,OBJPROP_PRICE3) );
  if(ObjName == "CC" || ObjName == "MW") {
    rtcsvstr = StringConcatenate(rtcsvstr,";",ObjectDescription(ObjName));
  }
  
  return(rtcsvstr);
}

string DumpOrderTicket(int status_handle) {
  int    total=OrdersTotal();

  for(int pos=0;pos<total;pos++) {
    if(OrderSelect(pos,SELECT_BY_POS)==false) continue;
    if(OrderSymbol() == Symbol() && OrderMagicNumber() == Period()) {
      FileWrite(status_handle,
		StringConcatenate("OBJNAME=Order_",OrderTicket()),
		StringConcatenate("OrderTicket=",OrderTicket()),
		StringConcatenate("OrderOpenTime=",OrderOpenTime()),
		StringConcatenate("OrderType=",OrderType()),
		StringConcatenate("OrderLots=",OrderLots()),
		StringConcatenate("OrderOpenPrice=",OrderOpenPrice()),
		StringConcatenate("OrderStopLoss=",OrderStopLoss()),
		StringConcatenate("OrderTakeProfit=",OrderTakeProfit()),
		StringConcatenate("OrderCloseTime=",OrderCloseTime()),
		StringConcatenate("OrderClosePrice=",OrderClosePrice()),
		StringConcatenate("OrderCommission=",OrderCommission()),
		StringConcatenate("OrderSwap=",OrderSwap()),
		StringConcatenate("OrderProfit=",OrderProfit()),
		StringConcatenate("OrderComment=",OrderComment()),
		StringConcatenate("OrderMagicNumber=",OrderMagicNumber()),
		StringConcatenate("OrderExpiration=",OrderExpiration()));
    }
  }
}

string DumpAccountInfo(int status_handle) {

  FileWrite(status_handle,
	    "OBJNAME=AccountInfo",
	    StringConcatenate("AccountBalance=",AccountBalance()),
	    StringConcatenate("AccountCredit=", AccountCredit()),
	    StringConcatenate("AccountCompany=", "17forex"),
	    StringConcatenate("AccountCurrency=", AccountCurrency()),
	    StringConcatenate("AccountEquity=", AccountEquity()),
	    StringConcatenate("AccountFreeMargin=",  AccountFreeMargin()),
	    StringConcatenate("AccountProfit=",AccountProfit()));
}

string DumpTrendSys(int status_handle) {

  FileWrite(status_handle,
	    "OBJNAME=TrendSys",
	    StringConcatenate("M5=", iMA(NULL,0,5,0,MODE_EMA,PRICE_MEDIAN,0)),
	    StringConcatenate("M8=", iMA(NULL,0,8,0,MODE_EMA,PRICE_MEDIAN,0)),
	    StringConcatenate("M13=",iMA(NULL,0,13,0,MODE_EMA,PRICE_MEDIAN,0)),
	    StringConcatenate("M21=",iMA(NULL,0,21,0,MODE_EMA,PRICE_MEDIAN,0)),
	    StringConcatenate("M34=",iMA(NULL,0,34,0,MODE_EMA,PRICE_MEDIAN,0)),
	    StringConcatenate("M55=",iMA(NULL,0,55,0,MODE_EMA,PRICE_MEDIAN,0)));
}

string DumpMarketInfo(int status_handle) {
  FileWrite(status_handle,
	    "OBJNAME=MarcketInfo",
	    StringConcatenate("LOW=",MarketInfo(Symbol(),MODE_LOW)),
	    StringConcatenate("HIGH=",MarketInfo(Symbol(),MODE_HIGH)),
	    StringConcatenate("TIME=",MarketInfo(Symbol(),MODE_TIME)),
	    StringConcatenate("BID=",MarketInfo(Symbol(),MODE_BID)),
	    StringConcatenate("ASK=",MarketInfo(Symbol(),MODE_ASK)),
	    StringConcatenate("POINT=",MarketInfo(Symbol(),MODE_POINT)),
	    StringConcatenate("DIGITS=",MarketInfo(Symbol(),MODE_DIGITS)),
	    StringConcatenate("SPREAD=",MarketInfo(Symbol(),MODE_SPREAD)),
	    StringConcatenate("STOPLEVEL=",MarketInfo(Symbol(),MODE_STOPLEVEL)),
	    StringConcatenate("LOTSIZE=",MarketInfo(Symbol(),MODE_LOTSIZE)),
	    StringConcatenate("TICKVALUE=",MarketInfo(Symbol(),MODE_TICKVALUE)),
	    StringConcatenate("TICKSIZE=",MarketInfo(Symbol(),MODE_TICKSIZE)),
	    StringConcatenate("SWAPLONG=",MarketInfo(Symbol(),MODE_SWAPLONG)),
	    StringConcatenate("SWAPSHORT=",MarketInfo(Symbol(),MODE_SWAPSHORT)),
	    StringConcatenate("STARTING=",MarketInfo(Symbol(),MODE_STARTING)),
	    StringConcatenate("EXPIRATION=",MarketInfo(Symbol(),MODE_EXPIRATION)),
	    StringConcatenate("TRADEALLOWED=",MarketInfo(Symbol(),MODE_TRADEALLOWED)),
	    StringConcatenate("MINLOT=",MarketInfo(Symbol(),MODE_MINLOT)),
	    StringConcatenate("LOTSTEP=",MarketInfo(Symbol(),MODE_LOTSTEP)),
	    StringConcatenate("MAXLOT=",MarketInfo(Symbol(),MODE_MAXLOT)),
	    StringConcatenate("SWAPTYPE=",MarketInfo(Symbol(),MODE_SWAPTYPE)),
	    StringConcatenate("PROFITCALCMODE=",MarketInfo(Symbol(),MODE_PROFITCALCMODE)),
	    StringConcatenate("MARGINCALCMODE=",MarketInfo(Symbol(),MODE_MARGINCALCMODE)),
	    StringConcatenate("MARGININIT=",MarketInfo(Symbol(),MODE_MARGININIT)),
	    StringConcatenate("MARGINMAINTENANCE=",MarketInfo(Symbol(),MODE_MARGINMAINTENANCE)),
	    StringConcatenate("MARGINHEDGED=",MarketInfo(Symbol(),MODE_MARGINHEDGED)),
	    StringConcatenate("MARGINREQUIRED=",MarketInfo(Symbol(),MODE_MARGINREQUIRED)),
	    StringConcatenate("FREEZELEVEL=",MarketInfo(Symbol(),MODE_FREEZELEVEL)));
}
