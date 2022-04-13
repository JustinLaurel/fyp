import numpy as np


class FuzzySet:


  def create_triangular(cls, name, domain_min, domain_max, res, a, b, c):
    t1fs = cls(name, domain_min, domain_max, res)

    a = t1fs._adjust_domain_val(a)
    b = t1fs._adjust_domain_val(b)
    c = t1fs._adjust_domain_val(c)

    t1fs._dom = np.round(np.maximum(np.minimum((t1fs._domain-a)/(b-a), (c-t1fs._domain)/(c-b)), 0), t1fs._precision)
