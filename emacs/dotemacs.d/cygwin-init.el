(provide 'cygwin-init)
(require 'cygwin-mount)

(setenv "PATH" (concat "d:/cygwin/bin;" (getenv "PATH")))
(setq exec-path (cons "d:/cygwin/bin/" exec-path))
(cygwin-mount-activate) 
(add-hook 'comint-output-filter-functions  'shell-strip-ctrl-m nil t)
(add-hook 'comint-output-filter-functions  'comint-watch-for-password-prompt nil t)
(setq explicit-shell-file-name "bash.exe")
;; For subprocesses invoked via the shell
;; (e.g., "shell -c command")
(setq shell-file-name explicit-shell-file-name) 
