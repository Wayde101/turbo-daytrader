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
    DumpOrderCsv(handle);
    DumpAccountCsv(handle);
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

string DumpOrderCsv(int status_handle) {
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

string DumpAccountCsv(int status_handle) {

  FileWrite(status_handle,
	    "OBJNAME=AccountInfo",
	    StringConcatenate("AccountBalance=",AccountBalance()),
	    StringConcatenate("AccountCredit=", AccountCredit()),
	    StringConcatenate("AccountCompany=", "17forex"),
	    StringConcatenate("AccountCurrency=", AccountCurrency()),
	    StringConcatenate("AccountEquity=", AccountEquity()),
	    StringConcatenate("AccountFreeMargin=",  AccountFreeMargin()),
	    StringConcatenate("AccountProfit=",AccountProfit()));
  FileClose(status_handle);
}
