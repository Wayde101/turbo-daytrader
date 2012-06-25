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
					  TimeCurrent(),
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
    FileWrite(handle,DumpObjCsv("CC"));
    FileWrite(handle,DumpObjCsv("MW"));
    FileWrite(handle,DumpObjCsv("MW_up"));
    FileWrite(handle,DumpObjCsv("MW_down"));
    FileClose(handle);
  }
}

string DumpObjCsv(string ObjName)
{
  string rtcsvstr=StringConcatenate("ON=",ObjName,";","NotFound");
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

