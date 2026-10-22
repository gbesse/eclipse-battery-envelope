import unittest
from eclipse_battery_envelope import run

def calc(segments,**kw):return run(dict(capacity_wh=100,initial_wh=[70,80],reserve_wh=20,segments=segments,**kw))
def seg(id,dt,g,l):return dict(id=id,duration_hours=dt,generation_w=g,load_w=l)
class DomainTests(unittest.TestCase):
 def test_eclipse_worst_case(self):
  r=calc([seg('e',2,[0,0],[25,35])]);self.assertEqual(r['charge_wh'],[0,30]);self.assertAlmostEqual(r['first_worst_case_reserve_crossing_hours'],50/35)
 def test_capacity_curtailment(self):
  r=calc([seg('s',2,[30,40],[0,0])]);self.assertEqual(r['charge_wh'],[100,100]);self.assertEqual(r['trace'][0]['guaranteed_curtailment_wh'],30)
 def test_zero_clamp_does_not_hide_deficit(self):
  r=calc([seg('e',5,[0,0],[20,30])]);self.assertEqual(r['worst_case_unserved_wh'],80);self.assertFalse(r['guaranteed_reserve'])
 def test_exact_reserve_allowed(self):
  r=calc([seg('e',1,[0,0],[50,50])]);self.assertTrue(r['guaranteed_reserve'])
 def test_efficiency(self):
  r=calc([seg('s',1,[20,20],[0,0])],charge_efficiency=.5);self.assertEqual(r['charge_wh'],[80,90])
 def test_reversed_bounds(self):
  with self.assertRaises(ValueError):calc([seg('s',1,[10,9],[0,0])])
 def test_realizations_inside_bounds(self):
  r=calc([seg('s',1,[10,20],[5,15])]);lo,hi=r['charge_wh']
  for initial in (70,75,80):
   for g in (10,15,20):
    for l in (5,10,15):self.assertLessEqual(lo,initial+g-l);self.assertGreaterEqual(hi,initial+g-l)
