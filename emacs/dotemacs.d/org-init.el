(provide 'org-init)

(setq load-path (add-to-list 'load-path "~/.emacs.d/org-mode/lisp"))
(require 'org-install)
(add-to-list 'auto-mode-alist '("\\.org$" . org-mode))
(define-key global-map "\C-cl" 'org-store-link)
(define-key global-map "\C-ca" 'org-agenda)
(setq org-log-done t)
(setq org-fontify-emphasized-text t
      org-descriptive-links nil
      org-agenda-include-diary nil
      org-agenda-start-on-weekday nil
      org-agenda-include-all-todo t
      org-agenda-include-all-deadline t
      org-startup-folded nil
      org-log-done t
      org-agenda-skip-deadline-if-done t
      org-agenda-skip-scheduled-if-done t
      org-agenda-repeating-timestamp-show-all t
      org-agenda-show-all-dates t
      org-hide-leading-stars t
      org-use-fast-todo-selection t
      )


(setq org-agenda-files (list "~/org/todolist.org"
			     "~/org/memo-tasks.org"
			     "~/org/someday.org"
			     ))
(add-to-list 'auto-mode-alist '("\\.\\(org\\|org_archive\\)$" . org-mode))

(setq org-todo-keywords
      '((sequence "TODO(t)" "WAITING(w)" "NOW(n)" "|" "DONE(d)" "ABORT(a)")))

;; Change task state to STARTED when clocking in
(setq org-clock-in-switch-to-state "NOW")

(setq org-todo-keyword-faces
      (quote (("TODO" :background "blue" :weight bold)
	      ("WAITING" :background "green" :foreground "blue" :weight bold)
	      ("NOW" :background "red" :weight bold)
	      )))

;; Resume clocking tasks when emacs is restarted
(setq org-clock-persistence-insinuate)
;; Sometimes I change tasks I'm clocking quickly - this removes clocked tasks with 0:00 duration
(setq org-clock-out-remove-zero-time-clocks t)
;; Don't clock out when moving task to a done state
(setq org-clock-out-when-done nil)
;; Save the running clock and all clock history when exiting Emacs, load it on startup
(setq org-clock-persist t)

(setq org-tag-alist '(
		      ("Project" . ?p)
		      ("Writing" . ?w)
		      ("Conference" . ?c)
		      ("Lecture" . ?l)
		      ("Reading" . ?r)
		      ("Tasks" . ?t)
		      ("Misc" . ?m)
		      ))

(setq org-agenda-custom-commands
      '(
	("P" "Projects"
	 ((tags-todo "Project")
	  (tags-todo "Writing")
	  (tags-todo "Tasks")))
	("c" "DOING"
	 ((todo "NOW")))
	("h" "Office and Home Lists"
	 (;(agenda)
	  (tags-todo "Project")
	  (tags-todo "Writing")
	  (tags-todo "Conference")
	  (tags-todo "Lecture")
	  (tags-todo "Reading")
	  (tags-todo "Tasks")
	  (tags-todo "Misc")))
	("d" "Daily Action List"
	 ((agenda "" ((org-agenda-ndays 1)
		      (org-agenda-sorting-strategy
		       (quote ((agenda time-up priority-down tag-up) )))
      ))))
	("W" "Weekly Review"
         ((agenda "" ((org-agenda-ndays 7)))
          (todo "TODO")
))
	)
      )

;; Always hilight the current agenda line
(add-hook 'org-agenda-mode-hook '(lambda () (hl-line-mode 1)))

;; Sorting order for tasks on the agenda
(setq org-agenda-sorting-strategy
      (quote ((agenda time-up priority-down effort-up category-up)
              (todo priority-down)
              (tags priority-down))))



