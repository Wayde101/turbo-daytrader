#property copyright "Copyright (c) 2011, TingYu"
#property link      "http://www.17forex.com"

#property indicator_chart_window

string ticket_in[12];
string ticket_path;
string ticket_in_file;
int    CRITICAL = 0;

int init()
{
  ticket_path = StringConcatenate("shots\\",
				  Symbol(), "_" ,
				  Period());
  ticket_in_file = StringConcatenate(ticket_path, "\\ticket.in");
  
  return(0);
}


int start()
{
  reset_ticket_in();
  ticket_read();
  ticket_proc();
  return(0);
}

int reset_ticket_in() {
  for(int i = 0 ; i <= 12; i++) {
    ticket_in[i] = "NA";
  }
  return(0);
}

int ticket_read() {
  int    ticket_handle;
  int    lastError;

  ticket_handle = FileOpen(ticket_in_file,FILE_CSV|FILE_READ);
    
  if(ticket_handle < 1) {
    return(1);
  }
  
  for(int i = 0 ; i <= 11 ; i++) {
    ticket_in[i] = FileReadString(ticket_handle);    
  }

  FileClose(ticket_handle);
  return(0);
}

int ticket_proc() {
  
  if(ticket_in[0] == "OBJNAME=OrderSend") {
    double expect_price  = StrToDouble(ticket_in[4]),
           current_price = 0;
    int    t;
    int    order_trigger = 0;   // 0 表示不具备扳机条件.
    int    order_cmd     = StrToInteger(ticket_in[2]);
    double order_vol     = StrToDouble(ticket_in[3]);
    double order_price   = StrToDouble(ticket_in[4]);
    int    order_slippage = StrToInteger(ticket_in[5]);
    double order_stoploss = StrToDouble(ticket_in[6]);
    double order_takeprofit = StrToDouble(ticket_in[7]);
    string order_comment  = ticket_in[8];
    int    order_magic    = StrToInteger(ticket_in[9]);
    datetime order_expiration = 0;

    int lastError;
    if (CRITICAL == 1) {
      FileDelete(ticket_in_file);
      lastError = GetLastError();
      if(lastError != 0) {
	Print("An error ocurred while (",lastError,") deleting file:",ticket_in_file);
	CRITICAL = 1;
	return(4);  // 下单成功，但是清除 ticket.in 失败，比较严重.
      } else {
	CRITICAL = 0;
	return(5);  
      }
    }
    
    if(ticket_in[0] == "NA" || StrToDouble(ticket_in[3]) > 0.5) {
      Print("Wrong @",ticket_in,";",ticket_in[3]);
      rm_obj("PendingLine","No ticket.in found!");
      rm_obj("StopLossLine","No ticket.in found!");
      rm_obj("TakeProfit","No ticket.in found!");
      return(-1); // 没有发现ticket.in 或者仓位离谱返回 -1 .
    }

    
    hline_reprice("PendingLine",expect_price);
    hline_reprice("StopLossLine",order_stoploss);
    hline_reprice("TakeProfit",order_takeprofit);
  
    if(order_cmd == OP_SELL)  {
      current_price     = Bid;
      ObjectSet("PendingLine",OBJPROP_COLOR,Green);
      if( current_price >= expect_price ) {
	order_trigger = 1;
      }
    }
    else if (order_cmd == OP_BUY) {
      current_price     = Ask;
      ObjectSet("PendingLine",OBJPROP_COLOR,Red);
      if( current_price <= expect_price ) {
	order_trigger = 1;
      }
    }
    else {
      return(1);   // 如果 交易指令不属于 OP_BUY OP_SELL, 返回 1
    }

    if ( order_trigger == 0 ) {
      Print("Order Price still out of expected price:[",current_price,"]");
      return(2);  // 价格未到退出。
    }

    t = OrderSend(Symbol(),
		  order_cmd,
		  order_vol,
		  current_price,
		  order_slippage,
		  order_stoploss,
		  order_takeprofit,
		  order_comment,
		  Period(),
		  order_expiration);

    if(t < 0) {
      Print("OrderSend failed with error #",GetLastError());
      return(3); // 下单失败。
    } else {
      FileDelete(ticket_in_file);
      lastError = GetLastError();
      if(lastError != 0) {
	Print("An error ocurred while (",lastError,") deleting file:",ticket_in_file);
	CRITICAL = 1;
	return(4);  // 下单成功，但是清除 ticket.in 失败，比较严重.
      }
    }
    return(0);
  }
  
  if(ticket_in[0] == "OBJNAME=OrderModify") {
    double mod_ticket     = StrToInteger(ticket_in[1]);
    double mod_stoploss   = StrToDouble(ticket_in[2]);
    double mod_takeprofit = StrToDouble(ticket_in[3]);
    Print("OrderModify recieved, ticket:",mod_ticket);
    OrderSelect(mod_ticket,SELECT_BY_TICKET);
    if(OrderModify(OrderTicket(),OrderOpenPrice(),mod_stoploss,mod_takeprofit)) {
      Print("OrderModify failed:",GetLastError());
    }
  }
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

int hline_reprice(string objname,double p) {
  if(ObjectFind(objname) == -1) {
    ObjectCreate(objname,OBJ_HLINE,0,0,p);
    return(0);
  }
  ObjectSet(objname,OBJPROP_PRICE1,p);
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

