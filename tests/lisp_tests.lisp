(define run-test
  (lambda (name expr verbose)
    (if expr
        (progn (if verbose (print name (quote PASS)) nil) 0)
        (progn (print name (quote FAIL)) 1))))

(define verbose 1)

(define failures
  (+ (run-test (quote addition) (= (+ 1 1) 2) verbose)
     (run-test (quote car) (= (car (list 1 2 3)) 1) verbose)))

(define total 2)

(print total (quote tests) (quote run) (- total failures) (quote passed) failures (quote failed))
(if (= failures 0) 0 1)
