(require 'erc)
(setq erc-log-channels-directory "~/.erc/logs/")
(setq erc-save-buffer-on-part t)
(setq erc-log-insert-log-on-open nil)
(setq erc-hide-timestamps t)
(defadvice save-buffers-kill-emacs (before save-logs (arg) activate)
(save-some-buffers t (lambda () (when (eq major-mode 'erc-mode) t))))

(defun myerc-join-channels (&rest channels)
  (mapc 'erc-join-channel channels))
(defun myerc-autojoin-channels (server nick)
  (cond
   ((member erc-session-server '("opsirc.corp.taobao.com"))
    (myerc-join-channels "#jumbo"))
   ((string= erc-session-server "irc.debian.org")
    (myerc-join-channels "#emacs" ))))

(add-hook 'erc-after-connect 'myerc-autojoin-channels)

(defconst erc-default-server "opsirc.corp.taobao.com"
  "IRC server to use if it cannot be detected otherwise.")

(provide 'erc-init)
