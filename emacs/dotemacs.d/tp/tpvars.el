
(setq time-frame-vars (quote (("mon" nil :name "1月" :mtime 1316080476.259275 :threshold 38707200) ("wek" nil :name "1周" :mtime 1316080643.152473 :threshold 9676800) ("day" nil :name "1日" :mtime 1318149579.292868 :threshold 1382400) ("4hr" nil :name "4时" :mtime 1318469886.576708 :threshold 230400) ("1hr" nil :name "1时" :mtime 1318469886.578657 :threshold 57600) ("15m" nil :name "1刻" :mtime 1318469886.603503 :threshold 14400))))

(setq tplan-vars (quote (("usdx-mon" nil :obj 下 :sub 上) ("usdx-wek" nil :obj 转 :sub 星) ("usdx-day" nil :obj 上 :sub 星 :sum "客观均线中的55日均线支撑了汇价，但是目前来看美元指数高位主主交替." :tsel "NA" :gfx "NA") ("usdx-4hr" nil :obj 下 :sub 下 :sum "均线系统已经对指数形成压制,接下来一周美元指数进入下跌趋势." :dsum "一致性较好" :gfx "NA" :tsel "NA") ("usdx-1hr" nil :obj 下 :sub 下 :qiang "" :sum "美元指数依然处于下跌节奏当中，缝次空美元" :gfx "NA" :tsel "NA" :dsum "除了日元意外其他货币主客观方向一致向上.") ("usdx-15m" nil :obj "NA" :sub "NA" :sum "" :gfx "NA" :tsel "NA" :dsum "澳元加元一致走弱，欧系货币和日元震荡整理") ("eur-mon" nil :obj 横 :sub 上) ("eur-wek" nil :obj 转 :sub 下) ("eur-day" nil :obj 下 :sub 星 :tsel "NA" :gfx "NA") ("eur-4hr" nil :obj 上 :sub 上 :gfx "nc" :zu "1.3943" :cheng "1.3557" :tsel "NA") ("eur-1hr" nil :obj 上 :sub 上 :gfx "nc" :cheng "1.3553" :zu "1.3943" :tsel "NA" :qr 3.75) ("eur-15m" nil :obj "NA" :sub "NA" :gfx "NA" :cheng "1.3635" :zu "1.3479" :tsel "NA") ("gbp-mon" nil :obj 下 :sub 下) ("gbp-wek" nil :obj 转 :sub 下) ("gbp-day" nil :obj "NA" :sub "NA" :tsel "NA" :gfx "NA") ("gbp-4hr" nil :obj 上 :sub 上 :gfx "nc" :cheng "1.5537" :zu "1.6098" :tsel "NA") ("gbp-1hr" nil :obj 上 :sub 上 :gfx "cc" :zu "" :cheng "1.5655" :tsel "NA" :qr 3.25) ("gbp-15m" nil :obj "NA" :sub "NA" :gfx "NA" :cheng "1.5524" :zu "1.5609" :tsel "NA") ("chf-mon" nil :obj 上 :sub 上) ("chf-wek" nil :obj 转 :sub 下) ("chf-day" nil :obj 下 :sub 下 :tsel "NA" :gfx "NA") ("chf-4hr" nil :obj 上 :sub 上 :gfx "nc" :cheng "0.9127" :zu "0.8685" :tsel "NA") ("chf-1hr" nil :obj 上 :sub 上 :gfx "cc" :cheng "0.9024" :zu "0" :tsel "NA" :qr 3.5) ("chf-15m" nil :obj "NA" :sub "NA" :gfx "NA" :tsel "NA" :cheng "0.9021" :zu "0.8950") ("aud-mon" nil :obj 上 :sub 星) ("aud-wek" nil :obj 转 :sub 下) ("aud-day" nil :obj 下 :sub 星 :tsel "NA" :gfx "NA") ("aud-4hr" nil :obj 上 :sub 上 :gfx "nc" :cheng "1.0043" :zu "1.0418" :tsel "NA") ("aud-1hr" nil :obj 上 :sub 上 :gfx "nc" :tsel "NA" :cheng "0.9802" :zu "9" :qr 3.5) ("aud-15m" nil :obj "NA" :sub "NA" :gfx "NA" :tsel "NA" :cheng "" :zu "0.9837") ("cad-mon" nil :obj 上 :sub 下) ("cad-wek" nil :obj 转 :sub 下) ("cad-day" nil :obj "NA" :sub "NA" :tsel "NA" :gfx "NA") ("cad-4hr" nil :obj 上 :sub 上 :gfx "nc" :cheng "1.0337" :zu "1.0135" :tsel "NA") ("cad-1hr" nil :obj 上 :sub 上 :gfx "cc" :tsel "NA" :cheng "1.0261" :zu "1.0135" :qr 3.5) ("cad-15m" nil :obj "NA" :sub "NA" :gfx "NA" :tsel "NA" :cheng "0" :zu "1.0279") ("jpy-mon" nil :obj "NA" :sub "NA") ("jpy-wek" nil :obj "NA" :sub "NA") ("jpy-day" nil :obj "NA" :sub "NA" :tsel "NA" :gfx "NA") ("jpy-4hr" nil :obj 下 :sub 下 :gfx "nc" :cheng "0" :zu "0" :tsel "NA") ("jpy-1hr" nil :obj 下 :sub 下 :gfx "NA" :tsel "NA" :zu "76.16" :cheng "76.85" :qr 3.25) ("jpy-15m" nil :obj "NA" :sub "NA" :gfx "NA" :tsel "NA" :cheng "" :zu ""))))
