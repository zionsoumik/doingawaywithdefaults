from ..Child import Child


c = Child()

def test_haveParametersChanged():
        # Set up initial, relevant data in Child instance
        c.oldGrammar = [0,0,0,0,0,1,1,1,1,1,0,0,0]
        c.grammar = [0,0,0,0,0,1,1,1,1,1,0,0,0]
        c.timeCourseVector = [[1,i] for i in range(1,14)]

        c.haveParametersChanged(5)

        # Assert that none of data has changed after
        # the function has run
        assert c.oldGrammar == [0,0,0,0,0,1,1,1,1,1,0,0,0]
        assert c.grammar == [0,0,0,0,0,1,1,1,1,1,0,0,0]
        assert c.timeCourseVector == [[1,i] for i in range(1,14)]

        # This grammar is the opposite of the original
        # and should cause the oldGrammar and timeCourseVector
        # to change after running haveParametersChanged
        c.grammar = [1,1,1,1,1,0,0,0,0,0,1,1,1]

        c.haveParametersChanged(6)

        # Assert oldGramar, grammar, and timeCourseVector
        # have changed accordingly
        assert c.oldGrammar == [1,1,1,1,1,0,0,0,0,0,1,1,1]
        assert c.grammar == [1,1,1,1,1,0,0,0,0,0,1,1,1]
        assert c.timeCourseVector == [[6,i] for i in range(1,14)]

        c.grammar = [0,1,1,1,1,0,0,0,0,0,1,1,1]

        c.haveParametersChanged(10)

        assert c.oldGrammar == [0,1,1,1,1,0,0,0,0,0,1,1,1]
        assert c.grammar == [0,1,1,1,1,0,0,0,0,0,1,1,1]
        temp1 = [[10,1]]
        temp2 = [[6,i] for i in range(2, 14)]
        assert c.timeCourseVector == temp1 + temp2


# Test various combinations of lists
# and values to draw out border cases
def test_findIndex():
        c.infoList = [611, 'IMP', ['0','0','0']]
        assert c.findIndex('0') == 0
        assert c.findIndex('0.01') == -1

        c.infoList[2] = ['0','0','434']
        assert c.findIndex('434') == 2
        assert c.findIndex('435') == -1
        assert c.findIndex('433') == -1


def test_isQuestion():
        c.infoList = [584, 'Q', 'Adv S Aux Never Verb']
        assert c.isQuestion()

        c.infoList = [584, 'Q ', 'Adv S Aux Never Verb']
        assert not c.isQuestion()

        c.infoList = [584, 'q', 'Adv S Aux Never Verb']
        assert not c.isQuestion()

        c.infoList = [584, "Q", 'Adv S Aux Never Verb']
        assert c.isQuestion()


def test_isImperative():
        c.infoList = [584, 'IMP', 'Adv S Aux Never Verb']
        assert c.isImperative()

        c.infoList = [584, 'IMp', 'Adv S Aux Never Verb']
        assert not c.isImperative()

        c.infoList = [584, '  IMP', 'Adv S Aux Never Verb']
        assert not c.isImperative()

        c.infoList = [584, 'imp', 'Adv S Aux Never Verb']
        assert not c.isImperative()

        c.infoList = [584, "IMP", 'Adv S Aux Never Verb']
        assert c.isImperative()


def test_isDeclarative():
        c.infoList = [584, 'DEC', 'Adv S Aux Never Verb']
        assert c.isDeclarative()

        c.infoList = [584, 'DEc', 'Adv S Aux Never Verb']
        assert not c.isDeclarative()

        c.infoList = [584, '  DEC', 'Adv S Aux Never Verb']
        assert not c.isDeclarative()

        c.infoList = [584, 'dec', 'Adv S Aux Never Verb']
        assert not c.isDeclarative()

        c.infoList = [584, "DEC", 'Adv S Aux Never Verb']
        assert c.isDeclarative()


