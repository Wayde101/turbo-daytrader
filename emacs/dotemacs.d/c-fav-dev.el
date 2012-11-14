(provide 'c-fav-dev)

;; (mouse-avoidance-mode 'animate)
(defun c-func-comment ()
 ;; Insert a c function header comment at the cursor position 
 (interactive) 
 (insert 
"/** 
 * Name: 
 * Func:
 * Parameter:
 * Return:
 * Date:
 */
")
 (previous-line 2) 
 (end-of-line)) 

(defun c-file-comment () 
 ;; Insert a c function header comment at the cursor position 
 (interactive) 
 (insert 
"/** 
 * Company Name :yahoo
 * Project Name :none
 * Source  Name :  
 * Object  Name : .o
 * Description  :
 * Programer    :tingyu
 * ReProgramer  :
 * Date         :
 */
")
 (previous-line 7) 
 (end-of-line)) 



(defun headerize () "Adds the #define HEADER_H, etc." (interactive) 
 (let ((flag-name (replace-regexp-in-string "\\." "_" (upcase (file-name-nondirectory (buffer-name)))))) 
 (goto-char (point-max)) 
 (insert (concat "#endif   /*_"flag-name"_*/\n")) 
 (goto-char (point-min)) 
 (insert (concat "#ifndef _" flag-name "_\n")) 
 (insert (concat "#define _" flag-name "_\n\n")) 
 ) 
) 

(defun add-para () "Adds the para." (interactive) 
 (let ((flag-name (replace-regexp-in-string "\\." "_" (upcase (file-name-nondirectory (buffer-name)))))) 
 (goto-char (point-max)) 
 (insert (concat "#endif   /*_"flag-name"_*/\n")) 
 (goto-char (point-min)) 
 (insert (concat "#ifndef _" flag-name "_\n")) 
 (insert (concat "#define _" flag-name "_\n\n")) 
 ) 
) 

