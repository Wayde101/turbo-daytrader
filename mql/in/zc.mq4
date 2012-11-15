//+------------------------------------------------------------------+
//|                                               Moving Average.mq4 |
//|                      Copyright © 2005, MetaQuotes Software Corp. |
//|                                       http://www.metaquotes.net/ |
//+------------------------------------------------------------------+
#define MAGICMA  1002

extern double Lots               = 0.1;
extern double MaximumRisk        = 0.02;
extern double DecreaseFactor     = 3;
extern double MovingPeriod       = 12;
extern double MovingShift        = 6;
extern double CCEntry = 0.60;

double ccdist=0,
       cc0p = 0,
       cc1p = 0;
string zpoint="Nil";

// 均线系统。
// 2012.07.24-2012.07.30

bool has_cc() {
  if(ObjectFind("CC") == -1) return(false);
  return(true);
}

double get_channel_angle() {
  if( ! has_cc() ) {
    ObjectDelete("angle");
    return(361);
  }

  parse_cc_desc();

  if(ObjectFind("angle") == -1) {
    ObjectCreate("angle",
		 OBJ_TRENDBYANGLE,
		 0,
		 ObjectGet("CC",OBJPROP_TIME1),
		 ObjectGet("CC",OBJPROP_PRICE1),
		 ObjectGet("CC",OBJPROP_TIME2),
		 ObjectGet("CC",OBJPROP_PRICE2));

    ObjectSet("angle",OBJPROP_TIME1,ObjectGet("CC",OBJPROP_TIME1));
    ObjectSet("angle",OBJPROP_PRICE1,ObjectGet("CC",OBJPROP_PRICE1));
    ObjectSet("angle",OBJPROP_TIME2,ObjectGet("CC",OBJPROP_TIME2));
    ObjectSet("angle",OBJPROP_PRICE2,ObjectGet("CC",OBJPROP_PRICE2));

  } else {
    ObjectSet("angle",OBJPROP_TIME1,ObjectGet("CC",OBJPROP_TIME1));
    ObjectSet("angle",OBJPROP_PRICE1,ObjectGet("CC",OBJPROP_PRICE1));
    ObjectSet("angle",OBJPROP_TIME2,ObjectGet("CC",OBJPROP_TIME2));
    ObjectSet("angle",OBJPROP_PRICE2,ObjectGet("CC",OBJPROP_PRICE2));
  }
  if(zpoint == "MW_up") {
    return(360 - ObjectGet("angle",OBJPROP_ANGLE));
  }
  return(ObjectGet("angle",OBJPROP_ANGLE));
}



bool parse_cc_desc() {
  if ( ! has_cc() ) {
    ccdist = 0;
    cc0p = 0;
    cc1p = 0;
    zpoint = "Nil";
    return(false);
  }

  int offset;
  string optStr = ObjectDescription("CC");
  string ss="Nil";
  //Print("has cc in cc_desc",optStr);

  for(int pos=0; pos<StringLen(optStr); pos++) {
    if(StringGetChar(optStr,pos) == 59) {
      ss = StringSubstr(optStr, offset, pos - offset);
      if(StringSubstr(ss,0,StringLen("CCDIST")) == "CCDIST") {
	ccdist=StrToDouble(StringSubstr(ss,
					StringLen("CCDIST") + 1,
					StringLen(ss)));
	//Print(ccdist);
      }

      if(StringSubstr(ss,0,StringLen("CC0P")) == "CC0P") {
	cc0p=StrToDouble(StringSubstr(ss,
				      StringLen("CC0P") + 1,
				      StringLen(ss)));
	//Print(cc0p);
      }

      if(StringSubstr(ss,0,StringLen("CC1P")) == "CC1P") {
	cc1p=StrToDouble(StringSubstr(ss,
				      StringLen("CC1P") + 1,
				      StringLen(ss)));
	//Print(cc1p);
      }
      if(StringSubstr(ss,0,StringLen("ZPOINT")) == "ZPOINT") {
	zpoint=StringSubstr(ss,
			    StringLen("ZPOINT") + 1,
			    StringLen(ss));
	//Print(zpoint);
      }
      offset = pos + 1;
    }
  }
  return(true);
}


//+------------------------------------------------------------------+
//| Calculate open positions                                         |
//+------------------------------------------------------------------+
int CalculateCurrentOrders(string symbol)
  {
   int buys=0,sells=0;
//----
   for(int i=0;i<OrdersTotal();i++)
     {
      if(OrderSelect(i,SELECT_BY_POS,MODE_TRADES)==false) break;
      if(OrderSymbol()==Symbol() && OrderMagicNumber()==MAGICMA)
        {
         if(OrderType()==OP_BUY)  buys++;
         if(OrderType()==OP_SELL) sells++;
        }
     }
//---- return orders volume
   if(buys>0) return(buys);
   else       return(-sells);
  }
