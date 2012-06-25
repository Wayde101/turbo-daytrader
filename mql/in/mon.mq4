#property copyright "Copyright (c) 2011, TingYu"
#property link      "http://www.17forex.com"

#property indicator_chart_window


int init()
{
  return(0);
}

int start()
{
  Print("AutoTradeon is on");
  if(ObjectFind("CC") == -1 ) {
    return(0)
  }
  signal_parser("AutoTradeOn");
  return(0);
}

int signal_parser(string signame) {
  string sigfile,
	 sigpath;
  int    sighandle;
  int    sflag;
  
  sigpath = StringConcatenate("shots\\",
			      Symbol(), "_" ,
			      Period());

  if(signame == "AutoTradeOn") {
    sigfile = StringConcatenate(sigpath, "\\" , signame);
    Print(sigfile);

    sighandle = FileOpen(sigfile,FILE_READ);
    
    if(sighandle < 1) {
      Print("Failed");
      return(0);
    } 
    
    FileClose(sighandle);
    FileDelete(sigfile);
    Print("Proccessing: getting", sigfile ," then remove it");
  }

  if(signame == "")
}
