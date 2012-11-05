(provide 'ibus-init)

(setq load-path (add-to-list 'load-path "~/.emacs.d/ibus-el-0.2.1"))
(require 'ibus)
(add-hook 'after-init-hook 'ibus-mode-on)
(setq ibus-agent-file-name "~/.emacs.d/ibus-el-0.2.1/ibus-el-agent")