# c.grammar[0] will be set to '1' if O1 appears in any index
# other than 0 and S appears after it in c.sentence 
def test_setSubjPos():
        # Since '01' and 'S' don't appear in the infoList.
        # grammar[0] will remain '0'
        c.infoList = [584, "DEC", 'Adv S Aux Never Verb']
        c.sentence = c.infoList[2].split()
        c.grammar = [0,0,0,0,0,0,1,0,0,0,1,0,1]
        assert c.grammar[0] == 0
        c.setSubjPos()
        assert c.grammar[0] == 0

        # '01' and 'S' are both in infoList[2] but since
        # '01' is in the initial position, grammar[0]
        # won't change
        c.infoList = [584, "DEC", '01 S Aux Never Verb']
        c.sentence = c.infoList[2].split()
        assert c.grammar[0] == 0
        c.setSubjPos()
        assert c.grammar[0] == 0

        # grammar[0] will change since both are present
        # and 01 isn't in the initial spot but appears
        # before S
        c.infoList = [584, "DEC", 'Aux O1 S Never Verb']
        c.infoList[2] = c.infoList[2].split()
        assert c.grammar[0] == 0
        c.setSubjPos()
        assert c.grammar[0] == 1

        # S and 01 are in the wrong order, therefore
        # grammar[0] won't change
        c.grammar[0] = 0
        c.infoList = [584, "DEC", 'Aux S O1 Never Verb']
        c.infoList[2] = c.infoList[2].split()
        assert c.grammar[0] == 0
        c.setSubjPos()
        assert c.grammar[0] == 0

        # Neither S or 01 appear in infoList[2]
        c.infoList = [584, "DEC", 'Aux Never Verb']
        c.infoList[2] = c.infoList[2].split()
        assert c.grammar[0] == 0
        c.setSubjPos()
        assert c.grammar[0] == 0

        # Only 01 appears in infoList[2]
        c.infoList = [584, "DEC", 'Aux O1 Never Verb']
        c.infoList[2] = c.infoList[2].split()
        assert c.grammar[0] == 0
        c.setSubjPos()
        assert c.grammar[0] == 0

        c.infoList = [584, "DEC", 'Aux O1 Never S Verb']
        c.infoList[2] = c.infoList[2].split()
        assert c.grammar[0] == 0
        c.setSubjPos()
        assert c.grammar[0] == 1

        c.infoList = [584, "DEC", 'Aux Never Verb O1 S']
        c.infoList[2] = c.infoList[2].split()
        c.grammar[0] = 0
        c.setSubjPos()
        assert c.grammar[0] == 1


# c.grammar[0] will be set to '0'
# if O1 appears before S in sentence
# in any index
def test_noSubjPos():
        # grammar[0] won't change since 
        # S appears after O1
        c.infoList[2] = 'Aux Never Verb O1 S'.split()
        c.grammar[0] = 1
        c.noSubjPos()
        assert c.grammar[0] == 1

        c.infoList[2] = 'S Aux Never Verb O1'.split()
        c.noSubjPos()
        assert c.grammar[0] == 0

        c.grammar[0] = 1
        c.infoList[2] = 'Aux Never Verb S O1'.split()
        c.noSubjPos()
        assert c.grammar[0] == 0

        c.grammar[0] = 1
        c.infoList[2] = 'Aux Never Verb S'.split()
        c.noSubjPos()
        assert c.grammar[0] == 1

        c.infoList[2] = 'Aux Never Verb O1'.split()
        c.noSubjPos()
        assert c.grammar[0] == 1


'''
c.grammar[1] will be set to '1' if either scenario occurs:
(1) If O3 followed directly by P appears in c.sentence
and O3 is in any index position other than 0

(2) If c.infoList[1] == 'IMP' and Verb followed directly
by O1 appear in c.sentence
'''
def test_setHead():
        # Testing for scenario one
        c.infoList[2] = 'Aux Never Verb O3 P'.split()
        c.grammar[1] = 0
        c.setHead()
        assert c.grammar[1] == 1

        c.infoList[2] = 'Aux Never O3 Verb P'.split()
        c.grammar[1] = 0
        c.setHead()
        assert c.grammar[1] == 0

        c.infoList[2] = 'O3 P Aux Never Verb'.split()
        c.setHead()
        assert c.grammar[1] == 0

        c.infoList[2] = 'O3 Aux P Never Verb'.split()
        c.setHead()
        assert c.grammar[1] == 0


