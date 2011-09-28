(require 'info)
;; (require 'widget)
(require 'tree-widget)
;; (require 'tree-mode)

(setq time-frame-vars nil)
(setq tplan-vars nil)
(setq tplan-)

(defvar forex-el "~/.emacs.d/tp/tpvars.el"
  "tradeplan vars"
  )

(defvar forex-symbol '("usdx" "eur" "gbp" "chf" "aud" "cad" "jpy")
  "symbo lists")

(defvar time-frame '("mon" "wek" "day" "4hr" "1hr" "15m")
  "time frame lists")

(defvar tp-buffer-name "*交易计划模板*"
  "*Name of the buffer")

(defvar tp-list
  '(("交易计划模板" tp-contents :header "交易计划模板" )
    ("市场整体情况" tp-usdx :header "市场整体情况(美元指数分析)")
    ("交易币种初选" tp-fselect :header "货币初选")
    ("选定币种趋势信息表" tp-tselected :header "选定币种趋势信息表")
    ("交易信息确认" tp-tinfo-ensure :header "交易信息确认")
    ("图表分析" tp-tinfo-chart :header "图表分析")
    ("交易计划审核" tp-tinfo-verify :header "交易计划审核")
    ("交易计划执行" tp-tinfo-exec :header "交易计划执行")
    ("交易总结" tp-tinfo-summary :header "交易总结")
    )
  "每日交易功课菜单列表")

(defvar tp-current nil
  "Current page in `tp-list'.")

(defvar tp-form nil
  "A table for lookup widget created in current buffer.")

(defvar tp-anchors nil
  "A table for lookup markers created in current buffer.")

(defvar tp-mode-map
  (let ((map (make-sparse-keymap)))
    (set-keymap-parent map widget-keymap)
    (define-key map "n" 'tp-next)
    (define-key map "p" 'tp-previous)
    (define-key map "u" 'tradeplan-without-vars)
    (define-key map "j" 'next-line)
    (define-key map "k" 'previous-line)
    (define-key map "h" 'widget-backward)
    (define-key map "l" 'widget-forward)
    (define-key map "s" 'save-tp-vars)
    (define-key map "/" 'isearch-forward)
    (dolist (num (number-sequence ?1 ?9))
      (define-key map (char-to-string num) 'tp-goto-page))
    ;; this command may be helpful for debug
    (define-key map "r" 'tp-reset)
    (define-key map "\C-c\C-s" 'tp-show-source)
    (define-key map "\C-c\C-n" 'tp-next)
    (define-key map "\C-c\C-p" 'tp-previous)
    (define-key map "\C-c\C-u" 'tradeplan)
    (define-key map "\C-c\C-t" 'tradeplan)
    map)
  "Keymap to use in *Widget Demo* buffer.")

;;{{{  Helper functions
(defmacro dolist-if ( pair condtion body)
  (list 'let '(result)
        (list 'dolist  (append pair '(result))
              (list 'if condtion
                    (list 'setq 'result 
                          (list 'append 'result 
                                (list 'list 
                                      (list 'progn
                                            body))))))))

(defun tp-menu-goto ()
  (interactive)
  (tp-goto (symbol-name last-command-event)))

(defun tp-form-create (id widget)
  (if (assoc id tp-form)
      (error "identifier %S is used!" id)
    (push (cons id widget) tp-form)))

(defun tp-form-add (id widget)
  (let ((old (assoc id tp-form)))
    (if old
        (setcdr old widget)
      (push (cons id widget) tp-form))))

(defun tp-form-get (id)
  (cdr (assoc id tp-form)))

(defun tp-create-anchor (anchor)
  (push (cons anchor (point-marker)) tp-anchors))

(defun tp-resolve-link (name)
  "Return the Next, Top, Next page."
  (let* ((page (assoc name tp-list))
         (rest (member page tp-list))
         (len (length rest))
         next previous)
    ;; the contents only list next 
    (if (eq page (car tp-list))
        (list (cadr tp-list))
      (if (= len 1)
          (setq next nil)
        (setq next (cadr rest)))
      (setq previous (nth (- (length tp-list) len 1)
                          tp-list))
      (list next (car tp-list) previous))))

(defun tp-add-page (&rest page)
  "add new PAGE to tp.
The page is constituted by

 (PAGE-NAME PAGE-DEFINITION [KEYWORD VALUE]).

Current only keyword :header is supported, which value is a string
to display in menu and the header of buffer instead of the page-name."
  (setq tp-list
        (append tp-list (list page))))

(defun tp-remove-page (name)
  (setq tp-list
        (delq (assoc name tp-list)
              tp-list)))
;;}}}


;;{{{  tpvar manage functions
(defun dump-vars-to-file (varlist filename)
  "simplistic dumping of variables in VARLIST to a file FILENAME"
  (save-excursion
    (let ((buf (find-file-noselect filename)))
      (set-buffer buf)
      (erase-buffer)
      (dump varlist buf)
      (save-buffer)
      (kill-buffer))))

(defun dump (varlist buffer)
  "insert into buffer the setq statement to recreate the variables in VARLIST"
  ;; (loop for var in varlist do
  (dolist (var varlist)
        (print (list 'setq var (list 'quote (symbol-value var)))
               buffer)))

(defun write-string-to-file (string file)
  (interactive "sEnter the string: \nFFile to save to: ")
  (with-temp-buffer
    (insert string)
    (when (file-writable-p file)
      (write-region (point-min)
		    (point-max)
		    file))))


(defun init-time-frame-vars()
  (interactive)

  (let* ((15m (* 60 15))
	 (1hr (* 15m 4))
	 (4hr (* 1hr 4))
	 (day (* 4hr 6))
	 (wek (* day 7))
	 (mon (* wek 4))
	 (thsn  16)
	 (thsec 0)
	 (cname "无名")
	 )
    
    (dolist (var time-frame)
      (cond ((string= var "15m") (progn (setq thsec (* 15m thsn)) (setq cname "1刻")))
	    ((string= var "1hr") (progn (setq thsec (* 1hr thsn)) (setq cname "1时")))
	    ((string= var "4hr") (progn (setq thsec (* 4hr thsn)) (setq cname "4时")))
	    ((string= var "day") (progn (setq thsec (* day thsn)) (setq cname "1日")))
	    ((string= var "wek") (progn (setq thsec (* wek thsn)) (setq cname "1周")))
	    ((string= var "mon") (progn (setq thsec (* mon thsn)) (setq cname "1月"))))

      (if (not (assoc var time-frame-vars))
	  (setq time-frame-vars (append time-frame-vars
					(list
					 (list var
					       nil		;nil function 
					       :usdx nil
					       :eur  nil
					       :gbp  nil
					       :chf  nil
					       :cad  nil
					       :aud  nil
					       :jpy  nil
					       :name cname
					       :mtime 0
					       :tp-sum nil
					       :threshold thsec)
					 )))))))

(defun init-tplan-vars()
  (interactive)
  (dolist (s forex-symbol)
    (dolist (f time-frame)
      (if (not (assoc (concat s "-" f) tplan-vars))
	  (setq tplan-vars (append tplan-vars
				   (list
				    (list (concat s "-" f)
					  nil
					  :obj "NA"
					  :sub "NA"
				     ))))))))


(defun mod-touch-tf (fxs-tfm)
  "初始化每个时间级别的 mtime mod by threshold, 如果超过 threadhold 会update mtime"
  (let* ((tf (cadr (split-string fxs-tfm "-")))
	 (th (plist-get (assoc tf time-frame-vars) :threshold))
	 (mt (plist-get (assoc tf time-frame-vars) :mtime)))

    (message "time frame:[%s] modify time:[%s]" tf mt) 
    (if (> (- (float-time) mt) th)
	(plist-put (assoc tf time-frame-vars) :mtime (float-time))
	)
       )
  )

(defun tpvar-update (fxs-tfm key val)
  "主观方向与客观方向的更新 args: "
    (mod-touch-tf fxs-tfm)
    (plist-put (assoc fxs-tfm tplan-vars) key val)
  )

(defun tpvar-get (fxs-tfm key)
  "主观方向与客观方向的更新 args: "
  (let* ((tf (cadr (split-string fxs-tfm "-")))
	 (th (plist-get (assoc tf time-frame-vars) :threshold))
	 (mt (plist-get (assoc tf time-frame-vars) :mtime))
	 (out (plist-get (assoc fxs-tfm tplan-vars) key)))

    ;; (message "time frame:[%s] modify time:[%s]" tf mt) 
    (if (< (- (float-time) mt) th)
	out
      (progn (tpvar-update (concat "usdx-" tf) :sum "")
	(dolist (fxs forex-symbol)
	       (if (or (string= key ":obj") (string= key ":sub") (string= key ":gfx"))
		   (progn (tpvar-update (concat fxs "-" tf) :obj "NA")
			  (tpvar-update (concat fxs "-" tf) :sub "NA")
			  (tpvar-update (concat fxs "-" tf) :tsel "NA")
			  (tpvar-update (concat fxs "-" tf) :gfx "NA"))))
	     "NA")
      )))


(defun tpvar-get-float (fxs-tfm key)
  "主观方向与客观方向的更新 args: "
  (let* ((tf (cadr (split-string fxs-tfm "-")))
	 (th (plist-get (assoc tf time-frame-vars) :threshold))
	 (mt (plist-get (assoc tf time-frame-vars) :mtime))
	 (out (plist-get (assoc fxs-tfm tplan-vars) key)))

    (if out
	(string-to-number out)
	)
    (message "time frame:[%s] modify time:[%s]" tf mt) 
    (if (< (- (float-time) mt) th)
	(if out
	    (string-to-number out)
	  9)
      9)))
;;}}}


;;{{{  Commands
;;;###autoload

(defun save-tp-vars()
  "保存变量"
  (interactive)
  (dump-vars-to-file '(time-frame-vars tplan-vars) forex-el)
  )

(defun tradeplan-without-vars ()
  "goto tradeplan page"
  (interactive)
  (switch-to-buffer tp-buffer-name)
  (tp-goto "交易计划模板"))

(defun tradeplan ()
  "交易计划模板"
  (interactive)
  (init-time-frame-vars)
  (init-tplan-vars)
  (load forex-el)
  ;; (dump-vars-to-file '(time-frame-vars tplan-vars) forex-el)
  (switch-to-buffer tp-buffer-name)
  (tp-goto "交易计划模板"))

(define-derived-mode tp-mode nil "交易计划模板 mode"
  "Widget demo.
\\{widget-demo-mode-map}"
  (make-local-variable 'tp-form)
  (make-local-variable 'tp-anchors))

;; important function
(defun tp-goto (link)
  (interactive
   (list (completing-read "Goto: " tp-list nil t)))
  (switch-to-buffer tp-buffer-name)
  (tp-mode)
  (setq link (split-string link "#"))
  (let* ((inhibit-read-only t)
         (name (car link))
         (anchor (cadr link))
         (page (assoc name tp-list)))
    (erase-buffer)
    (remove-overlays)
    (setq tp-current name)
    ;; insert buttons
    (let ((links (tp-resolve-link name))
          (label '("Next" "交易计划模板" "Prev")))
      (dolist (link links)
        (when link
          (widget-create 'push-button
                         :format
                         (if (string= (car label) "交易计划模板")
                             "%[交易计划模板%]"
                           (format "%%t: %%[%s%%]" (car link)))
                         :button-face 'info-xref
                         :tag (car label)
                         :notify (lambda (wid &rest ignore)
                                   (tp-goto (widget-value wid)))
                         (car link))
          (widget-insert "  "))
        (setq label (cdr label))))
    ;; insert title 
    (widget-insert "\n\n ")
    (widget-insert
     (propertize
      (or (plist-get page :header) (car page))
      'face 'info-title-1))
    (widget-insert "\n\n")
    (funcall (cadr page))
    ;; if there is an anchor, jump to the anchor
    (if (and anchor
             (setq anchor (assoc-default anchor tp-anchors)))
        (goto-char anchor)
      (goto-char (point-min)))
    (widget-setup)
    (use-local-map tp-mode-map)))

(defun tp-next ()
  (interactive)
  (let ((links (tp-resolve-link tp-current)))
    (if (car links)
        (tp-goto (caar links))
      (message "No next pages!"))))

(defun tp-previous ()
  (interactive)
  (let ((links (tp-resolve-link tp-current)))
    (if (nth 2 links)
        (tp-goto (car (nth 2 links)))
      (message "No previous pages!"))))


(defun tp-goto-page ()
  (interactive)
  (let ((num (- last-command-event ?0)))
    (if (< num (length tp-list))
        (tp-goto (car (nth num tp-list)))
      (message "Only %d pages!" (length tp-list)))))

(defun tp-reflesh ()
  (interactive)
  (tp-goto tp-current))

(defun tp-show-source ()
  (interactive)
  (let ((page (assoc tp-current tp-list)))
    (with-selected-window
        (display-buffer
         (find-file-noselect (find-library-name "tp")))
      (imenu (symbol-name (cadr page)))
      (recenter 1))))

;;}}}
(defun tp-reset ()
  (interactive)
  ;; (unload-feature 'tradeplan) 
  (load-file "~/.emacs.d/tp/tradeplan.el")
  (kill-buffer "*交易计划模板*")
  (tradeplan)
)
;;; Pages
(defun tp-contents ()
  (interactive)
  (let ((idx 1))
    (dolist (page (cdr tp-list))
      (widget-insert (format "%3d. " idx))
      (widget-create 'link
                     :format "%[%t%]"
                     :tag (or (plist-get page :header) (car page))
                     :button-prefix ""
                     :button-suffix ""
                     :notify (lambda (widget &rest ignore)
                               (tp-goto (widget-value widget)))
                            
		     (car page))
      (widget-insert "\n")
      (setq idx (1+ idx)))))

(defun tp-os-matrix-print(cur-sym)
  (widget-insert "   ---------------" cur-sym "---------------------\n tf   | ")
  (dolist (tfi time-frame)
    (widget-insert (format "%s | " (plist-get (assoc tfi time-frame-vars) :name))))
  (widget-insert "\n   ------------------------------------\n 客 : ")
  (dolist (tfi time-frame)
    (tp-create-anchor (concat cur-sym "-" tfi "-obj" ))
    (widget-create 'link
		   :notify `(lambda (widget &rest ignore)
			      (let ((choosed (widget-choose ,(concat cur-sym "-" tfi "-obj") '((上 . 上) (下 . 下) (横 . 横) (转换 . 转)))))
				(tpvar-update ,(concat cur-sym "-" tfi) :obj choosed)
				(tp-goto ,(concat tp-current "#" cur-sym "-" tfi "-obj"))))
		   (format " %s " (tpvar-get (concat cur-sym "-" tfi) :obj))
		   (widget-insert "|")))

  (widget-insert "\n 主 : ")
  (dolist (tfi time-frame)
    (tp-create-anchor (concat cur-sym "-" tfi "-sub" ))
    (widget-create 'link
		   :notify `(lambda (widget &rest ignore)
			      (let ((choosed (widget-choose ,(concat cur-sym "-" tfi "-sub") '((上 . 上) (下 . 下) (看不懂 . 星)))))
				(tpvar-update ,(concat cur-sym "-" tfi) :sub choosed)
				(tp-goto ,(concat tp-current "#" cur-sym "-" tfi "-sub")))) 
		   (format " %s " (tpvar-get (concat cur-sym "-" tfi) :sub))
		   (widget-insert "|")))
  (widget-insert "\n   ------------------------------------\n\n")
  )


(defun tp-usdx-summary-editor()
  "市场整体情况的结论"
  (dolist-if (tfi time-frame)
	     (or (string= tfi "4hr") (string= tfi "1hr") (string= tfi "15m") (string= tfi "day"))
	     (progn (widget-create 'editable-field
				   :size 50
				   :format (concat "美元(" tfi ")指数: %v " )
				   :notify `(lambda (widget &rest ignore)
					     (tpvar-update ,(concat "usdx-" tfi) :sum (widget-value widget )))
				   (tpvar-get (concat "usdx-" tfi) :sum)
				   )
		    (widget-insert "\n"))
	     ))

(defun tp-usdx-market-diff-view()
  "市场分化,与规范性筛选"
  (dolist (tfi '("4hr" "1hr" "15m"))
    (widget-insert " \n  ------------------------------------\n" tfi ":客:")
    (dolist-if (fxs forex-symbol)
	       (not (string= fxs "usdx"))
	       (progn
		 (tp-create-anchor (concat fxs "-" tfi "-obj" ))
		 (widget-create 'link
				:notify `(lambda (widget &rest ignore)
					   (let ((choosed (widget-choose ,(concat fxs "-" tfi "-obj") '((上 . 上) (下 . 下) (横 . 横) (转换 . 转)))))
					     (tpvar-update ,(concat fxs "-" tfi) :obj choosed)
					     (tp-goto ,(concat tp-current "#" fxs "-" tfi "-obj"))))
				(format "%s:   %s  " fxs (tpvar-get (concat fxs "-" tfi ) :obj)))

		 (widget-insert " ")))
    (widget-insert " \n" tfi ":主:")
    (dolist-if (fxs forex-symbol)
	       (not (string= fxs "usdx"))
	       (progn
		 (tp-create-anchor (concat fxs "-" tfi "-sub" ))
		 (widget-create 'link
				:notify `(lambda (widget &rest ignore)
					   (let ((choosed (widget-choose ,(concat fxs "-" tfi "-sub") '((上 . 上) (下 . 下) (看不清 . 星)))))
					     (tpvar-update ,(concat fxs "-" tfi) :sub choosed)
					     (tp-goto ,(concat tp-current "#" fxs "-" tfi "-sub"))))
				(format "%s:   %s  " fxs (tpvar-get (concat fxs "-" tfi ) :sub)))

		 (widget-insert " ")))
    (widget-insert " \n" tfi ":规:")
    (dolist-if (fxs forex-symbol)
	       (not (string= fxs "usdx"))
	       (progn
		 (tp-create-anchor (concat fxs "-" tfi "-gfx" ))
		 (widget-create 'link
				:notify `(lambda (widget &rest ignore)
					   (let ((choosed (widget-choose ,(concat fxs "-" tfi "-gfx") '((已经有中继或者次的迹象 . "zc") (已经有不规范的次的迹象 . "cc") (暂时还没有中继或者次的迹象 . "nc") (短时间内不太可能形成次 . "fc")))))
					     (tpvar-update ,(concat fxs "-" tfi) :gfx choosed)
					     (tp-goto ,(concat tp-current "#" fxs "-" tfi "-gfx"))))
				(format "%s:   %s  " fxs (tpvar-get (concat fxs "-" tfi ) :gfx)))

		 (widget-insert " ")))
    (widget-insert " \n" tfi ":撑:")
    (dolist-if (fxs forex-symbol)
	       (not (string= fxs "usdx"))
	       (progn
		 (tp-create-anchor (concat fxs "-" tfi "-cheng" ))
		 (widget-create 'link
				:notify `(lambda (widget &rest ignore)
					   (let ((price (completing-read "支撑:" nil nil nil)))
					     (tpvar-update ,(concat fxs "-" tfi) :cheng price)
					     (tp-goto ,(concat tp-current "#" fxs "-" tfi "-cheng"))))
				(format "%s:%.4f " fxs (tpvar-get-float (concat fxs "-" tfi ) :cheng)))

		 (widget-insert " ")))

    (widget-insert " \n" tfi ":阻:")
    (dolist-if (fxs forex-symbol)
	       (not (string= fxs "usdx"))
	       (progn
		 (tp-create-anchor (concat fxs "-" tfi "-zu" ))
		 (widget-create 'link
				:notify `(lambda (widget &rest ignore)
					   (let ((price (completing-read "阻力:" nil nil nil)))
					     (tpvar-update ,(concat fxs "-" tfi) :zu price)
					     (tp-goto ,(concat tp-current "#" fxs "-" tfi "-zu"))))
				(format "%s:%.4f " fxs (tpvar-get-float (concat fxs "-" tfi ) :zu)))

		 (widget-insert " ")))


    ))

(defun tp-usdx-diff-summary-editor()
  "各货币分化情况描述"
  (dolist-if (tfi time-frame)
	     (or (string= tfi "4hr") (string= tfi "1hr") (string= tfi "15m"))
	     (progn (widget-create 'editable-field
				   :size 50
				   :format (concat  tfi "分化: %v " )
				   :notify `(lambda (widget &rest ignore)
					     (tpvar-update ,(concat "usdx-" tfi) :dsum (widget-value widget ))))
		    (widget-insert "\n"))
	     ))

(defun tp-usdx ()
  (widget-insert "*美元指数分析\n")
  (tp-os-matrix-print "usdx")
  (widget-insert "*结论\n\n")
  (tp-usdx-summary-editor)
  (widget-insert "\n\n*货币分化表\n")
  (tp-usdx-market-diff-view)
  (widget-insert "\n\n*分化结论\n\n")
  (tp-usdx-diff-summary-editor)
)

(defun tp-fselect-qr()

  (dolist-if (fxs forex-symbol)
	     (not (string= fxs "usdx"))
	     (progn
	       (tp-create-anchor (concat fxs "-qrtag" ))
	       (widget-create 'link
			      :notify `(lambda (widget &rest ignore)
					 (let ((choosed (widget-choose ,(concat fxs "-qr") '(("" . "4hr") ("1小时" . "1hr") ("15分钟" . "15m")))))
					    (if (string= (tpvar-get (concat ,fxs "-" choosed) :qr) "select")
						(tpvar-update (concat ,fxs "-" choosed) :tsel "NA")
					      (tpvar-update (concat ,fxs "-" choosed) :tsel "select"))
					   (tp-goto ,(concat tp-current "#" fxs "-tsel"))))
			      (format "%s" fxs ))
	       (widget-insert " ")))

  (widget-create 'editable-field
		 :size 50
		 :format (concat  "** 强势货币: %v " )
		 :notify `(lambda (widget &rest ignore)
			    (tpvar-update ,(concat "usdx-1hr") :qiang (widget-value widget ))))
  (widget-create 'editable-field
		 :size 50
		 :format (concat  "\n** 中等货币: %v " )
		 :notify `(lambda (widget &rest ignore)
			    (tpvar-update ,(concat "usdx-1hr") :zhong (widget-value widget ))))
  (widget-create 'editable-field
		 :size 50
		 :format (concat  "\n** 弱势货币: %v " )
		 :notify `(lambda (widget &rest ignore)
			    (tpvar-update ,(concat "usdx-1hr") :ruo (widget-value widget ))))
  )

(defun tp-fselect-gf()
  "市场规范性选择"
  (dolist (tfi '("4hr" "1hr" "15m"))
    (widget-insert " \n  ------------------------------------\n" tfi ":规范性:\n")
    (dolist (gfx '(("zc" . "已经有中继或者次的迹象") 
		   ("cc" . "已经有不规范的次的迹象") 
		   ;; ("nc" . "暂时还没有中继或者次的迹象") 
		   ;; ("fc" . "短时间内不太可能形成次") 
		   ("NA" . "未更新规范性")))
      (widget-insert (cdr gfx) ":")
      (dolist (fxs forex-symbol)
	(if (string= (tpvar-get (concat fxs "-" tfi) :gfx) (car gfx))
	    (widget-insert "[" fxs "]")
	    ))
	(widget-insert "\n")))
  (widget-insert " \n  ------------------------------------\n"))

(defun tp-fselect()
  (widget-insert "*交易币种初步选择\n\n")
  (tp-fselect-qr)
  (widget-insert "\n\n*规范性选择\n")
  (tp-fselect-gf)
  )

(defun tp-tselected()
  (widget-insert "* 请选择要交易的货币\n\n")
  (dolist-if (fxs forex-symbol)
	     (not (string= fxs "usdx"))
	     (progn
	       (tp-create-anchor (concat fxs "-tsel" ))
	       (widget-create 'link
			      :notify `(lambda (widget &rest ignore)
					 (let ((choosed (widget-choose ,(concat fxs "-tsel") '(("4小时" . "4hr") ("1小时" . "1hr") ("15分钟" . "15m")))))
					    (if (string= (tpvar-get (concat ,fxs "-" choosed) :tsel) "select")
						(tpvar-update (concat ,fxs "-" choosed) :tsel "NA")
					      (tpvar-update (concat ,fxs "-" choosed) :tsel "select"))
					   (tp-goto ,(concat tp-current "#" fxs "-tsel"))))
			      (format "%s" fxs ))
	       (widget-insert " ")))
  (dolist (tfi '("4hr" "1hr" "15m"))
    (dolist-if (fxs forex-symbol)
	       (string= (tpvar-get (concat fxs "-" tfi) :tsel) "select")
	       (progn
		 (widget-insert "\n\n* 选择货币级别 " fxs "-" tfi "\n")
		 (tp-os-matrix-print fxs)
		)
	       ))
   )

(provide 'tradeplan)
