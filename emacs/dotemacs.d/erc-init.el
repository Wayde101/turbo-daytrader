(require 'erc)
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