'''
c.grammar[1] will be set to '0' if either scenario occurs
(1) If O3 and P both appear in c.infoList[2] and the index
of P is greater than zero and lower than O3's

(2) The sentence type is imperative and both O1 and Verb
appear in c.infoList[2]. Verb must directly follow O1.
'''
def test_noHead():
        # Testing for scenario 1
        c.infoList[2] = 'Aux Never Verb O3 P'.split()
        c.grammar[1] = 1
        c.noHead()
        assert c.grammar[1] == 1

        c.infoList[2] = 'Aux Never Verb P O3'.split()
        c.grammar[1] = 1
        c.noHead()
        assert c.grammar[1] == 0

        c.infoList[2] = 'P O3 Aux Never Verb'.split()
        c.grammar[1] = 1
        c.noHead()
        assert c.grammar[1] == 1

        c.infoList[2] = 'Aux P Never Verb O3'.split()
        c.noHead()
        assert c.grammar[1] == 1

        c.infoList[2] = 'Aux P O3 Never Verb'.split()
        c.noHead()
        assert c.grammar[1] == 0

        # Testing for scenario 2
        c.grammar[1] = 1
        c.infoList[1] = 'IMP'
        c.infoList[2] = 'Verb Aux O1 P'.split()
        c.noHead()
        assert c.grammar[1] == 1

        c.infoList[1] = 'DEC'
        c.infoList[2] = 'Aux Verb O1'.split()
        c.noHead()
        assert c.grammar[1] == 1

        c.infoList[1] = 'IMP'
        c.infoList[2] = 'Aux Verb O1 P'.split()
        c.noHead()
        assert c.grammar[1] == 0


# Tests whether S, O1, O2, O3, or Adv appears
# first in c.infoList[2]
def test_containsTopicalizable():
        c.infoList[2] = 'O1 Aux Verb P'.split()
        assert c.containsTopicalizable()
        
        c.infoList[2] = 'O2 Aux Verb P'.split()
        assert c.containsTopicalizable()

        c.infoList[2] = 'O3 Aux Verb P'.split()
        assert c.containsTopicalizable()

        c.infoList[2] = 'S Aux Verb P'.split()
        assert c.containsTopicalizable()

        c.infoList[2] = 'Adv Aux Verb P'.split()
        assert c.containsTopicalizable()

        c.infoList[2] = 'P O1 O2 O3 S Adv'.split()
        assert not c.containsTopicalizable()

        c.infoList[2] = 'O1 Adv Aux Verb P'.split()
        assert c.containsTopicalizable()


'''
If the sentence is a question check whether
(1) 'ka' is in infoList[2]

(2) 'ka' isn't in infoList[2] while 'Aux' is
'''
def test_setHeadCP():
        # Testing for scenario #1
        c.grammar[2] = 0
        c.infoList[1] = 'Q'
        c.infoList[2] = 'O1 Adv Aux Verb P ka'.split()
        c.setHeadCP()
        assert c.grammar[2] == 1

        c.grammar[2] = 0
        c.infoList[2] = 'O1 Adv ka Verb P Aux'.split()
        c.setHeadCP()
        assert c.grammar[2] == 0

        c.infoList[2] = 'O1 Adv ka Verb P'.split()
        c.setHeadCP()
        assert c.grammar[2] == 0

        # Testing for scenario #2
        c.infoList[2] = 'O1 Adv Verb P Aux'.split()
        c.setHeadCP()
        assert c.grammar[2] == 1

        c.grammar[2] = 0
        c.infoList[1] = 'IMP'
        c.infoList[2] = 'O1 Adv Verb P ka'.split()
        c.setHeadCP()
        assert c.grammar[2] == 0

        c.infoList[2] = 'O1 Adv Verb P Aux'.split()
        c.setHeadCP()
        assert c.grammar[2] == 0


