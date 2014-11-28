import unittest
from syllib import *

class TestProposition(unittest.TestCase):
  def setUp(self):
    self.aprop = Proposition('A', 'B', A)
    self.eprop = Proposition('A', 'B', E)
    self.iprop = Proposition('A', 'B', I)
    self.oprop = Proposition('A', 'B', O)

  def test_subject(self):
    self.assertEqual(self.aprop.subject(), 'A')

  def test_predicate(self):
    self.assertEqual(self.iprop.predicate(), 'B')

  def test_negatives(self):
    self.assertFalse(self.aprop.is_negative())
    self.assertTrue(self.eprop.is_negative())
    self.assertFalse(self.iprop.is_negative())
    self.assertTrue(self.oprop.is_negative())

  def test_affirmatives(self):
    self.assertTrue(self.aprop.is_affirmative())
    self.assertFalse(self.eprop.is_affirmative())
    self.assertTrue(self.iprop.is_affirmative())
    self.assertFalse(self.oprop.is_affirmative())

  def test_universals(self):
    self.assertTrue(self.aprop.is_universal())
    self.assertTrue(self.eprop.is_universal())
    self.assertFalse(self.iprop.is_universal())
    self.assertFalse(self.oprop.is_universal())

  def test_particulars(self):
    self.assertFalse(self.aprop.is_particular())
    self.assertFalse(self.eprop.is_particular())
    self.assertTrue(self.iprop.is_particular())
    self.assertTrue(self.oprop.is_particular())

  def test_contradictions(self):
    self.assertEqual(self.aprop.contradict(), self.oprop)
    self.assertEqual(self.eprop.contradict(), self.iprop)
    self.assertEqual(self.iprop.contradict(), self.eprop)
    self.assertEqual(self.oprop.contradict(), self.aprop)

class TestSyllogism(unittest.TestCase):
  def setUp(self):
    self.barbara = Syllogism(Proposition('A', 'B', A),
                             Proposition('C', 'A', A),
                             Proposition('C', 'B', A))
    self.festino = Syllogism(Proposition('C', 'A', I),
                             Proposition('B', 'A', E),
                             Proposition('C', 'B', O))
    self.bocardo = Syllogism(Proposition('A', 'C', A),
                             Proposition('A', 'B', O),
                             Proposition('C', 'B', O))
    self.calemes = Syllogism(Proposition('B', 'A', A),
                             Proposition('A', 'C', E),
                             Proposition('C', 'B', E))
    self.invalid = Syllogism(Proposition('A', 'B', A),
                             Proposition('C', 'A', E),
                             Proposition('C', 'B', A))
  def test_figure(self):
    self.assertEqual(self.barbara.figure(), 1)
    self.assertEqual(self.festino.figure(), 2)
    self.assertEqual(self.bocardo.figure(), 3)
    self.assertEqual(self.calemes.figure(), 4)
    nofig = Syllogism(Proposition('A', 'B', A),
                      Proposition('C', 'D', A),
                      Proposition('C', 'B', A))
    self.assertEqual(nofig.figure(), 0)



  def test_name(self):
    self.assertEqual(self.barbara.name(), BARBARA)
    self.assertEqual(self.festino.name(), FESTINO)
    self.assertEqual(self.bocardo.name(), BOCARDO)
    self.assertEqual(self.calemes.name(), CALEMES)
    self.assertEqual(self.invalid.name(), INVALID)

  def test_premises(self):
    self.assertEqual(self.barbara.major(), Proposition('A', 'B', A))
    self.assertEqual(self.bocardo.minor(), Proposition('A', 'C', A))
    self.assertEqual(self.calemes.conclusion(), Proposition('C', 'B', E))

  def test_valid(self):
    self.assertTrue(self.barbara.valid())
    self.assertTrue(self.festino.valid())
    self.assertTrue(self.bocardo.valid())
    self.assertTrue(self.calemes.valid())
    self.assertFalse(self.invalid.valid())

  def test_gen_syl(self):
    self.assertEqual(self.barbara.name(), Syllogism.gen_syllogism(1, A, A, A).name())
    self.assertEqual(self.festino.name(), Syllogism.gen_syllogism(2, E, I, O).name())
    self.assertEqual(self.bocardo.name(), Syllogism.gen_syllogism(3, O, A, O).name())
    self.assertEqual(self.calemes.name(), Syllogism.gen_syllogism(4, A, E, E).name())
    with self.assertRaises(ValueError):
      Syllogism.gen_syllogism(0, A, A, A)
    with self.assertRaises(ValueError):
      Syllogism.gen_syllogism(2, 'd', A, A)
    with self.assertRaises(ValueError):
      Syllogism.gen_syllogism(2, A, 'd', A)
    with self.assertRaises(ValueError):
      Syllogism.gen_syllogism(2, A, A, 'd')

  def test_contradict(self):
    syl1, syl2 = self.barbara.contradict()
    contra1 = Syllogism(Proposition('C', 'B', O),
                        Proposition('C', 'A', A),
                        Proposition('A', 'B', O))
    contra2 = Syllogism(Proposition('C', 'B', O),
                        Proposition('A', 'B', A),
                        Proposition('C', 'A', O))
    self.assertIn(syl1, [contra1, contra2])
    self.assertIn(syl2, [contra1, contra2])
    self.assertNotEqual(syl1, syl2)

if __name__ == '__main__':
  unittest.main()
