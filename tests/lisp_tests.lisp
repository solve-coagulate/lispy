(define run-test
  (lambda (name expr verbose)
    (if expr
        (progn (if verbose (print name (quote PASS)) nil) 0)
        (progn (print name (quote FAIL)) 1))))

(define verbose 1)

(define length
  (lambda (xs)
    (if (null? xs) 0 (+ 1 (length (cdr xs))))) )

(define sum
  (lambda (xs)
    (if (null? xs) 0 (+ (car xs) (sum (cdr xs))))) )

(define tests
  (list
    (run-test (quote addition) (= (+ 1 1) 2) verbose)
    (run-test (quote car) (= (car (list 1 2 3)) 1) verbose)
    (run-test (quote cdr) (= (cdr (list 1 2 3)) (list 2 3)) verbose)
    (run-test (quote cons) (= (cons 1 (list 2 3)) (list 1 2 3)) verbose)
    (run-test (quote lambda) (= ((lambda (x) (+ x 1)) 2) 3) verbose)
    (run-test (quote if) (= (if (> 2 1) 42 0) 42) verbose)
    (run-test (quote null) (null? (cdr (list 1))) verbose)
    (run-test (quote list?) (list? (list 1 2)) verbose)
    (run-test (quote quote) (= (quote (1 2 3)) (list 1 2 3)) verbose)
    (run-test
      (quote macro)
      (= (progn
           (defmacro when (test body)
             (list (quote if) test body nil))
           (when (> 2 1) 5))
         5)
      verbose)))

(define total (length tests))
(define failures (sum tests))

(print total (quote tests) (quote run)
      (- total failures) (quote passed) failures (quote failed))
(if (= failures 0) 0 1)