'''
Grammar[1] is set to 0 if both O3 and P
are in the sentence and P isn't the first element in the
sentence but appears immediately before O3 in the sentence

Grammar[1] is set to 1 if the sentence is imperative
and 01 and Verb are in the sentence. Additionally,
Verb must appear immediately before O1
'''
def test_noHead():
        # Testing for scenario #1
        c.grammar[1] = 1
        c.infoList[1] = 'Q'
        c.infoList[2] = 'O3 Adv Verb P Aux'.split()
        c.noHead()
        assert c.grammar[1] == 1

        c.infoList[2] = 'P O3 Adv Verb Aux'.split()
        c.noHead()
        assert c.grammar[1] == 1

        c.infoList[2] = 'Adv P O3 Verb Aux'.split()
        c.noHead()
        assert c.grammar[1] == 0

        c.grammar[1] = 1
        c.infoList[2] = 'Adv P Verb O3 Aux'.split()
        c.noHead()
        assert c.grammar[1] == 1

        # Testing for scenario #2
        c.grammar[1] = 0
        c.infoList[1] = 'IMP'
        c.infoList[2] = 'Adv P Verb O1 Aux'.split()
        c.noHead()
        assert c.grammar[1] == 1

        c.grammar[1] = 0
        c.infoList[2] = 'Adv P Verb Aux O1'.split()
        c.noHead()
        assert c.grammar[1] == 0

        c.infoList[2] = 'Adv P O1 Verb Aux'.split()
        c.noHead()
        assert c.grammar[1] == 0


'''
If the sentence is a question and either
ka is the first element of the sentence or
ka isn't in the sentence and aux is the first
element of the sentence, grammar[2] is set to 0
'''
def test_noHeadCP():
        c.infoList[1] = 'Q'
        c.grammar[2] = 1
        c.infoList[2] = 'ka Adv P O1 Verb Aux'.split()
        c.noHeadCP()
        assert c.grammar[2] == 0

        c.grammar[2] = 1
        c.infoList[2] = 'Aux Adv P O1 Verb'.split()
        c.noHeadCP()
        assert c.grammar[2] == 0

        c.grammar[2] = 1
        c.infoList[2] = 'Aux Adv P O1 ka Verb'.split()
        c.noHeadCP()
        assert c.grammar[2] == 1

        c.infoList[1] = 'DEC'
        c.grammar[2] = 1
        c.infoList[2] = 'ka Adv P O1 Verb Aux'.split()
        c.noHeadCP()
        assert c.grammar[2] == 1

        c.grammar[2] = 1
        c.infoList[2] = 'Aux Adv P O1 Verb'.split()
        c.noHeadCP()
        assert c.grammar[2] == 1

        c.infoList[2] = 'Aux Adv P O1 ka Verb'.split()
        c.noHeadCP()
        assert c.grammar[2] == 1

        c.infoList[1] = 'IMP'
        c.grammar[2] = 1
        c.infoList[2] = 'ka Adv P O1 Verb Aux'.split()
        c.noHeadCP()
        assert c.grammar[2] == 1

        c.grammar[2] = 1
        c.infoList[2] = 'Aux Adv P O1 Verb'.split()
        c.noHeadCP()
        assert c.grammar[2] == 1

        c.infoList[2] = 'Aux Adv P O1 ka Verb'.split()
        c.noHeadCP()
        assert c.grammar[2] == 1


'''
If the sentence is declarative and either
1. O2 is in the sentence while O1 isn't, 
then grammar[5] is set to 1. If grammar[3]
is equivalent to 1, then grammar[3] is set to 0

2. If containsTopicalizable returns true,
then grammar[3] is set to 1
'''
def test_setObligTopic():
        # Testing for scenario #1
        c.infoList[1] = 'DEC'
        c.grammar[5] = 0
        c.grammar[3] = 1
        c.infoList[2] = 'Aux Adv P O2 ka Verb'.split()
        c.setObligTopic()
        assert c.grammar[3] == 0
        assert c.grammar[5] == 1
        c.setObligTopic()
        assert c.grammar[3] == 0

        # Testing for scenario #2
        c.grammar[3] = 0
        c.infoList[2] = 'Aux Adv P O2 ka Verb O1'.split()
        c.setObligTopic()
        assert c.grammar[3] == 0

        c.infoList[2] = 'S Aux Adv P O2 ka Verb O1'.split()
        c.setObligTopic()
        assert c.grammar[3] == 1

        c.grammar[0] = 0
        c.infoList[2] = 'O1 Aux Adv P O2 ka Verb'.split()
        c.setObligTopic()
        assert c.grammar[3] == 1

        c.grammar[0] = 0
        c.infoList[2] = 'O2 Aux Adv P O1 ka Verb'.split()
        c.setObligTopic()
        assert c.grammar[3] == 1

        c.grammar[0] = 0
        c.infoList[2] = 'O3 Aux Adv P O2 ka O1 Verb'.split()
        c.setObligTopic()
        assert c.grammar[3] == 1

        c.grammar[0] = 0
        c.infoList[2] = 'Adv P ka Verb'.split()
        c.setObligTopic()
        assert c.grammar[3] == 1


