#/bin/env python3
# -*- encoding: utf-8 -*-

import unittest
from calender.tests import *

if __name__ == "__main__":
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="junit"))
