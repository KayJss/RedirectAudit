import unittest
from redirectaudit.core import *
class T(unittest.TestCase):
 def test_url(self):
  with self.assertRaises(ValueError):validate_url("/x")
 def test_clean(self):self.assertTrue(analyze([Hop("https://x",200)])["healthy"])
 def test_redirect(self):self.assertEqual(analyze([Hop("http://x",301,"https://x"),Hop("https://x",200)])["redirect_count"],1)
 def test_loop(self):self.assertTrue(analyze([Hop("x",301,"/a"),Hop("x/a",301,"/"),Hop("x",0,"redirect-loop")])["loop_detected"])
 def test_long(self):self.assertFalse(analyze([Hop(str(i),302,str(i+1)) for i in range(5)]+[Hop("5",200)])["healthy"])
 def test_500(self):self.assertFalse(analyze([Hop("x",500)])["healthy"])
if __name__=="__main__":unittest.main()