'''
Determine if any of the specified positioning
and appearance of O1, O2, O3, and P correspond to 
the contents of the sentence. If so, the function 
return either true or false depending on which 
combination appears
'''
def test_outOblique():
        # Testing for scenario #1
        c.infoList[2] = 'O1 O2 P O3 Aux Verb'.split()
        assert not c.outOblique()

        c.infoList[2] = 'O1 Aux O2 Verb P O3 ka'.split()
        assert not c.outOblique()

        c.infoList[2] = 'O1 Aux O2 Verb P ka O3'.split()
        assert c.outOblique()

        c.infoList[2] = 'Aux O2 O1 Verb P O3 ka'.split()
        assert c.outOblique()

        # Testing for scenario #2
        c.infoList[2] = 'O3 P O2 O1 Aux ka'.split()
        assert not c.outOblique()

        c.infoList[2] = 'O3 O2 P O1 Aux ka'.split()
        assert c.outOblique()

        c.infoList[2] = 'O3 P Aux O2 ka O1 Verb'.split()
        assert not c.outOblique()

        c.infoList[2] = 'O2 O3 P O1 Aux ka'.split()
        assert c.outOblique()


def test_setNullSubj():
        c.grammar[4] = 0
        c.infoList[1] = 'DEC'
        c.infoList[2] = 'O3 O2 P O1 Aux ka'.split()
        c.setNullSubj()
        assert c.grammar[4] == 1

        c.grammar[4] = 0
        c.infoList[1] = 'Q'
        c.setNullSubj()
        assert c.grammar[4] == 0

        c.infoList[1] = 'IMP'
        c.setNullSubj()
        assert c.grammar[4] == 0

        c.infoList[1] = 'DEC'
        c.infoList[2] = 'O3 O2 P O1 Aux ka S'.split()
        c.setNullSubj()
        assert c.grammar[4] == 0

        c.infoList[2] = 'O3 O2 P O1 Aux ka S'.split()
        c.setNullSubj()
        assert c.grammar[4] == 0


# c.grammar[5] is set to 1 if O2 is in the 
# sentence and O1 isn't in the sentence
def test_setNullTopic():
        c.grammar[5] = 0
        c.infoList[2] = 'O3 O2 P Aux ka S'.split()
        c.setNullTopic()
        assert c.grammar[5] == 1
        
        c.grammar[5] = 0
        c.infoList[2] = 'O3 O2 O1 P Aux ka S'.split()
        c.setNullTopic()
        assert c.grammar[5] == 0

        c.infoList[2] = 'O3 P O1 Aux ka S'.split()
        c.setNullTopic()
        assert c.grammar[5] == 0

        c.infoList[2] = 'O3 P Aux ka S'.split()
        c.setNullTopic()
        assert c.grammar[5] == 0


def test_setWHMovement():
        c.grammar[6] = 1
        c.infoList[2] = 'O3 +WH P Aux ka S'.split()
        c.setWHMovement()
        assert c.grammar[6] == 0

        c.grammar[6] = 1
        c.infoList[2] = 'O3 +WH P Aux O3[+WH] ka S'.split()
        c.setWHMovement()
        assert c.grammar[6] == 1

        c.grammar[6] = 1
        c.infoList[2] = 'O3 +WH O3 P Aux ka S'.split()
        c.setWHMovement()
        assert c.grammar[6] == 0

        c.grammar[6] = 1
        c.infoList[2] = 'O3[+WH] P Aux ka S'.split()
        c.setWHMovement()
        assert c.grammar[6] == 1

        c.grammar[6] = 1
        c.infoList[2] = 'O3 P Aux ka S'.split()
        c.setWHMovement()
        assert c.grammar[6] == 1


def test_setPrepStrand():
        c.grammar[7] = 0
        c.infoList[2] = 'O3 +WH P Aux ka S'.split()
        c.setPrepStrand()
        assert c.grammar[7] == 1

        c.grammar[7] = 0
        c.infoList[2] = 'O3 P Aux ka S'.split()
        c.setPrepStrand()
        assert c.grammar[7] == 0

        c.infoList[2] = 'O3 Aux ka S'.split()
        c.setPrepStrand()
        assert c.grammar[7] == 0

        c.infoList[2] = '+WH Aux ka S'.split()
        c.setPrepStrand()
        assert c.grammar[7] == 0      


