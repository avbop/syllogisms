# Constants
A = 'A'
E = 'E'
I = 'I'
O = 'O'
BARBARA = 'Barbara'
CELARENT = 'Celarent'
DARII = 'Darii'
FERIO = 'Ferio'
CESARE = 'Cesare'
CAMESTRES = 'Camestres'
FESTINO = 'Festino'
BAROCO = 'Baroco'
DARAPTI = 'Darapti'
FELAPTON = 'Felapton'
DISAMIS = 'Disamis'
DATISI = 'Datisi'
BOCARDO = 'Bocardo'
FERISON = 'Ferison'
BRAMANTIP = 'Bramantip'
CALEMES = 'Calemes'
DIMATIS = 'Dimatis'
FESAPO = 'Fesapo'
FRESISON = 'Fresison'
INVALID = '(Invalid)'

class Proposition():
  """An immutable object representing a proposition."""
  def __init__(self, subj, pred, mood):
    if mood not in [A, E, I, O]:
      raise ValueError('mood not one of A, E, I, O')
    self._subject = subj
    self._predicate = pred
    self._mood = mood

  def subject(self):
    return self._subject

  def predicate(self):
    return self._predicate

  def is_affirmative(self):
    return self._mood == A or self._mood == I

  def is_negative(self):
    return self._mood == E or self._mood == O

  def is_universal(self):
    return self._mood == A or self._mood == E

  def is_particular(self):
    return self._mood == I or self._mood == O

  def mood(self):
    return self._mood

  def contradict(self):
    if self._mood == A:
      return Proposition(self._subject, self._predicate, O)
    elif self._mood == E:
      return Proposition(self._subject, self._predicate, I)
    elif self._mood == I:
      return Proposition(self._subject, self._predicate, E)
    elif self._mood == O:
      return Proposition(self._subject, self._predicate, A)

  def __str__(self):
    retstr = ''
    if self._mood == A:
      retstr = 'Every {} is {}.'
    elif self._mood == E:
      retstr = 'No {} is {}.'
    elif self._mood == I:
      retstr = 'Some {} is {}.'
    elif self._mood == O:
      retstr = 'Some {} is not {}.'
    return retstr.format(self._subject, self._predicate)

  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    if self._subject != other._subject or self._predicate != other._predicate or self._mood != other._mood:
      return False
    return True

  def __ne__(self, other):
    return not self.__eq__(other)

