;;;###autoload
(require 'compile)

(add-to-list 'auto-mode-alist '("\\.mq4\\'" . mql-mode))

(defvar mql-mode-hook nil)

(add-hook 'mql-mode-hook
           (lambda ()
	          (unless (file-exists-p "Makefile")
		           (set (make-local-variable 'compile-command)
				(let ((file (file-name-nondirectory buffer-file-name)))
                      (format "%s %s %s"
                              (or (getenv "WINE") "/usr/bin/wine")
                              (or (getenv "METALANG") "/home/yuting/MinGW/msys/1.0/home/yuting/Alpari/MetaLang.exe")
			            file))))))


(defun mql-mode ()
  "Major mode for editing MQL file."
  (interactive)
  (kill-all-local-variables)
  (c-mode)
  (setq major-mode 'mql-mode)
  (setq mode-name "MQL")
  (run-hooks 'mql-mode-hook))


(provide 'mql-mode)
