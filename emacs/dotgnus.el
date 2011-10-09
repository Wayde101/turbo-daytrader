(load-library "smtpmail")
(load-library "nnimap")
(load-library "starttls")
;; server settings
(setq gnus-select-method '(nnimap "www.17forex.com"
           (nnimap-address "www.17forex.com")
            (nnimap-server-port 55143)
           ;;(nnimap-server-port 993)
           ;; (nnimap-authinfo-file "~/.imap-authinfo")
           ;; (nnimap-stream ssl)))
              ))
(setq message-send-mail-function 'smtpmail-send-it)
(add-to-list 'gnus-secondary-select-methods '(nntp "news.cn99.com"))

;; view settings
(add-to-list 'mm-attachment-override-types "image/.*")
(setq w3m-default-display-inline-images t)
(setq mm-inline-text-html-with-images t)



;; sort articles in reverse date
(setq gnus-article-sort-functions
      '(gnus-article-sort-by-subject
        (not gnus-article-sort-by-date)))

;; Make Gnus NOT ignore [Gmail] mailboxes
(setq gnus-ignored-newsgroups "^to\\.\\|^[0-9. ]+\\( \\|$\\)\\|^[\"]\"[#'()]")

;; override personal information
(setq gnus-posting-styles
      '(
        (".*"
                                        ; (signature-file "~/emacs/gnus/.signature_english") 
          (name "于霆")
           (address "yanzhuang@taobao.com"))
        ))

;; cn.bbs.* charset fix
(setq gnus-parameters
      (nconc
       ;; Some charsets are just examples! 
       '(("\\bcn\\.bbs\\..*" ;; Chinese 
            (mm-coding-system-priorities
                '(iso-8859-1 gbk utf-8))))
       gnus-parameters))

(setq gnus-treat-fill t)
