(define failures 0)

(define run-test
  (lambda (name expr)
    (if expr
        (progn (print name (quote PASS)) nil)
        (progn (print name (quote FAIL))
               (define failures (+ failures 1))
               nil)))
)

(run-test (quote addition) (= (+ 1 1) 2))
(run-test (quote car) (= (car (list 1 2 3)) 1))

(if (= failures 0) 0 1)
