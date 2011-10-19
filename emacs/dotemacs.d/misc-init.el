(setq load-path (add-to-list 'load-path "~/.emacs.d/misc"))
(provide 'misc-init)
(require 'ido)
(ido-mode t)

(setq inferior-lisp-program "/usr/bin/sbcl")
(add-to-list 'load-path "/usr/share/emacs/site-lisp/slime/")
(require 'slime)
(slime-setup)


(setq user-home-dir (getenv "HOME")
      conf-root-dir (concat user-home-dir "/.emacs.d"))

(defun add-search-path (path)
  (add-to-list 'load-path (concat conf-root-dir "/" path))
  (message (concat "misc-init: load-path added: " path)))

(set-language-environment 'UTF-8) 
(set-locale-environment "UTF-8") 

(setq x-select-enable-clipboard t)
(setq interprogram-paste-function 'x-cut-buffer-or-selection-value)

;; convert text files between unix and dos
(defun dos-unix () (interactive)
(goto-char (point-min))
(while (search-forward "\r" nil t) (replace-match "")))
(defun unix-dos () (interactive)
(goto-char (point-min))
(while (search-forward "\n" nil t) (replace-match "\r\n")))


(defun runperl()
  "run perl,xxx"
  (interactive)
  ;(save-buffer)
  (let ((filename buffer-file-name)
 (cmd "")
 (oldbuf (current-buffer))
 (end (point-max)))
    (if filename
 (save-buffer)
      (save-excursion
 (setq filename (concat (getenv "tmp") "/temp.pl"))
 (set-buffer (create-file-buffer filename))
 (insert-buffer-substring oldbuf 1 end)
 (write-file filename)
 (kill-buffer (current-buffer))))
    (setq cmd (concat "perl " filename))
    (message "%s  ..." cmd)
    (shell-command cmd)))

;;(global-set-key[(meta o)] 'runperl)

(define-skeleton skeleton-perl-function
  "Insert a Perl function" "function name: "
  "# {{{ " str ": TODO" \n
  "sub " str \n
  "{" \n
  \n
  "}" \n
  "# }}}" \n)


(require 'tramp)
(setq tramp-default-method "scp") 
(setq tramp-chunksize 328)



(setq default-major-mode 'text-mode)
(global-font-lock-mode t)
(global-set-key (kbd "C-c C-w") 'copy-lines)
(defun copy-lines(&optional arg)
  (interactive "p")
  (save-excursion
    (beginning-of-line)
    (set-mark (point))
    (next-line arg)
    (kill-ring-save (mark) (point))
    )
  )


(autoload 'speedbar-frame-mode "speedbar" "Popup a speedbar frame" t)
(autoload 'speedbar-get-focus "speedbar" "Jump to speedbar frame" t) 
(define-key-after (lookup-key global-map [menu-bar tools])
  [speedbar] '("Speedbar" . speedbar-frame-mode) [calendar])
(global-set-key [(f5)] 'speedbar-get-focus)


(recentf-mode 1)
(defun recentf-open-files-compl ()
  (interactive)
  (let* ((all-files recentf-list)
         (tocpl (mapcar (function
                         (lambda (x) (cons (file-name-nondirectory x) x))) all-files))
         (prompt (append '("File name: ") tocpl))
         (fname (completing-read (car prompt) (cdr prompt) nil nil)))
    (find-file (cdr (assoc-ignore-representation fname tocpl)))))    
				   
(global-set-key [(control x)(control r)] 'recentf-open-files-compl)

(setq frame-title-format "emacs@%b")


(defun edit-hosts ()
  (interactive)
  (find-file "c:/WINDOWS/system32/drivers/etc/hosts")
)


(defun fast-compile () "Compiles without asking anything" (interactive) 
 (let ((compilation-read-command nil)) 
 (setq window-configuration-before-compilation (current-window-configuration)) 
 (setq compilation-ask-about-save nil) 
 (compile compile-command))) 

(defun comment-and-go-down ()
 "Comments the current line and goes to the next one" 
 (interactive) 
 (condition-case nil (comment-region (point-at-bol) (point-at-eol)) (error nil)) 
(next-line 1)) 

(defun open-a-new-line ()
  (interactive)
 (condition-case nil (open-line (point-at-eol)) (error nil)) 
)

(defun load-dot-emacs ()
  (interactive)
  "Load .emacs file"
  (load-file "~/.emacs")
)


(defun match-paren (arg) 
 "Go to the matching paren if on a paren; otherwise insert %." 
 (interactive "p") 
 (cond ((looking-at "\\s\(") (forward-list 1) (backward-char 1)) 
 ((looking-at "\\s\)") (forward-char 1) (backward-list 1)) 
 (t (self-insert-command (or arg 1))))) 
 

(defun uncomment-and-go-up () 
 "Uncomments the current line and goes to the previous one" 
 (interactive) 
 (condition-case nil (uncomment-region (point-at-bol) (point-at-eol)) (error nil)) 
 (next-line -1)) 


(setq auto-mode-alist (cons '("/usr/src/linux.*/.*\\.[ch]$" . linux-c-mode) auto-mode-alist))

(defun switch-to-other-buffer () (interactive) (switch-to-buffer (other-buffer)))

(defun my-print-date ()
  "prints date"
  (interactive)
  (insert (current-time-string)))

(defun ska-point-to-register()
  "Store cursorposition _fast_ in a register.
Use ska-jump-to-register to jump back to the stored
position."
  (interactive)
  (setq zmacs-region-stays t)
  (point-to-register 8))

(defun ska-jump-to-register()
  "Switches between current cursorposition and position
that was stored with ska-point-to-register."
  (interactive)
  (setq zmacs-region-stays t)
  (let ((tmp (point-marker)))
        (jump-to-register 8)
        (set-register 8 tmp)))

(define-skeleton skeleton-perl-function
  "Insert a Perl function" "function name: "
  "# {{{ " str ": TODO" \n
  "sub " str \n
  "{" \n
  \n
  "}" \n
  "# }}}" \n)

(define-skeleton perl-log-skel
  "Insert Log level" "log level: "
  "$self->log('" str "',__PACKAGE__,__LINE__,\"\");"
)

(defun wy-go-to-char (n char)
  "Move forward to Nth occurence of CHAR.
Typing `wy-go-to-char-key' again will move forwad to the next Nth
occurence of CHAR."
  (interactive "p\ncGo to char: ")
  (search-forward (string char) nil nil n)
  (while (char-equal (read-char)
                     char)
    (search-forward (string char) nil nil n))
  (setq unread-command-events (list last-input-event)))



(setq scroll-step 1
      scroll-margin 5
      scroll-conservatively 10000)

(setq user-full-name "Ting Yu")
(setq user-mail-address "yanzhuang@taobao.com")


(setq tabbar-buffer-groups-function 'tabbar-buffer-ignore-groups)
(defun tabbar-buffer-ignore-groups (buffer)
  "Return the list of group names BUFFER belongs to.
Return only one group for each buffer."
  (with-current-buffer (get-buffer buffer)
    (cond
     ((or (get-buffer-process (current-buffer))
          (memq major-mode
                '(comint-mode compilation-mode)))
      '("Process")
      )
     ((member (buffer-name)
              '("*scratch*" "*Messages*"))
      '("Common")
      )
     ((eq major-mode 'dired-mode)
      '("Dired")
      )
     ((memq major-mode
            '(help-mode apropos-mode Info-mode Man-mode))
      '("Help")
      )
     ((memq major-mode
            '(linux-c-mode c-mode
              ))
      '("C-program")
      )
     ((memq major-mode
            '(php-mode php-mode
              ))
      '("php-program")
      )
     ((memq major-mode
            '(makefile-mode
              ))
      '("Makefile-Program")
      )
     (t
      (list
       "default"  ;; no-grouping
       (if (and (stringp mode-name) (string-match "[^ ]" mode-name))
           mode-name
         (symbol-name major-mode)))
      )
     )))

(defun ysl/set-x-font () 
   (let ((fontset "fontset-default"))
   (set-default-font ysl/x-font-en) 
   (dolist (charset '(kana han symbol cjk-misc bopomofo)) 
   (set-fontset-font fontset charset ysl/x-font-zh))))
   (setq ysl/x-font-en "Consolas:size=14:weight=bold"  ysl/x-font-zh "Microsoft YaHei:size=16:weight=light")

;; (display-time)
;; ;;(unset-font)
;; ;;(setq visible-bell t)

;; ;;(desktop-load-default)
;; ;;(desktop-read)

;;(set-default-font "rk16")
(set-foreground-color "white")
(set-background-color "black")

(set-cursor-color "blue2")
(scroll-bar-mode -1)
(menu-bar-mode -1)
(tool-bar-mode -1)

;; (define-key global-map (kbd "<f9> r") 'remember)
;; (define-key global-map (kbd "<f9> R") 'remember-region)
