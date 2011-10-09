(require 'python)

(add-search-path "virtualenv")
(require 'virtualenv)
(setq virtualenv-root-dir (concat user-home-dir "/.python2"))
(virtualenv-activate "")
(setq virtualenv-use-ipython nil)
(setenv "PYMACS_PYTHON" (virtualenv-get-interpreter virtualenv-active))
;; }}
(message (getenv "PYMACS_PYTHON"))

(setq interpreter-mode-alist
      (cons '("python" . python-mode) interpreter-mode-alist)
      python-mode-hook
      '(lambda () (progn
                    (set (make-local-variable 'py-indent-offset) 4)
                    (set (make-local-variable 'py-smart-indentation) nil)
                    (set (make-local-variable 'indent-tabs-mode) nil)
                    (set (make-local-variable 'compilation-scroll-output) nil)
                    (ysl/turn-on-line-exceed-detection 'python-mode)
                    (define-key python-mode-map "\C-m" 'newline-and-indent)
                    (add-to-list 'ac-sources 'ac-source-ropemacs)
                    ;; Adding hook to automatically open a rope project if
                    ;; there is one in the current or in the upper level
                    ;; directory
                    ;; (python-auto-fill-comments-only)
                    (cond ((file-exists-p ".ropeproject")
                           (rope-open-project default-directory))
                          ((file-exists-p "../.ropeproject")
                           (rope-open-project (concat default-directory ".."))))
                    )
         )
      )

(add-search-path "pymacs")
(autoload 'pymacs-apply "pymacs")
(autoload 'pymacs-call "pymacs")
(autoload 'pymacs-eval "pymacs" nil t)
(autoload 'pymacs-exec "pymacs" nil t)
(autoload 'pymacs-load "pymacs" nil t)

;; Initialize Rope
(setq ropemacs-enable-shortcuts nil)
;(setq ropemacs-local-prefix "C-c C-p")
(pymacs-load "ropemacs" "rope-")
(ac-ropemacs-initialize)

;; Stops from erroring if there's a syntax err
(setq ropemacs-codeassist-maxfixes 3)
(setq ropemacs-guess-project t)
(setq ropemacs-enable-autoimport t)

; compile python code {{
(defun compile-python ()
  "Use compile to run python programs"
  (interactive)
  (compile (concat (virtualenv-get-interpreter virtualenv-active) " " (buffer-file-name))))
(define-key python-mode-map (kbd "C-c C-c") 'compile-python)
;; }}

;; Autofill inside of comments
(defun python-auto-fill-comments-only ()
  (auto-fill-mode 1)
  (set (make-local-variable 'fill-nobreak-predicate)
       (lambda ()
         (not (python-in-string/comment)))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Auto-completion
;;;  Integrates:
;;;   1) Rope
;;;   2) Yasnippet
;;;   all with AutoComplete.el
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun prefix-list-elements (list prefix)
  (let (value)
    (nreverse
     (dolist (element list value)
       (setq value (cons (format "%s%s" prefix element) value))))))

(defvar ac-source-rope
  '((candidates
     . (lambda ()
         (prefix-list-elements (rope-completions) ac-target))))
  "Source for Rope")

(defun ac-python-find ()
  "Python `ac-find-function'."
  (require 'thingatpt)
  (let ((symbol (car-safe (bounds-of-thing-at-point 'symbol))))
    (if (null symbol)
        (if (string= "." (buffer-substring (- (point) 1) (point)))
            (point)
          nil)
      symbol)))

(defun ac-python-candidate ()
  "Python `ac-candidates-function'"
  (let (candidates)
    (dolist (source ac-sources)
      (if (symbolp source)
          (setq source (symbol-value source)))
      (let* ((ac-limit (or (cdr-safe (assq 'limit source)) ac-limit))
             (requires (cdr-safe (assq 'requires source)))
             cand)
        (if (or (null requires)
                (>= (length ac-target) requires))
            (setq cand
                  (delq nil
                        (mapcar (lambda (candidate)
                                  (propertize candidate 'source source))
                                (funcall (cdr (assq 'candidates source)))))))
        (if (and (> ac-limit 1)
                 (> (length cand) ac-limit))
            (setcdr (nthcdr (1- ac-limit) cand) nil))
        (setq candidates (append candidates cand))))
    (delete-dups candidates)))

(add-hook 'python-mode-hook
          (lambda ()
            (set (make-local-variable 'ac-sources)
                 (append ac-sources '(ac-source-yasnippet ac-source-rope)))
            (set (make-local-variable 'ac-find-function) 'ac-python-find)
            (set (make-local-variable 'ac-candidate-function) 'ac-python-candidate)))
;;            (set (make-local-variable 'ac-auto-start) nil)))


;; slow don't know why
;; ;; load flymake {{
;; (add-search-path "misc")
;; (load-library "flymake-cursor")
;; (setq flymake-extension-use-showtip t)
;; (setq flymake-allowed-file-name-masks
      ;; '(("\\.p[ml]\\'" flymake-perl-init))
;; )
;; (delete '("\\.html?\\'" flymake-xml-init) flymake-allowed-file-name-masks)
;; ;; }}



;; ;; setup flymake {{
;; (add-hook 'find-file-hook 'flymake-find-file-hook)
;; (when (load "flymake" t)
  ;; (defun flymake-pyflakes-init ()
    ;; (let* ((temp-file (flymake-init-create-temp-buffer-copy
                       ;; 'flymake-create-temp-inplace))
           ;; (local-file (file-relative-name
                        ;; temp-file
                        ;; (file-name-directory buffer-file-name))))
      ;; (list "pycheckers"  (list local-file))))
  ;; (add-to-list 'flymake-allowed-file-name-masks
               ;; '("\\.py\\'" flymake-pyflakes-init)))

;; (add-hook 'python-mode-hook
          ;; (lambda ()
            ;; (unless (eq buffer-file-name nil) (flymake-mode 1))
            ;; (local-set-key [f10] 'flymake-goto-prev-error)
            ;; (local-set-key [f11] 'flymake-goto-next-error)
            ;; ))
;; ;; }}

(provide 'python-init)






