from .. import runSimulation
import pytest, os


def test_makeSelectedSentences():
        infoFile = open(os.path.dirname(__file__) + '/../EngFrJapGerm.txt')
        runSim1 = runSimulation.runSimulation(infoFile.readlines(), 611)
        infoFile.close()

    # These four ids are present in EngFrJapGerm: French=584, English=611, German=2253, Japanese=3856
        # Check that makeSelectedSentenceList returns the proper number of sentences for each id
        runSim1.makeSelectedSentenceList()
        assert runSim1.selectedSentences
        assert len(runSim1.selectedSentences) == 540

        runSim1.targetGrammar = 584
        runSim1.selectedSentences = []
        runSim1.makeSelectedSentenceList()
        assert len(runSim1.selectedSentences) == 756

        runSim1.targetGrammar = 2253
        runSim1.selectedSentences = []
        runSim1.makeSelectedSentenceList()
        assert len(runSim1.selectedSentences) == 1134

        runSim1.targetGrammar = 3856
        runSim1.selectedSentences = []
        runSim1.makeSelectedSentenceList()
        assert len(runSim1.selectedSentences) == 1092

        # Check that makeSelectedSentencesList returns empty lists
        # when given ids that don't exist in the orignal txt file
        runSim1.targetGrammar = 612
        runSim1.selectedSentences = []
        runSim1.makeSelectedSentenceList()
        assert not runSim1.selectedSentences

        runSim1.targetGrammar = None
        runSim1.selectedSentences = []
        runSim1.makeSelectedSentenceList()
        assert not runSim1.selectedSentences
