import unittest
from scorer import Scorer


class TestScorerMethods(unittest.TestCase):

    def test_canLoadParticipants(self):
        scorerObj = Scorer(data="participants.csv")
        scorerObj.loadParticipants()

        self.assertTrue(len(scorerObj.participants) > 0)

    def test_canLoadProject(self):
        scorerObj = Scorer(data="participants.csv", proj='project.json')
        scorerObj.loadProject()
        self.assertIsNotNone(scorerObj.project)

    def test_canReadProject(self):
        scorerObj = Scorer(data="participants.csv", proj='project.json')
        scorerObj.loadProject()
        self.assertIsNotNone(scorerObj.project)
        self.assertTrue(scorerObj.project.name ==
                        'Looking for software engineers experienced with Kafka')

    def test_samePointHasZeroDistance(self):
        loc = {
            "latitude": 40.7127753,
            "longitude": -74.0059728
        }

        scorerObj = Scorer(data="participants.csv", proj='project.json')
        self.assertTrue(scorerObj.computeDistance(loc, loc) == 0)

    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)
    pass


if __name__ == '__main__':
    unittest.main()
