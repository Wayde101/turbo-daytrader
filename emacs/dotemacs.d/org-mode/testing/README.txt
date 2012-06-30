                           Org-mode Testing
                           ================

Author: Ting Yu <yanzhuang@taobao.com>
Date: 2011-08-27 10:58:52 CST


The following instructions describe how to get started using the
Org-mode test framework.

Table of Contents
=================
1 To run the tests interactively 
2 To run the tests in batch mode 


1 To run the tests interactively 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1) Install the jump.el testing dependency which is included as a git
   submodule in the org-mode repository.  To do so run the following
   git submodule commands from inside the base of the Org-mode
   directory (or just execute the following code block).

  cd ..
  git submodule init
  git submodule update


2) Load the [org-test.el] file
  (load-file "org-test.el")


3) The `org-test-jump' command is now bound to `M-C-j' in all
   emacs-lisp files.  Call this command from any file in the `lisp/'
   directory of the org-mode repository to jump to the related test
   file in the `testing/' directory.  Call this functions with a
   prefix argument, and the corresponding test file will be stubbed
   out if it doesn't already exist.

4) Ingest the library-of-babel.org file since some tests require this.
  (org-babel-lob-ingest "../contrib/babel/library-of-babel.org")


5) [Review the ERT documentation] 

6) A number of org-mode-specific functions and macros are provided in
   `org-test.el' see the [;;; Functions for Writing Tests] subsection of
   that file.  Some of these functions make use of example org-mode
   files located in the [examples/] directory.

7) Functions for loading and running the Org-mode tests are provided
   in the [;;; Load and Run Tests] subsection, the most important of
   which are
   - `org-test-load' which loads the entire Org-mode test suite
   - `org-test-current-defun' which runs all tests for the current
     function around point (should be called from inside of an
     Org-mode elisp file)
   - `org-test-run-all-tests' which runs the entire Org-mode test suite
   - also note that the `ert' command can also be used to run tests

8) Load and run all tests
  (load-file "org-test.el")
  (org-babel-lob-ingest "../contrib/babel/library-of-babel.org")
  (org-test-load)
  (org-test-run-all-tests)



  [org-test.el]: file:org-test.el
  [Review the ERT documentation]: info:ert#Top
  [;;; Functions for Writing Tests]: file:org-test.el::%3B%3B%3B%20Functions%20for%20writing%20tests
  [examples/]: file:examples
  [;;; Load and Run Tests]: file:org-test.el::%3B%3B%3B%20Load%20and%20Run%20tests

2 To run the tests in batch mode 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
First tangle this file out to your desktop.
  ;; add to the load path
  (add-to-list 'load-path (concat org-dir "/lisp/"))
  (add-to-list 'load-path (concat org-dir "/lisp/testing/"))
  (add-to-list 'load-path (concat org-dir "/lisp/testing/ert/"))
  
  ;; load Org-mode
  (require 'org)
  
  ;; setup the ID locations used in tests
  (require 'org-id)
  (org-id-update-id-locations
   (list (concat org-dir "/testing/examples/babel.org")
         (concat org-dir "/testing/examples/normal.org")
         (concat org-dir "/testing/examples/ob-awk-test.org")
         (concat org-dir "/testing/examples/ob-fortran-test.org")
         (concat org-dir "/testing/examples/link-in-heading.org")
         (concat org-dir "/testing/examples/links.org")))
  
  ;; ensure that the latest Org-mode is loaded
  (org-reload)
  
  ;; load the test suite
  (load-file (concat org-dir "/testing/org-test.el"))
  
  ;; configure Babel
  (org-babel-lob-ingest (concat org-dir "/contrib/babel/library-of-babel.org"))
  (org-babel-do-load-languages
   'org-babel-load-languages
   '((emacs-lisp . t)
     (sh . t)))
  (setq org-confirm-babel-evaluate nil)
  
  ;; run the test suite
  (org-test-run-all-tests)
  
  ;; print the results
  (with-current-buffer "*ert*"
    (print (buffer-string)))


Then run the test suite with the following command which could use any
version of Emacs.
  emacs --batch -Q -l ~/Desktop/run-org-tests.el

