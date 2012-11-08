#define MAGICMA  20050610

extern double Lots               = 0.1;
extern double MaximumRisk        = 0.02;
extern double DecreaseFactor     = 3;
extern double MovingPeriod       = 13;
extern double MovingShift        = 6;
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
      if(losses>1) lot=NormalizeDouble(lot-lot*losses/DecreaseFactor,1);
     }
//---- return lot size
   if(lot<0.1) lot=0.1;
   return(lot);
  }
//+------------------------------------------------------------------+
//| Check for open order conditions                                  |
//+------------------------------------------------------------------+
void CheckForOpen()
  {
   double ma;
   int    res;
   int    rect = t_is_in_rect();
   Print("rect:",rect);
   if(rect == 0) return;
   
//---- go trading only for first tiks of new bar
   if(Volume[0]>1) return;
//---- get Moving Average 
   ma=iMA(NULL,0,MovingPeriod,0,MODE_EMA,PRICE_CLOSE,1);
//---- sell conditions
   if(Open[1]>=ma && Close[1]<=ma && rect == -1)
     {
       res=OrderSend(Symbol(),OP_SELL,LotsOptimized(),Bid,3,High[iHighest(NULL,0,MODE_HIGH,MovingPeriod,0)],0,"",MAGICMA,0,Red);
       return;
     }
//---- buy conditions
   Print("Open[1]:",Open[1]," Close[1]:",Close[1]," MA:",ma);
   if(Open[1]<=ma && Close[1]>=ma && rect == 1)
     {
       res=OrderSend(Symbol(),OP_BUY,LotsOptimized(),Ask,3,Low[iLowest(NULL,0,MODE_LOW,MovingPeriod,0)],0,"",MAGICMA,0,Blue);
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
//---- get Moving Average 
   ma=iMA(NULL,0,MovingPeriod,MovingShift,MODE_EMA,PRICE_CLOSE,0);
//----
   for(int i=0;i<OrdersTotal();i++)
     {
      if(OrderSelect(i,SELECT_BY_POS,MODE_TRADES)==false)        break;
      if(OrderMagicNumber()!=MAGICMA || OrderSymbol()!=Symbol()) continue;
      //---- check order type

      if(OrderType()==OP_BUY)
        {
	  //if(Open[1]>ma && Close[1]<ma) OrderClose(OrderTicket(),OrderLots(),Bid,3,White);
	  if(p_is_in_rect() == 0 || t_is_in_rect() == 0) OrderClose(OrderTicket(),OrderLots(),Bid,3,White);
	  break;
        }
      if(OrderType()==OP_SELL)
        {
	  //if(Open[1]<ma && Close[1]>ma) OrderClose(OrderTicket(),OrderLots(),Ask,3,White);
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
    if (TimeCurrent() > t1 && TimeCurrent() < t2) {
      if (clr == Red)   return(1);
      if (clr == Green) return(-1);
      continue;
    }
  }
  return(0);
}

int p_is_in_rect()
{
  int    obj_total=ObjectsTotal();
  string name;
  datetime t1,t2;
  double p1,p2,cp;
  int clr;
  for(int i=0;i<obj_total;i++) {
    name=ObjectName(i);
    if(ObjectType(name)!=OBJ_RECTANGLE) continue;
    t1 = ObjectGet(name,OBJPROP_TIME1);
    t2 = ObjectGet(name,OBJPROP_TIME2);
    p1 = ObjectGet(name,OBJPROP_PRICE1);
    p2 = ObjectGet(name,OBJPROP_PRICE2);
    cp = (Bid + Ask) / 2;
    clr = ObjectGet(name,OBJPROP_COLOR);

    if ((TimeCurrent() > t1 && TimeCurrent() < t2) &&
	(cp > MathMin(p1,p2) && cp < MathMax(p1,p2))) {
      return(1);
    }
  }
  return(0);
}


int init()
{
  if( ! IsTesting() ) return(0);
   set_rect("r1",Red,D'2012.08.22 09:30',1.24085,D'2012.08.23 00:00',1.25846);
   set_rect("r2",Red,D'2012.08.27 07:45',1.256127,D'2012.08.28 04:45',1.248002);
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


   if(CalculateCurrentOrders(Symbol())==0) CheckForOpen();
   else                                    CheckForClose();
//----
  }
//+------------------------------------------------------------------+
