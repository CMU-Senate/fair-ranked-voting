# stv_compute_tests.py: computes election results using single transferable vote
# Copyright (C) 2016 Carnegie Mellon Student Senate. Created by Devin Gund.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

from election import *
import unittest

candidate_for_id = {
    'NC': NoConfidence(),
    'A': Candidate('Devin Gund', 'dgund'),
    'B': Candidate('George Washington', 'gwashington'),
    'C': Candidate('John Adams', 'jadams'),
    'D': Candidate('Thomas Jefferson', 'tjefferson'),
    'E': Candidate('James Madison', 'jmadison'),
    'F': Candidate('James Monroe', 'jmonroe'),
    'G': Candidate('John Quincy Adams', 'jqadams'),
    'H': Candidate('Andrew Jackson', 'ajackson'),
    'I': Candidate('Martin Van Buren', 'mvburen'),
    'J': Candidate('William Harrison', 'wharrison'),
    'K': Candidate('John Tyler', 'jtyler'),
    'L': Candidate('James Polk', 'jpolk'),
    'M': Candidate('Zachary Taylor', 'ztaylor'),
    'N': Candidate('Millard Fillmore', 'mfillmore'),
    'O': Candidate('Franklin Pierce', 'fpierce'),
    'P': Candidate('James Buchanan', 'jbuchanan'),
    'Q': Candidate('Abraham Lincoln', 'alincoln'),
    'R': Candidate('Andrew Johnson', 'ajohnson'),
    'S': Candidate('Ulysses Grant', 'ugrant'),
    'T': Candidate('Rutherford Hayes', 'rhayes'),
    'U': Candidate('James Garfield', 'jgarfield'),
    'V': Candidate('Chester Arthur', 'carthur'),
    'W': Candidate('Grover Cleveland', 'gcleveland'),
    'X': Candidate('Benjamin Harrison', 'bharrison'),
    'Y': Candidate('William McKinley', 'wmckinley'),
    'Z': Candidate('Theodore Roosevelt', 'troosevelt'),
}

def candidates_for_ids(candidate_ids):
    candidates = []
    for candidate_id in candidate_ids:
        candidates.append(candidate_for_id[candidate_id])
    return candidates

def ballots_for_candidates(candidates, count):
    ballots = set()
    for i in xrange(count):
        ballot = Ballot()
        ballot.set_candidates(candidates)
        ballots.add(ballot)
    return ballots

def ballots_for_ids(candidate_ids, count):
    return ballots_for_candidates(candidates_for_ids(candidate_ids), count)