def test_setTopicMark():
        c.grammar[8] = 0
        c.infoList[2] = 'WA +WH Aux ka S'.split()
        c.setTopicMark()
        assert c.grammar[8] == 1

        c.grammar[8] = 0
        c.infoList[2] = '+WA Aux ka S'.split()
        c.setTopicMark()
        assert c.grammar[8] == 0


'''
If O1 and Verb appear in the sentence,
O1 appears after the first element, and
there is at least one element between them,
then grammar[9] is set to 1
'''
def test_vToI():
        c.grammar[9] = 0
        c.infoList[2] = 'Verb +WA O1 Aux ka S'.split()
        c.vToI()
        assert c.grammar[9] == 1
        
        c.grammar[9] = 0
        c.infoList[2] = '+WA O1 Aux Verb ka S'.split()
        c.vToI()
        assert c.grammar[9] == 1

        c.grammar[9] = 0
        c.infoList[2] = 'O1 Aux Verb ka S'.split()
        c.vToI()
        assert c.grammar[9] == 0

        c.infoList[2] = '+WA O1 Verb Aux ka S'.split()
        c.vToI()
        assert c.grammar[9] == 0

        c.infoList[2] = '+WA O1 Aux ka S'.split()
        c.vToI()
        assert c.grammar[9] == 0

        c.infoList[2] = '+WA Aux Verb ka S'.split()
        c.vToI()
        assert c.grammar[9] == 0


'''
If the sentence is declarative, S appears in the
sentence but not in the first position and Aux
appears immediately after, then return True
'''
def test_S_Aux():
        c.infoList[1] = 'DEC'
        c.infoList[2] = '+WA Verb ka S Aux'.split()
        assert c.S_Aux()
        
        c.infoList[2] = '+WA S Aux Verb ka'.split()
        assert c.S_Aux()

        c.infoList[2] = 'S Aux +WA Verb ka'.split()
        assert not c.S_Aux()

        c.infoList[2] = '+WA ka S Verb Aux'.split()
        assert not c.S_Aux()

        c.infoList[2] = '+WA Verb ka Aux'.split()
        assert not c.S_Aux()

        c.infoList[2] = '+WA Verb ka Aux'.split()
        assert not c.S_Aux()

        c.infoList[1] = 'Q'
        c.infoList[2] = '+WA Verb ka S Aux'.split()
        assert not c.S_Aux()


def test_Aux_S():
        c.infoList[1] = 'DEC'
        c.infoList[2] = '+WA Verb ka Aux S'.split()
        assert c.Aux_S()

        c.infoList[2] = '+WA Aux S Verb ka'.split()
        assert c.Aux_S()

        c.infoList[2] = 'Aux S +WA Verb ka'.split()
        assert not c.Aux_S()

        c.infoList[2] = '+WA Verb Aux ka S'.split()
        assert not c.Aux_S()

        c.infoList[2] = '+WA Verb ka S Aux'.split()
        assert not c.Aux_S()

        c.infoList[1] = 'Q'
        c.infoList[2] = '+WA Verb ka Aux S'.split()
        assert not c.Aux_S()


def test_Aux_Verb():
        c.infoList[1] = 'DEC'
        c.infoList[2] = '+WA ka Aux Verb S'.split()
        assert c.Aux_Verb()

        c.infoList[1] = 'DEC'
        c.infoList[2] = '+WA ka Verb S'.split()
        assert not c.Aux_Verb()

        c.infoList[1] = 'DEC'
        c.infoList[2] = '+WA ka Verb Aux S'.split()
        assert not c.Aux_Verb()

        c.infoList[1] = 'Q'
        c.infoList[2] = '+WA ka Aux Verb S'.split()
        assert not c.Aux_Verb()


def test_Verb_Aux():
        c.infoList[1] = 'DEC'
        c.infoList[2] = '+WA ka Verb Aux S'.split()
        assert c.Verb_Aux()

        c.infoList[1] = 'DEC'
        c.infoList[2] = '+WA Verb ka Aux S'.split()
        assert not c.Verb_Aux()

        c.infoList[1] = 'Q'
        c.infoList[2] = '+WA ka Verb Aux S'.split()
        assert not c.Verb_Aux()


