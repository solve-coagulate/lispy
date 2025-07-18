(define total 0)
(define failures 0)

(define run-test
  (lambda (name expr verbose)
    (progn
      (set! total (+ total 1))
      (if expr
          (if verbose (print name (quote PASS)) nil)
          (progn (print name (quote FAIL))
                 (set! failures (+ failures 1))
                 nil))))
)

(define verbose 1)

(run-test (quote addition) (= (+ 1 1) 2) verbose)
(run-test (quote car) (= (car (list 1 2 3)) 1) verbose)

(print total (quote tests) (quote run) (- total failures) (quote passed) failures (quote failed))
(if (= failures 0) 0 1)