//+------------------------------------------------------------------+
//| Calculate optimal lot size                                       |
//+------------------------------------------------------------------+
double LotsOptimized()
  {
   double lot=Lots;
   int    orders=HistoryTotal();     // history orders total
   int    losses=0;                  // number of losses orders without a break
//---- select lot size
   lot=NormalizeDouble(AccountFreeMargin()*MaximumRisk/1000.0,1);
//---- calcuulate number of losses orders without a break
   if(DecreaseFactor>0)
     {
      for(int i=orders-1;i>=0;i--)
        {
         if(OrderSelect(i,SELECT_BY_POS,MODE_HISTORY)==false) { Print("Error in history!"); break; }
         if(OrderSymbol()!=Symbol() || OrderType()>OP_SELL) continue;
         //----
         if(OrderProfit()>0) break;
         if(OrderProfit()<0) losses++;
        }
      if(losses>2) lot=NormalizeDouble(lot-lot*losses/DecreaseFactor,1);
     }
//---- return lot size
   if(lot<0.1) lot=0.1;
   return(lot);
  }

bool close_to_entry() {
  double cp = (Bid + Ask) / 2;
  Print("rate:",MathAbs( cp - ObjectGetValueByShift("angle",0)) / ccdist);
  return (MathAbs( cp - ObjectGetValueByShift("angle",0)) / ccdist >= CCEntry);
}


bool ReadyCond() {
  if( get_channel_angle() > 35 ) return (false);
  Print("angle less 35:",get_channel_angle());
  //if( ccdist > 0.0050 ) return(false);
  if( ! close_to_entry() ) return(false);
  Print("current price close to entry");  

  return(true);
}

//+------------------------------------------------------------------+
//| Check for open order conditions                                  |
//+------------------------------------------------------------------+
void CheckForOpen()
  {
   double ma;
   int    res;
//---- go trading only for first tiks of new bar
   if(Volume[0]>1) return;
   if( ! ReadyCond() ) return(false);

   
   if(zpoint == "MW_up") {
     Print("sl:",cc1p-0.0030);
     Print("tp:",cc0p);
      res=OrderSend(Symbol(),
		    OP_BUY,
		    LotsOptimized(),
		    Ask,
		    3,
		    cc1p - ccdist,
		    cc0p + 0.0030,
		    "",
		    MAGICMA,
		    0,
		    Red);
      return;     
   }

   if(zpoint == "MW_down") {
      res=OrderSend(Symbol(),
		    OP_SELL,
		    LotsOptimized(),
		    Bid,
		    3,
		    cc1p + ccdist,
		    cc0p - 0.0030,
		    "",
		    MAGICMA,
		    0,
		    Blue);
      return;     
   }
   Print("Zap!");

   
  }
//+------------------------------------------------------------------+
//| Check for close order conditions                                 |
//+------------------------------------------------------------------+
void CheckForModify()
  {
    if(ObjectFind("angle") == -1)  return;
    for(int i=0;i<OrdersTotal();i++)
      {
	if(OrderSelect(i,SELECT_BY_POS,MODE_TRADES)==false)        break;
	if(OrderMagicNumber()!=MAGICMA || OrderSymbol()!=Symbol()) continue;
	//---- check order type 
	if(OrderType()==OP_BUY)
	  {
	    if( Ask >= ObjectGetValueByShift("angle",0)) {
	      OrderModify(OrderTicket(),
			  OrderOpenPrice(),
			  Low[iLowest(NULL,0,MODE_LOW,11,0)],
			  //OrderOpenPrice(),
			  OrderTakeProfit(),
			  White);
	      ObjectDelete("angle");
	    }
	    break;
	  }
	if(OrderType()==OP_SELL)
	  {
	    if( Bid <= ObjectGetValueByShift("angle",0)) {
	      OrderModify(OrderTicket(),
			  OrderOpenPrice(),
			  //OrderOpenPrice(),
			  High[iHighest(NULL,0,MODE_HIGH,11,0)],
			  OrderTakeProfit(),
			  White);
	      ObjectDelete("angle");
	    }
	    break;
	  }
      }
  }

void init() {
  // clean all object
  ObjectDelete("CC");
  ObjectDelete("angle");
}

//+------------------------------------------------------------------+
//| Start function                                                   |
//+------------------------------------------------------------------+
void start()
  {
//---- check for history and trading
   if(Bars<100 || IsTradeAllowed()==false) return;

//---- calculate open orders by current symbol
   if(CalculateCurrentOrders(Symbol())==0 ) CheckForOpen();
   else					    CheckForModify();
//----
  }
//+------------------------------------------------------------------+