def test_Never_Verb():
        c.infoList[1] = 'DEC'
        c.infoList[2] = '+WA ka Never Verb S'.split()
        assert c.Never_Verb()

        c.infoList[2] = '+WA ka Verb Never S'.split()
        assert not c.Never_Verb()

        c.infoList[2] = 'Aux +WA ka Never Verb S'.split()
        assert not c.Never_Verb()

        c.infoList[1] = 'Q'
        c.infoList[2] = '+WA ka Never Verb S'.split()
        assert not c.Never_Verb()


def test_Verb_Never():
        c.infoList[1] = 'DEC'
        c.infoList[2] = '+WA ka Verb Never S'.split()
        assert c.Verb_Never()

        c.infoList[2] = '+WA ka Verb Never S Aux'.split()
        assert not c.Verb_Never()

        c.infoList[2] = '+WA Verb ka Never S'.split()
        assert not c.Verb_Never()

        c.infoList[1] = 'Q'
        c.infoList[2] = '+WA ka Verb Never S'.split()
        assert not c.Verb_Never()


def test_hasKa():
        c.infoList[2] = '+WA ka Verb Never S'.split()
        assert c.hasKa()

        c.infoList[2] = '+WA Verb Never S'.split()
        assert not c.hasKa()


def test_iToC():
        c.infoList[1] = 'DEC'
        c.grammar[0] = 0
        c.grammar[1] = 0
        c.grammar[2] = 0
        c.grammar[10] = 1
        c.infoList[2] = '+WA Verb Never S Aux'.split()
        c.iToC()
        assert c.grammar[10] == 0

        c.grammar[10] = 1
        c.grammar[0] = 1
        c.iToC()
        assert c.grammar[10] == 1

        c.grammar[10] = 1
        c.grammar[1] = 1
        c.grammar[2] = 1
        c.infoList[2] = '+WA Verb Never Aux S'.split()
        c.iToC()
        assert c.grammar[10] == 0

def test_Verb_tensed():
        c.infoList[1] = 'Q'
        c.infoList[2] = '+WA ka Verb Never S'.split()
        assert c.Verb_tensed()

        c.infoList[2] = '+WA Aux ka Verb Never S'.split()
        assert not c.Verb_tensed()

        c.infoList[1] = 'DEC'
        c.infoList[2] = '+WA ka Verb Never S'.split()
        assert c.Verb_tensed()

        c.infoList[2] = 'Aux +WA ka Verb Never S'.split()
        assert not c.Verb_tensed()


def test_affix_Hop():
        c.grammar[11] = 0
        c.infoList[1] = 'DEC'
        c.infoList[2] = '+WA ka Never Verb O1 S'.split()
        c.affixHop()
        assert c.Verb_tensed()
        assert c.grammar[11] == 1

        c.grammar[11] = 0
        c.infoList[2] = '+WA ka O1 Verb Never S'.split()
        c.affixHop()
        assert c.grammar[11] == 1
        
        c.grammar[11] = 0
        c.infoList[2] = 'O1 Verb Never S +WA ka Aux'.split()
        c.affixHop()
        assert c.grammar[11] == 0

        c.grammar[11] = 0
        c.infoList[1] = 'Q'
        c.infoList[2] = '+WA ka Never Verb O1 S'.split()
        c.affixHop()
        assert c.Verb_tensed()
        assert c.grammar[11] == 1

        c.grammar[11] = 0
        c.infoList[2] = '+WA ka O1 Verb Never S'.split()
        c.affixHop()
        assert c.grammar[11] == 1
        
        c.grammar[11] = 0
        c.infoList[2] = 'O1 Verb Never S +WA ka Aux'.split()
        c.affixHop()
        assert c.grammar[11] == 0


def test_questionInver():
        c.grammar[12] = 1
        c.infoList[2] = 'Aux +WA ka Verb Never S'.split()
        c.questionInver()
        assert c.grammar[12] == 0

        c.grammar[12] = 1
        c.infoList[2] = 'Aux +WA Verb Never S'.split()
        c.questionInver()
        assert c.grammar[12] == 1
