from syllib import *

valid_syls = []
for figure in range(1, 5):
  for major in [A, E, I, O]:
    for minor in [A, E, I, O]:
      for conclusion in [A, E, I, O]:
        syl = Syllogism.gen_syllogism(figure, major, minor, conclusion)
        if syl.valid():
          print(syl, end = ', ')
  print('')