class Syllogism():
  """An immutable object representing a syllogism."""
  def __init__(self, prop1, prop2, conc):
    self._conclusion = conc
    # Assign major and minor: if invalid, this will be random.
    if prop1.subject() == conc.subject() or prop1.predicate() == conc.subject():
      self._minor = prop1
      self._major = prop2
    else:
      self._minor = prop2
      self._major = prop1

  @staticmethod
  def gen_syllogism(figure, major, minor, conclusion):
    if figure not in [1, 2, 3, 4]:
      raise ValueError('Figure not one of 1, 2, 3, 4.')
    if major not in [A, E, I, O] or minor not in [A, E, I, O] or conclusion not in [A, E, I, O]:
      raise ValueError('Mood not one of A, E, I, O.')
    genconc = Proposition('S', 'P', conclusion)
    genmaj = None
    genmin = None
    if figure == 1:
      genmaj = Proposition('M', 'P', major)
      genmin = Proposition('S', 'M', minor)
    elif figure == 2:
      genmaj = Proposition('P', 'M', major)
      genmin = Proposition('S', 'M', minor)
    elif figure == 3:
      genmaj = Proposition('M', 'P', major)
      genmin = Proposition('M', 'S', minor)
    elif figure == 4:
      genmaj = Proposition('P', 'M', major)
      genmin = Proposition('M', 'S', minor)
    return Syllogism(genmin, genmaj, genconc)

  def major(self):
    return self._major

  def minor(self):
    return self._minor

  def conclusion(self):
    return self._conclusion

  def figure(self):
    minor = self._conclusion.subject()
    major = self._conclusion.predicate()
    if self._minor.subject() == minor: # ??/S?/SP
      if self._major.subject() == major: # P?/S?/SP
        if self._major.predicate() == self._minor.predicate(): # PM/SM/SP
          return 2
      elif self._major.predicate() == major: # ?P/S?/SP
        if self._major.subject() == self._minor.predicate(): # MP/SM/SP
          return 1
    elif self._minor.predicate() == minor: # ??/?S/SP
      if self._major.subject() == major: # P?/?S/SP
        if self._major.predicate() == self._minor.subject(): # PM/MS/SP
          return 4
      elif self._major.predicate() == major: # ?P/?S/SP
        if self._major.subject() == self._minor.subject(): # MP/MS/SP
          return 3
    return 0

  def valid(self):
    # Three terms
    if self.figure() == 0:
      return False
    # Two negatives
    if self._minor.is_negative() and self._major.is_negative():
      return False
    # Follow weaker
    if self._major.is_negative() or self._minor.is_negative():
      if not self._conclusion.is_negative():
        return False
    if self._major.is_particular() or self._minor.is_particular():
      if not self._conclusion.is_particular():
        return False
    # Middle distributed
    if self.figure() == 1:
      if not (self._major.is_universal() or self._minor.is_negative()):
        return False
    elif self.figure() == 2:
      if not (self._major.is_negative() or self._minor.is_negative()):
        return False
    elif self.figure() == 3:
      if not (self._major.is_universal() or self._minor.is_universal()):
        return False
    elif self.figure() == 4:
      if not (self._major.is_negative() or self._minor.is_universal()):
        return False
    # Terms distributed
    if self._conclusion.is_universal():
      if self.figure() in [1, 2]:
        if not self._minor.is_universal():
          return False
      elif self.figure() in [3, 4]:
        if not self._minor.is_negative():
          return False
    if self._conclusion.is_negative():
      if self.figure() in [1, 3]:
        if not self._major.is_negative():
          return False
      elif self.figure() in [2, 4]:
        if not self._major.is_universal():
          return False
    return True

  def contradict(self):
    con1 = Syllogism(self._conclusion.contradict(), self._major, self._minor.contradict())
    con2 = Syllogism(self._conclusion.contradict(), self._minor, self._major.contradict())
    return (con1, con2)

  def name(self):
    if not self.valid():
      return INVALID
    if self.figure() == 1:
      if self._major.mood() == A and self._minor.mood() == A and self._conclusion.mood() == A:
        return BARBARA
      if self._major.mood() == E and self._minor.mood() == A and self._conclusion.mood() == E:
        return CELARENT
      if self._major.mood() == A and self._minor.mood() == I and self._conclusion.mood() == I:
        return DARII
      if self._major.mood() == E and self._minor.mood() == I and self._conclusion.mood() == O:
        return FERIO
    elif self.figure() == 2:
      if self._major.mood() == E and self._minor.mood() == A and self._conclusion.mood() == E:
        return CESARE
      if self._major.mood() == A and self._minor.mood() == E and self._conclusion.mood() == E:
        return CAMESTRES
      if self._major.mood() == E and self._minor.mood() == I and self._conclusion.mood() == O:
        return FESTINO
      if self._major.mood() == A and self._minor.mood() == O and self._conclusion.mood() == O:
        return BAROCO
    elif self.figure() == 3:
      if self._major.mood() == A and self._minor.mood() == A and self._conclusion.mood() == I:
        return DARAPTI
      if self._major.mood() == E and self._minor.mood() == A and self._conclusion.mood() == O:
        return FELAPTON
      if self._major.mood() == I and self._minor.mood() == A and self._conclusion.mood() == I:
        return DISAMIS
      if self._major.mood() == A and self._minor.mood() == I and self._conclusion.mood() == I:
        return DATISI
      if self._major.mood() == O and self._minor.mood() == A and self._conclusion.mood() == O:
        return BOCARDO
      if self._major.mood() == E and self._minor.mood() == I and self._conclusion.mood() == O:
        return FERISON
    elif self.figure() == 4:
      if self._major.mood() == A and self._minor.mood() == A and self._conclusion.mood() == I:
        return BRAMANTIP
      if self._major.mood() == A and self._minor.mood() == E and self._conclusion.mood() == E:
        return CALEMES
      if self._major.mood() == I and self._minor.mood() == A and self._conclusion.mood() == I:
        return DIMATIS
      if self._major.mood() == E and self._minor.mood() == A and self._conclusion.mood() == O:
        return FESAPO
      if self._major.mood() == E and self._minor.mood() == I and self._conclusion.mood() == O:
        return FRESISON
    return '{}{}{}{}'.format(self.figure(), self._major.mood(), self._minor.mood(), self._conclusion.mood())

  def __str__(self):
    return self.name()

  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    if self._minor != other._minor or self._major != other._major or self._conclusion != other._conclusion:
      return False
    return True

  def __ne__(self, other):
    return not self.__eq__(other)
