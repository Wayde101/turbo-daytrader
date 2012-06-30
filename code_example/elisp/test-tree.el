(require 'widget)
(require 'tree-mode)



(defun widget-demo-tree-test ()
  (widget-insert "\nTree:\n")
  (widget-create
   '(tree-widget
     :node (push-button :format "%[%t%]\n" :tag "hello")
     :open t
     (push-button :format "%[%t%]\n" :tag "node1")
     (push-button :format "%[%t%]\n" :tag "node2"))))


(widget-demo-tree-test)Tree:

(widget-demo-add-page "Tree Test" 'widget-demo-tree-test)

(defvar widget-tradeplan-buffer-name "*每日交易计划*"
  "*每日交易计划")
