(provide 'slime-init)

(add-to-list 'load-path "~/.emacs.d/slime")
(require 'slime)
(add-hook 'lisp-mode-hook (lambda () (slime-mode t)))
(add-hook 'inferior-lisp-mode-hook (lambda () (inferior-slime-mode t)))
;; Optionally, specify the lisp program you are using. Default is "lisp"
(setq inferior-lisp-program "/usr/bin/sbcl") 
(slime-setup '(slime-fancy slime-asdf))

;; (add-to-list 'load-path "~/.emacs.d/slime/")  ; your SLIME directory
;; (require 'slime)
;; (require 'slime-autoloads)
;; (add-hook 'lisp-mode-hook (lambda () (slime-mode t)))
;; (add-hook 'inferior-lisp-mode-hook (lambda () (inferior-slime-mode t)))
;; (setq slime-net-coding-system 'utf-8-unix)
;; (slime-setup '(slime-repl))
;; (eval-after-load "slime"
;;   '(progn
;;     (add-to-list 'load-path "~/.emacs.d/slime/contrib")
;;     (slime-setup '(slime-fancy slime-asdf slime-banner))
;;     (setq lisp-indent-function 'common-lisp-indent-function)
;;     (setq slime-complete-symbol*-fancy t)
;;     (setq slime-startup-animation t)
;;     (setq slime-complete-symbol-function 'slime-fuzzy-complete-symbol)))
;; (setq inferior-lisp-program "/usr/local/bin/sbcl") ; your Lisp system
;; Optionally, specify the Lisp program you are using. Default is "lisp"
;; If the Allegro directory is not in your PATH environment variable
;; this should be a fully qualified path.
;; choose one of the below based on Express or non-Express usage
;; (setq inferior-lisp-program "alisp") 