class TestSmallElections(unittest.TestCase):

	def test_1_candidate_1_seat(self):
		"""
		Tests a 1 candidate election for 1 seat.
		Expected winners: A

		Round 0
			Ballots:
				10 * [A]
			Votes:
				A: 10
			Threshold: (10) / (1+1) + 1 = 6
			Result: A is elected
		"""
		# Setup
		expected_winners = set(candidates_for_ids(['A']))
		seats = 1
		tiebreak_alphanumeric = 'abcdefghijklmnopqrstuvwxyz'
		ballots = set(
			ballots_for_ids(['A'], 10))

		# Test
		election = Election(seats=seats,
							ballots=ballots,
							random_alphanumeric=tiebreak_alphanumeric)
		results = election.compute_results()
		self.assertEqual(expected_winners, results.candidates_elected)

	def test_2_candidates_1_seat(self):
		"""
		Tests a 2 candidate election for 1 seat.
		Expected winners: B

		Round 0
			Ballots:
				 5 * [A, B]
				10 * [B, A]
			Votes:
				A: 5
				B: 10
			Threshold: (15) / (1+1) + 1 = 8.5
			Result: B is elected
		"""
		# Setup
		expected_winners = set(candidates_for_ids(['B']))
		seats = 1
		tiebreak_alphanumeric = 'abcdefghijklmnopqrstuvwxyz'

		ballots = set(
			ballots_for_ids(['A', 'B'], 5) |
			ballots_for_ids(['B', 'A'], 10))

		# Test
		election = Election(seats=seats,
							ballots=ballots,
							random_alphanumeric=tiebreak_alphanumeric)
		results = election.compute_results()
		self.assertEqual(expected_winners, results.candidates_elected)

	def test_3_candidates_1_seat(self):
		"""
		Tests a 3 candidate election for 1 seat.
		Expected winners: C

		Round 0
			Ballots:
				 5 * [A, C]
				10 * [B]
				 7 * [C]
			Votes:
				A: 7
				B: 10
				C: 5
			Threshold: (7+10+5) / (1+1) + 1 = 12
			Result: A is eliminated

		Round 1
			Ballots:
				10 * [B]
				12 * [C]
			Votes:
				B: 10
				C: 12
			Threshold: (7+10+5) / (1+1) + 1 = 12
			Result: C is elected
		"""
		# Setup
		expected_winners = set(candidates_for_ids(['C']))
		seats = 1
		tiebreak_alphanumeric = 'abcdefghijklmnopqrstuvwxyz'

		ballots = set(
			ballots_for_ids(['A', 'C'], 5) |
			ballots_for_ids(['B'], 10) |
			ballots_for_ids(['C'], 7))

		# Test
		election = Election(seats=seats,
							ballots=ballots,
							random_alphanumeric=tiebreak_alphanumeric)
		results = election.compute_results()
		self.assertEqual(expected_winners, results.candidates_elected)

	def test_1_candidate_2_seats(self):
		"""
		Tests a 1 candidate election for 2 seats.
		Expected winners: A

		Round 0
			Ballots:
				 10 * [A]
			Votes:
				A: 10
			Threshold: (10) / (2+1) + 1 = 4.333
			Result: A is elected
		"""
		# Setup
		expected_winners = set(candidates_for_ids(['A']))
		seats = 2
		tiebreak_alphanumeric = 'abcdefghijklmnopqrstuvwxyz'

		ballots = set(
			ballots_for_ids(['A'], 10))

		# Test
		election = Election(seats=seats,
							ballots=ballots,
							random_alphanumeric=tiebreak_alphanumeric)
		results = election.compute_results()
		self.assertEqual(expected_winners, results.candidates_elected)

	def test_4_candidates_2_seats(self):
		"""
		Tests a 4 candidate election for 2 seats.
		Expected winners: A, B

		Round 0
			Ballots:
				10 * [A, NC]
				16 * [B, NC]
				15 * [C, NC]
				 7 * [D, A]
			Votes:
				A: 10
				B: 16
				C: 15
				D: 7
			Threshold: (10+16+15+7) / (2+1) + 1 = 17
			Result: D is eliminated

		Round 1
			Ballots:
				10 * [A, NC]
				16 * [B, NC]
				15 * [C, NC]
				 7 * [A]
			Votes:
				A: 17
				B: 16
				C: 15
			Threshold: (10+16+15+7) / (2+1) + 1 = 17
			Result: A is elected

		Round 2
			Ballots:
				16 * [B, NC]
				15 * [C, NC]
			Votes:
				B: 16
				C: 15
			Threshold: (16+15) / (1+1) + 1 = 16.5
			Result: C is eliminated

		Round 3
			Ballots:
				16 * [B, NC]
				15 * [NC]
			Votes:
				B: 16
				NC: 15
			Threshold: (16+15) / (1+1) + 1 = 16.5
			Result: NC is eliminated

		Round 4
			Ballots:
				16 [B, NC]
			Votes:
				B: 16
			Threshold: (16+15) / (1+1) + 1 = 16.5
			Result: B is elected
		"""
		# Setup
		expected_winners = set(candidates_for_ids(['A', 'B']))
		seats = 2
		tiebreak_alphanumeric = 'abcdefghijklmnopqrstuvwxyz'

		ballots = set(
			ballots_for_ids(['A', 'NC'], 10) |
			ballots_for_ids(['B', 'NC'], 16) |
			ballots_for_ids(['C', 'NC'], 15) |
			ballots_for_ids(['D', 'A'], 7))

		# Test
		election = Election(seats=seats,
							ballots=ballots,
							random_alphanumeric=tiebreak_alphanumeric)
		results = election.compute_results()
		self.assertEqual(expected_winners, results.candidates_elected)

