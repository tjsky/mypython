(defun c:deleteTC ()
  (vl-load-com)
  (setq ss (ssget "X" '((0 . "HATCH")))) ; 选择所有的填充
  (if ss
    (progn
      (command "_.erase" ss "") ; 删除填充
      (princ (strcat "\nDeleted " (itoa (sslength ss)) " hatch objects."))
    )
    (princ "\nNo hatch objects found.")
  )
  (princ)
)