#! /usr/bin/env python

###############################################################################
##  DendroPy Phylogenetic Computing Library.
##
##  Copyright 2009 Jeet Sukumaran and Mark T. Holder.
##
##  This program is free software; you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation; either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License along
##  with this program. If not, see <http://www.gnu.org/licenses/>.
##
###############################################################################

"""
NEXUS data read/write parse/format tests.
"""

import sys
import os
import unittest
from cStringIO import StringIO

from dendropy.utility import messaging
from dendropy.dataio import nexustokenizer

_LOG = messaging.get_logger(__name__)

class NexusTokenTest(unittest.TestCase):

    def testParseSpacy(self):
        f = """#NEXUS

BEGIN TAXA;
    DIMENSIONS NTAX=30;
    TAXLABELS
        'Anolis ahli'
        'Anolis garmani'
        'Anolis grahami'
        'Anolis valencienni'
        'Anolis lineatopus'
        'Anolis aliniger'
        'Anolis coelestinus'
        'Anolis bahorucoensis'
        'Anolis equestris'
        'Anolis luteogularis'
        'Anolis occultus'
        'Anolis barahonae'
        'Anolis cuvieri'
        'Anolis insolitus'
        'Anolis olssoni'
        'Anolis brevirostris'
        'Anolis distichus'
        'Anolis cristatellus'
        'Anolis krugi'
        'Anolis stratulus'
        'Anolis alutaceus'
        'Anolis vanidicus'
        'Anolis angusticeps'
        'Anolis paternus'
        'Anolis loysiana'
        'Anolis marcanoi'
        'Anolis strahmi'
        'Diplolaemus darwinii'
        'Anolis ophiolepis'
        'Anolis sagrei'
  ;
END;

BEGIN TREES;
    tree 'con 50 majrule' = [&U] ('Anolis ahli':0.2642130000,((('Anolis garmani':0.1068380000,'Anolis grahami':0.0863670000)1.00:0.069511,'Anolis valencienni':0.1642630000)0.87:0.020752,'Anolis lineatopus':0.1957260000)1.00:0.077682,((((((('Anolis aliniger':0.1600010000,'Anolis coelestinus':0.1932310000)1.00:0.071920,'Anolis bahorucoensis':0.2266880000)0.68:0.023043,('Anolis equestris':0.0227020000,'Anolis luteogularis':0.0306410000)1.00:0.198165,'Anolis occultus':0.4231200000)0.89:0.056277,('Anolis barahonae':0.2114890000,'Anolis cuvieri':0.1686700000)1.00:0.084190,('Anolis insolitus':0.2438820000,'Anolis olssoni':0.2568770000)1.00:0.050618)0.86:0.031679,(('Anolis brevirostris':0.1801300000,'Anolis distichus':0.1151360000)1.00:0.123136,(('Anolis cristatellus':0.2144360000,'Anolis krugi':0.1573300000)0.93:0.036788,'Anolis stratulus':0.1973470000)1.00:0.081037)1.00:0.056582)0.77:0.021826,(('Anolis alutaceus':0.1619060000,'Anolis vanidicus':0.2059960000)1.00:0.118216,(('Anolis angusticeps':0.0857100000,'Anolis paternus':0.0595110000)1.00:0.153413,'Anolis loysiana':0.1836280000)1.00:0.042858)1.00:0.057139,('Anolis marcanoi':0.2359120000,'Anolis strahmi':0.1977660000)1.00:0.141032,'Diplolaemus darwinii':0.6364930000)1.00:0.067869,('Anolis ophiolepis':0.0945010000,'Anolis sagrei':0.0967580000)1.00:0.179398)0.96:0.044895);
END;
"""
        r2 = StringIO(f)
        tokenizer = nexustokenizer.NexusTokenizer(r2)
        expected = ['#NEXUS', 'BEGIN', 'TAXA', ';', 'DIMENSIONS', 'NTAX', '=',
                    '30', ';', 'TAXLABELS', 'Anolis ahli', 'Anolis garmani',
                    'Anolis grahami', 'Anolis valencienni', 'Anolis lineatopus',
                    'Anolis aliniger', 'Anolis coelestinus', 'Anolis bahorucoensis',
                    'Anolis equestris', 'Anolis luteogularis', 'Anolis occultus', 'Anolis barahonae',
                    'Anolis cuvieri', 'Anolis insolitus', 'Anolis olssoni', 'Anolis brevirostris',
                    'Anolis distichus', 'Anolis cristatellus', 'Anolis krugi', 'Anolis stratulus', 'Anolis alutaceus', 'Anolis vanidicus', 'Anolis angusticeps', 'Anolis paternus', 'Anolis loysiana', 'Anolis marcanoi', 'Anolis strahmi', 'Diplolaemus darwinii', 'Anolis ophiolepis', 'Anolis sagrei',
                    ';', 'END', ';', 'BEGIN', 'TREES', ';', 'tree', 'con 50 majrule',  '=', '(', 'Anolis ahli', ':', '0.2642130000', ',', '(', '(', '(', 'Anolis garmani', ':', '0.1068380000', ',', 'Anolis grahami', ':', '0.0863670000', ')', '1.00', ':', '0.069511', ',', 'Anolis valencienni', ':', '0.1642630000', ')', '0.87', ':', '0.020752', ',', 'Anolis lineatopus', ':', '0.1957260000', ')', '1.00', ':', '0.077682', ',', '(', '(', '(', '(', '(', '(', '(', 'Anolis aliniger', ':', '0.1600010000', ',', 'Anolis coelestinus', ':', '0.1932310000', ')', '1.00', ':', '0.071920', ',', 'Anolis bahorucoensis', ':', '0.2266880000', ')', '0.68', ':', '0.023043', ',', '(', 'Anolis equestris', ':', '0.0227020000', ',', 'Anolis luteogularis', ':', '0.0306410000', ')', '1.00', ':', '0.198165', ',', 'Anolis occultus', ':', '0.4231200000', ')', '0.89', ':', '0.056277', ',', '(', 'Anolis barahonae', ':', '0.2114890000', ',', 'Anolis cuvieri', ':', '0.1686700000', ')', '1.00', ':', '0.084190', ',', '(', 'Anolis insolitus', ':', '0.2438820000', ',', 'Anolis olssoni', ':', '0.2568770000', ')', '1.00', ':', '0.050618', ')', '0.86', ':', '0.031679', ',', '(', '(', 'Anolis brevirostris', ':', '0.1801300000', ',', 'Anolis distichus', ':', '0.1151360000', ')', '1.00', ':', '0.123136', ',', '(', '(', 'Anolis cristatellus', ':', '0.2144360000', ',', 'Anolis krugi', ':', '0.1573300000', ')', '0.93', ':', '0.036788', ',', 'Anolis stratulus', ':', '0.1973470000', ')', '1.00', ':', '0.081037', ')', '1.00', ':', '0.056582', ')', '0.77', ':', '0.021826', ',', '(', '(', 'Anolis alutaceus', ':', '0.1619060000', ',', 'Anolis vanidicus', ':', '0.2059960000', ')', '1.00', ':', '0.118216', ',', '(', '(', 'Anolis angusticeps', ':', '0.0857100000', ',', 'Anolis paternus', ':', '0.0595110000', ')', '1.00', ':', '0.153413', ',', 'Anolis loysiana', ':', '0.1836280000', ')', '1.00', ':', '0.042858', ')', '1.00', ':', '0.057139', ',', '(', 'Anolis marcanoi', ':', '0.2359120000', ',', 'Anolis strahmi', ':', '0.1977660000', ')', '1.00', ':', '0.141032', ',', 'Diplolaemus darwinii', ':', '0.6364930000', ')', '1.00', ':', '0.067869', ',', '(', 'Anolis ophiolepis', ':', '0.0945010000', ',', 'Anolis sagrei', ':', '0.0967580000', ')', '1.00', ':', '0.179398', ')', '0.96', ':', '0.044895', ')', ';', 'END',';']
        for e in expected:
            token = tokenizer.read_next_token()
            self.assertEqual(token, e)

    def testComments(self):
        f = "  i [f]t [i] y"
        r2 = StringIO(f)
        tokenizer = nexustokenizer.NexusTokenizer(r2)
        expected = ['i', 't', 'y']
        for e in expected:
            token = tokenizer.read_next_token()
            self.assertEqual(e, token)
