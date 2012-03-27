(provide 'global-key-init)

(global-set-key [(shift f6)] 'redo)
(global-set-key [(f6)] 'undo)
;; (global-set-key "\C-cx" 'cscope-find-this-symbol)
;(global-set-key "\C-xp" 'my-print-date)
(global-set-key "\C-xp" 'perl-log-skel)
(global-set-key "\C-cg" 'goto-line)
(global-set-key "\C-ch" 'headerize)
(global-set-key "\M-s" 'other-window)
(global-set-key "%" 'match-paren)
;; (define-key global-map (kbd "C-c a") 'wy-go-to-char)
(global-set-key [(control ?\.)] 'ska-point-to-register)
(global-set-key [(control ?\,)] 'ska-jump-to-register)
(define-key global-map [(meta control tab)] 'switch-to-other-buffer)
(define-key global-map [(control =)] 'comment-and-go-down) ;make a line became comment
(define-key global-map [(control +)] 'uncomment-and-go-up) ;make a line became comment
(define-key global-map [(control \#)] 'c-func-comment)
(define-key global-map [(control \$)] 'c-file-comment)
(define-key global-map [f2] 'next-error) 
(define-key global-map [f1] 'fast-compile)
(global-set-key [S-f5] 'eshell)
(global-set-key [(f4)] (lambda () (interactive) (manual-entry (current-word))))

