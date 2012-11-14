#property copyright ""
#define MAGICMA  1001

extern double DecreaseFactor     = 3;
extern double MovingPeriodPc     = 13;
extern double MovingPeriodFast   = 13;
extern double MovingPeriodSlow   = 55;
extern double MovingPeriodBack   = 55;
extern double MovingShift        = 0;
extern int signaltype = 1;
extern double Lots               = 0.2;
extern double MaximumRisk        = 0.02;

string rect_name = "NoneRect";

//+------------------------------------------------------------------+
//| Calculate open positions                                         |
//+------------------------------------------------------------------+
// 2012.8.21 - 2012.11.8
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
   lot=NormalizeDouble(AccountFreeMargin()*MaximumRisk/1000.0,2);
   return(lot);
  }
//+------------------------------------------------------------------+
//| Check for open order conditions                                  |
//+------------------------------------------------------------------+

void CheckForOpen_pc()
  {
   double ma;
   int    res;
   int    rect = t_is_in_rect();
   if(rect == 0) return;
   Print("rect:",rect);
   
//---- go trading only for first tiks of new bar
   if(Volume[0]>1) return;
//---- get Moving Average 
   ma=iMA(NULL,0,MovingPeriodPc,MovingShift,MODE_EMA,PRICE_CLOSE,1);
//---- sell conditions
   if(Open[1]>=ma && Close[1]<=ma && rect == -1)
     {
       res=OrderSend(Symbol(),OP_SELL,LotsOptimized(),Bid,3,High[iHighest(NULL,0,MODE_HIGH,MovingPeriodPc,0)],0,"",MAGICMA,0,Red);
       return;
     }
//---- buy conditions
   if(Open[1]<=ma && Close[1]>=ma && rect == 1)
     {
       res=OrderSend(Symbol(),OP_BUY,LotsOptimized(),Ask,3,Low[iLowest(NULL,0,MODE_LOW,MovingPeriodPc,0)],0,"",MAGICMA,0,Blue);
       return;
     }
//----
  }

//----
void CheckForOpen_mc()
  {
    double ma_fast[5],ma_slow[5];
    int    res;
    int    rect = t_is_in_rect();

    if(rect == 0) return;
   
//---- go trading only for first tiks of new bar
   if(Volume[0]>1) return;
//---- get Moving Average 
    for(int i=0;i<5;i++) {
      ma_fast[i] = iMA(NULL,0,MovingPeriodFast,MovingShift,MODE_EMA,PRICE_CLOSE,i);
      ma_slow[i] = iMA(NULL,0,MovingPeriodSlow,MovingShift,MODE_EMA,PRICE_CLOSE,i);
    }
//---- sell conditions
   
   if(ma_fast[1] < ma_slow[1] && ma_fast[3] > ma_slow[3] && rect == -1)
     {
       res=OrderSend(Symbol(),OP_SELL,LotsOptimized(),Bid,3,High[iHighest(NULL,0,MODE_HIGH,MovingPeriodFast,0)],0,"",MAGICMA,0,Red);
       return;
     }
//---- buy conditions
   if(ma_fast[1] > ma_slow[1] && ma_fast[3] < ma_slow[3] && rect == 1)
     {
       res=OrderSend(Symbol(),OP_BUY,LotsOptimized(),Ask,3,Low[iLowest(NULL,0,MODE_LOW,MovingPeriodFast,0)],0,"",MAGICMA,0,Blue);
       return;
     }
//----
  }

//----
void CheckForOpen_mc_then_back()
{
  double ma_fast[5],ma_slow[5],ma_back;
  int    res;
  int    rect = t_is_in_rect();

  if(rect == 0) return;
  //---- go trading only for first tiks of new bar
  if(Volume[0]>1) return;
  //---- get Moving Average 
  for(int i=0;i<5;i++) {
    ma_fast[i] = iMA(NULL,0,MovingPeriodFast,MovingShift,MODE_EMA,PRICE_CLOSE,i);
    ma_slow[i] = iMA(NULL,0,MovingPeriodSlow,MovingShift,MODE_EMA,PRICE_CLOSE,i);
  }

   ma_back = iMA(NULL,0,MovingPeriodBack,MovingShift,MODE_EMA,PRICE_CLOSE,1);

  //---- shell conditions
   if(ma_fast[1] < ma_slow[1] && rect == -1 && Ask >= ma_back)
    {
      res=OrderSend(Symbol(),OP_SELL,LotsOptimized(),Bid,3,High[iHighest(NULL,0,MODE_HIGH,MovingPeriodBack,0)],0,"",MAGICMA,0,Red);
      return;
    }

  //---- buy conditions
  if(ma_fast[1] > ma_slow[1] && rect == 1 && Bid <= ma_back)
    {
      res=OrderSend(Symbol(),OP_BUY,LotsOptimized(),Ask,3,Low[iLowest(NULL,0,MODE_LOW,MovingPeriodBack,0)],0,"",MAGICMA,0,Blue);
      return;
    }
  //----
  }

