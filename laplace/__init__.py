from laplace.laplace import Laplace as _Laplace
from laplace.tracer import Tracer as _Tracer

import logging

Laplace = _Laplace
Tracer = _Tracer

logging.basicConfig(level=logging.INFO)