class TestNoConfidence(unittest.TestCase):

	def test_nc_halt_early(self):
		"""
		Tests a 3 candidate election for 3 seats.
		Once No Confidence is elected, the election should end.
		Expected winners: B, NC

		Round 0
			Ballots:
			    5 * [A, NC]
				6 * [B, NC]
				4 * [C, NC]
				5 * [NC]
			Votes:
				A: 5
				B: 6
				C: 4
			   NC: 5
			Threshold: (6+5+4+5) / (3+1) + 1 = 6
			Result: B is elected

		Round 1
			Ballots:
			    5 * [A, NC]
				4 * [C, NC]
				5 * [NC]
			Votes:
				A: 5
				C: 4
			   NC: 5
			Threshold: (5+4+5) / (2+1) + 1 = 5.666
			Result: C is eliminated

		Round 2
			Ballots:
			    5 * [A, NC]
				9 * [NC]
			Votes:
				A: 5
			   NC: 9
			Threshold: (5+9) / (2+1) + 1 = 5.666
			Result: NC is elected
		"""
		# Setup
		expected_winners = set(candidates_for_ids(['B','NC']))
		seats = 3
		tiebreak_alphanumeric = 'abcdefghijklmnopqrstuvwxyz'

		ballots = set(
			ballots_for_ids(['A', 'NC'], 5) |
			ballots_for_ids(['B', 'NC'], 6) |
			ballots_for_ids(['C', 'NC'], 4) |
			ballots_for_ids(['NC'], 5))

		# Test
		election = Election(seats=seats,
							ballots=ballots,
							random_alphanumeric=tiebreak_alphanumeric)
		results = election.compute_results()
		self.assertEqual(expected_winners, results.candidates_elected)

	def test_nc_halt_end(self):
		"""
		Tests a 2 candidate election for 3 seats.
		When empty seats are filled, only candidates with votes exceeding that
		of No Confidence may be elected.
		Expected winners: A, NC

		Round 0
			Ballots:
			   10 * [A]
				6 * [B]
				8 * [NC]
			Votes:
				A: 10
				B: 6
			   NC: 8
			Threshold: (10+6+8) / (3+1) + 1 = 7
			Result: A is elected
			As the 3 candidates (including No Confidence) can fill the 3 vacant
			seats, the candidates are slated to fill the seats. However, B's
			votes fall below that of No Confidence, so B is not elected.
		"""
		# Setup
		expected_winners = set(candidates_for_ids(['A','NC']))
		seats = 3
		tiebreak_alphanumeric = 'abcdefghijklmnopqrstuvwxyz'

		ballots = set(
			ballots_for_ids(['A'], 10) |
			ballots_for_ids(['B'], 6) |
			ballots_for_ids(['NC'], 8))

		# Test
		election = Election(seats=seats,
							ballots=ballots,
							random_alphanumeric=tiebreak_alphanumeric)
		results = election.compute_results()
		self.assertEqual(expected_winners, results.candidates_elected)

	def test_election_with_nc_elimination(self):
		"""
		Tests a 3 candidate election for 1 seat.
		All of the ballots list a single candidate followed by No Confidence.
		Expected winners: A

		Round 0
			Ballots:
				6 * [A, NC]
				5 * [B, NC]
				1 * [C, NC]
			Votes:
				A: 6
				B: 5
				C: 1
			Threshold: (6+5+1) / (1+1) + 1 = 7
			Result: C is eliminated

		Round 1
			Ballots:
				6 * [A, NC]
				5 * [B, NC]
				1 * [NC]

			Votes:
				A: 6
				B: 5
				NC: 1
			Threshold: (6+5+1) / (1+1) + 1 = 7
			Result: NC is eliminated

		Round 2
			Ballots:
				6 * [A]
				5 * [B]

			Votes:
				A: 6
				B: 5
			Threshold: (6+5) / (1+1) + 1 = 6.5
			Result: B is eliminated

		Round 3
			Ballots:
				6 * [A]

			Votes:
				A: 6
			Threshold: (6) / (1+1) + 1 = 4
			Result: A is elected
		"""
		# Setup
		expected_winners = set(candidates_for_ids(['A']))
		seats = 1
		tiebreak_alphanumeric = 'abcdefghijklmnopqrstuvwxyz'

		ballots = set(
			ballots_for_ids(['A', 'NC'], 6) |
			ballots_for_ids(['B', 'NC'], 5) |
			ballots_for_ids(['C', 'NC'], 1))

		# Test
		election = Election(seats=seats,
							ballots=ballots,
							random_alphanumeric=tiebreak_alphanumeric)
		results = election.compute_results()
		self.assertEqual(expected_winners, results.candidates_elected)

	def test_election_without_nc_elimination(self):
		"""
		Tests a 3 candidate election for 1 seat.
		All of the ballots list a single candidate followed by No Confidence.
		No Confidence is cannot be eliminated for having the fewest votes.
		Expected winners: NC

		Round 0
			Ballots:
				6 * [A, NC]
				5 * [B, NC]
				1 * [C, NC]
			Votes:
				A: 6
				B: 5
				C: 1
			Threshold: (6+5+1) / (1+1) + 1 = 7
			Result: C is eliminated

		Round 1
			Ballots:
				6 * [A, NC]
				5 * [B, NC]
				1 * [NC]
			Votes:
				A: 6
				B: 5
				NC: 1
			Threshold: (6+5+1) / (1+1) + 1 = 7
			Result: B is eliminated (because NC cannot be)

		Round 2
			Ballots:
				6 * [A, NC]
				6 * [NC]
			Votes:
				A: 6
				NC: 6
			Threshold: (6+6) / (1+1) + 1 = 7
			Result: A is eliminated (because NC cannot be)

		Round 3
			Ballots:
				12 * [NC]
			Votes:
				NC: 12
			Threshold: (12) / (1+1) + 1 = 7
			Result: NC is elected
		"""
		# Setup
		expected_winners = set(candidates_for_ids(['NC']))
		seats = 1
		tiebreak_alphanumeric = 'abcdefghijklmnopqrstuvwxyz'

		ballots = set(
			ballots_for_ids(['A', 'NC'], 6) |
			ballots_for_ids(['B', 'NC'], 5) |
			ballots_for_ids(['C', 'NC'], 1))

		# Test
		election = Election(seats=seats,
							ballots=ballots,
							random_alphanumeric=tiebreak_alphanumeric,
							can_eliminate_no_confidence=False)
		results = election.compute_results()
		self.assertEqual(expected_winners, results.candidates_elected)

