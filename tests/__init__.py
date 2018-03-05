########################################
# create by :ding-PC
# create time :2018-03-02 10:52:55.896546
########################################
import unittest
def test():
    """Run the unit tests."""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
