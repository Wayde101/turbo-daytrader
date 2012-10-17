(defvar *rcdb* nil)

(defun new-word (word pron meaning)
  (list :word word :pron pron :meaning meaning))

(defun add-word (word) (push word *rcdb*))

(add-word (new-word "tree" "tri:" "n.树"))
(add-word (new-word "besides" "bi'saidz" "adv.此外"))