class TestTiebreaks(unittest.TestCase):
	
	def test_backward_tiebreak(self):
		"""
		Tests a 3 candidate election for 2 seats.
		In the event of a tie to eliminate a candidate, eliminate the candidate
		with the fewest votes in the previous round. Repeat for all previous
		rounds if necessary.
		Expected winners: A, C

		Round 0
			Ballots:
				6 * [A]
				3 * [B]
				2 * [C]
				1 * [D, C]
			Votes:
				A: 6
				B: 3
				C: 3
				D: 1
			Threshold: (6+3+2+1) / (2+1) + 1 = 5
			Result: A is elected

		Round 1
			Ballots:
				3 * [B]
				2 * [C]
				1 * [D, C]
			Votes:
				B: 3
				C: 3
				D: 1
			Threshold: (3+2+1) / (1+1) + 1 = 4
			Result: D is eliminated

		Round 2
			Ballots:
				3 * [B]
				3 * [C]
			Votes:
				B: 3
				C: 3
			Threshold: (3+3) / (1+1) + 1 = 4
			Result: C is eliminated
			B and C are tied for fewest votes, but C has fewer votes in the
			previous round, so C is eliminated.

		Round 3
			Ballots:
				3 * [B]
			Votes:
				B: 3
			Threshold: (3) / (1+1) + 1 = 2.5
			Result: B is elected
		"""
		# Setup
		expected_winners = set(candidates_for_ids(['A', 'B']))
		seats = 2
		tiebreak_alphanumeric = 'abcdefghijklmnopqrstuvwxyz'

		ballots = set(
			ballots_for_ids(['A'], 6) |
			ballots_for_ids(['B'], 3) |
			ballots_for_ids(['C'], 2) |
			ballots_for_ids(['D', 'C'], 1))

		# Test
		election = Election(seats=seats,
							ballots=ballots,
							random_alphanumeric=tiebreak_alphanumeric)
		results = election.compute_results()
		self.assertEqual(expected_winners, results.candidates_elected)

	def test_forward_tiebreak(self):
		"""
		Tests a 3 candidate election for 2 seats.
		In the event of a tie to eliminate a candidate, and no backward
		tiebreak, eliminate the candidate with the fewest next-choice votes.
		Repeat for all subsequent ranks as necessary.
		Expected winners: A, C

		Round 0
			Ballots:
				6 * [A]
				3 * [B, C]
				3 * [C]
			Votes:
				A: 6
				B: 3
				C: 3
			Threshold: (6+3+3) / (2+1) + 1 = 5
			Result: A is elected

		Round 1
			Ballots:
				3 * [B, C]
				3 * [C]
			Votes:
				B: 3
				C: 3
			Threshold: (3+2+1) / (1+1) + 1 = 4
			Result: B is eliminated
			B and C are tied for fewest votes in this and previous rounds.
			B has fewer next-rank votes, so B is eliminated.

		Round 2
			Ballots:
				6 * [C]
			Votes:
				C: 6
			Threshold: (6) / (1+1) + 1 = 4
			Result: C is elected
		"""
		# Setup
		expected_winners = set(candidates_for_ids(['A', 'C']))
		seats = 2
		tiebreak_alphanumeric = 'abcdefghijklmnopqrstuvwxyz'

		ballots = set(
			ballots_for_ids(['A'], 6) |
			ballots_for_ids(['B', 'C'], 3) |
			ballots_for_ids(['C'], 3))

		# Test
		election = Election(seats=seats,
							ballots=ballots,
							random_alphanumeric=tiebreak_alphanumeric)
		results = election.compute_results()
		self.assertEqual(expected_winners, results.candidates_elected)

	def test_random_tiebreak(self):
		"""
		Tests a 3 candidate election for 2 seats.
		In the event of a tie to eliminate a candidate, and no backward
		tiebreak or forward tiebreak, eliminate a random candidate based on uid.
		Expected winners: A, C

		Round 0
			Ballots:
				6 * [A]
				3 * [B]
				3 * [C]
			Votes:
				A: 6
				B: 3
				C: 3
			Threshold: (6+3+3) / (2+1) + 1 = 5
			Result: A is elected

		Round 1
			Ballots:
				3 * [B]
				3 * [C]
			Votes:
				B: 3
				C: 3
			Threshold: (3+3) / (1+1) + 1 = 4
			Result: B is elected
			B and C are tied for fewest votes in this and all previous rounds,
			as well as future ranks. B's uid ('gwashington') is ordered before
			C's uid ('jadams') in the tiebreak_alphanumeric, so B is eliminated.

		Round 2
			Ballots:
				3 * [C]
			Votes:
				C: 3
			Threshold: (3) / (1+1) + 1 = 2.5
			Result: C is elected
		"""
		# Setup
		expected_winners = set(candidates_for_ids(['A', 'C']))
		seats = 2
		tiebreak_alphanumeric = 'abcdefghijklmnopqrstuvwxyz'

		ballots = set(
			ballots_for_ids(['A'], 6) |
			ballots_for_ids(['B'], 3) |
			ballots_for_ids(['C'], 3))

		# Test
		election = Election(seats=seats,
							ballots=ballots,
							random_alphanumeric=tiebreak_alphanumeric)
		results = election.compute_results()
		self.assertEqual(expected_winners, results.candidates_elected)

class TestLargeElections(unittest.TestCase):

	def test_26_candidates_10_seats(self):
		pass

	def test_cgp_grey_animal_kingdom(self):
		pass

	def test_wikipedia_food_selection(self):
		pass


if __name__ == '__main__':
    unittest.main()
