from syllib import *

END_POINTS = [BARBARA, CELARENT]

def reduces_by_contradiction(syls):
  if syls[-1].name() in END_POINTS:
    return True
  if syls[-1].name() in [s.name() for s in syls[:-1]]:
    return False
  l = len(syls)
  for contra in syls[-1].contradict():
    if not contra.valid():
      continue
    del syls[l:]
    syls.append(contra)
    if reduces_by_contradiction(syls):
      return True
  return False


for figure in range(1, 5):
  for major in [A, E, I, O]:
    for minor in [A, E, I, O]:
      for conclusion in [A, E, I, O]:
        syl = Syllogism.gen_syllogism(figure, major, minor, conclusion)
        if syl.valid():
          chain = [syl]
          if reduces_by_contradiction(chain):
            print('SUCCESS: ', end = '')
            for syl in chain:
              print(syl.name(), end = ', ')
            print('')
          else:
            print('FAIL: ', end = '')
            for syl in chain:
              print(syl.name(), end = ', ')
            print('')