//+------------------------------------------------------------------+
//| Check for close order conditions                                 |
//+------------------------------------------------------------------+
void CheckForClose()
  {
   double ma;
//---- go trading only for first tiks of new bar
   if(Volume[0]>1) return;

//----
   for(int i=0;i<OrdersTotal();i++)
     {
      if(OrderSelect(i,SELECT_BY_POS,MODE_TRADES)==false)        break;
      if(OrderMagicNumber()!=MAGICMA || OrderSymbol()!=Symbol()) continue;
      //---- check order type

      if(OrderType()==OP_BUY)
        {
	  if(p_is_in_rect() == 0 || t_is_in_rect() == 0) OrderClose(OrderTicket(),OrderLots(),Bid,3,White);
	  break;
        }
      if(OrderType()==OP_SELL)
        {
	  if(p_is_in_rect() == 0 || t_is_in_rect() == 0) OrderClose(OrderTicket(),OrderLots(),Ask,3,White);
         break;
        }
     }
//----
  }


//+------------------------------------------------------------------+
//| Init function for test                                           |
//+------------------------------------------------------------------+

int set_rect(string name,int Color,datetime t1,double p1,datetime t2,double p2)
{
  ObjectCreate(name,OBJ_RECTANGLE,0,t1,p1,t2,p2);
  ObjectSet(name,OBJPROP_COLOR,Color);
}

int t_is_in_rect()
{
  int    obj_total=ObjectsTotal();
  string name;
  datetime t1,t2;
  int clr;
  for(int i=0;i<obj_total;i++) {
    name=ObjectName(i);
    if(ObjectType(name)!=OBJ_RECTANGLE) continue;
    t1 = ObjectGet(name,OBJPROP_TIME1);
    t2 = ObjectGet(name,OBJPROP_TIME2);
    clr = ObjectGet(name,OBJPROP_COLOR);
    if (TimeCurrent() > MathMin(t1,t2) && TimeCurrent() < MathMax(t1,t2)) {
      if( rect_name == "NoneRect" ) rect_name = name;
      if (clr == Red)   return(1);
      if (clr == Green) return(-1);
      continue;
    }
  }
  rect_name = "NoneRect";
  return(0);
}

int p_is_in_rect()
{
  int    obj_total=ObjectsTotal();
  string name;
  datetime t1,t2;
  double p1,p2,cp;
  int clr;

  if(rect_name != "NoneRect") {
    t1 = ObjectGet(rect_name,OBJPROP_TIME1);
    t2 = ObjectGet(rect_name,OBJPROP_TIME2);
    p1 = ObjectGet(rect_name,OBJPROP_PRICE1);
    p2 = ObjectGet(rect_name,OBJPROP_PRICE2);
    cp = (Bid + Ask) / 2;
    if (cp > MathMin(p1,p2) && cp < MathMax(p1,p2))  return(1);
  }
  return(0);
}

int enter_rect()
{
  int p = p_is_in_rect(),
      t = t_is_in_rect();
  Print("rn:",rect_name);
  if(p == 1 && t != 0)  return(1);
  return(0);
}


int init()
{
  if( ! IsTesting() ) return(0);
   set_rect("r1",Red,D'2012.08.22 09:30',1.24085,D'2012.08.23 00:00',1.25846);
   set_rect("r2",Red,D'2012.08.27 07:45',1.256127,D'2012.08.28 04:45',1.248002);
   set_rect("r3",Green,D'2012.08.23 19:45',1.25903,D'2012.08.24 15:45',1.24811);
   set_rect("r4",Red,D'2012.08.23 15:15',1.25272,D'2012.08.23 19:15',1.2578);
   set_rect("r5",Green,D'2012.08.14 18:30',1.23664,D'2012.08.15 16:45',1.22715);
   
   // set_rect("r2",Red,D'2012.08.27 00:00',1.256127,D'2012.08.28 04:45',1.248002);
  return(0);
}

//+------------------------------------------------------------------+
//| Start function                                                   |
//+------------------------------------------------------------------+
void start()
  {
//---- check for history and trading
   if(Bars<100 || IsTradeAllowed()==false) return;
//---- calculate open orders by current symbol
   if(CalculateCurrentOrders(Symbol())==0 && enter_rect() == 1) {
     if(signaltype == 1) CheckForOpen_pc();
     if(signaltype == 2) CheckForOpen_mc();
     if(signaltype == 3) CheckForOpen_mc_then_back();
   }
   else  CheckForClose();
//----
  }
//+------------------------------------------------------------------+
