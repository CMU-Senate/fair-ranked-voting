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

from stv_compute import Ballot
from stv_compute import Election

def runTestWithOneCandidateOneSeatWinner():
	description = "One Candidate One Seat Winner Test"
	print(description)
	print("Generating ballots...")
	candidate = "Candidate"
	num_ballots = 10
	ballots = set()

	for i in xrange(num_ballots):
		ballot = Ballot()
		ballot.set_candidate_with_rank(candidate, 1)
		ballots.add(ballot)

	print("Running election...")
	election = Election()
	election.name = description
	election.seats = 1
	election.ballots = ballots

	winners = election.compute_winners(verbose=True)
	print(winners)

def runTestWithThreeCandidatesOneSeatNoConfidence():
	description = "Three Candidates One Seat No Confidence Test"
	print(description)
	print("Generating ballots...")
	candidateOne = "Devin Gund"
	candidateTwo = "Hillary Clinton"
	candidateThree = "Donald Trump"
	ballots = set()

	# Candidate-One-preferred ballots
	for i in xrange(2):
		ballot = Ballot()
		ballot.set_candidate_with_rank(candidateOne, 1)
		ballots.add(ballot)
		
	# Candidate-Two-preferred ballots
	for i in xrange(1):
		ballot = Ballot()
		ballot.set_candidate_with_rank(candidateTwo, 1)
		ballot.set_candidate_with_rank(candidateOne, 2)
		ballots.add(ballot)
		
	# Candidate-Three-preferred ballots
	for i in xrange(2):
		ballot = Ballot()
		ballot.set_candidate_with_rank(candidateThree, 1)
		ballots.add(ballot)
		
	# No-Confidence-preferred ballots
	for i in xrange(2):
		ballot = Ballot()
		ballot.set_candidate_with_rank(Ballot.NO_CONFIDENCE, 1)
		ballots.add(ballot)

	print("Running election...")
	election = Election()
	election.name = description
	election.seats = 1
	election.ballots = ballots

	winners = election.compute_winners(verbose=True)
	print(winners)

def runTestWithTwoCandidatesOneSeat():
	description = "Two Candidates One Seat Winner Test"
	print(description)
	print("Generating ballots...")
	candidateOne = "Candidate One"
	candidateTwo = "Candidate Two"
	num_ballots = 10
	ballots = set()

	for i in xrange(num_ballots):
		ballot = Ballot()
		if i < .4 * num_ballots:
			ballot.set_candidate_with_rank(candidateOne, 1)
		else:
			ballot.set_candidate_with_rank(candidateTwo, 1)
		ballots.add(ballot)

	print("Running election...")
	election = Election()
	election.name = description
	election.seats = 1
	election.ballots = ballots

	winners = election.compute_winners(verbose=True)
	print(winners)

def runTestWithOneCandidateTwoSeats():
	description = "One Candidate Two Seats Winner Test"
	print(description)
	print("Generating ballots...")
	candidate = "Candidate"
	num_ballots = 10
	ballots = set()

	for i in xrange(num_ballots):
		ballot = Ballot()
		ballot.set_candidate_with_rank(candidate, 1)
		ballots.add(ballot)

	print("Running election...")
	election = Election()
	election.name = description
	election.seats = 2
	election.ballots = ballots

	winners = election.compute_winners(verbose=True)
	print(winners)

def runTestWithTwoCandidatesTwoSeats():
	description = "Two Candidates Two Seats Winner Test"
	print(description)
	print("Generating ballots...")
	candidateOne = "Candidate One"
	candidateTwo = "Candidate Two"
	num_ballots = 10
	ballots = set()

	for i in xrange(num_ballots):
		ballot = Ballot()
		if i < .4 * num_ballots:
			ballot.set_candidate_with_rank(candidateOne, 1)
			ballot.set_candidate_with_rank(candidateTwo, 2)
		else:
			ballot.set_candidate_with_rank(candidateTwo, 1)
			ballot.set_candidate_with_rank(candidateOne, 2)
		ballots.add(ballot)

	print("Running election...")
	election = Election()
	election.name = description
	election.seats = 2
	election.ballots = ballots

	winners = election.compute_winners(verbose=True)
	print(winners)

def runTestWithThreeCandidatesTwoSeats():
	description = "Three Candidates Two Seats"
	print(description)
	print("Generating ballots...")
	candidateOne = "Candidate One"
	candidateTwo = "Candidate Two"
	candidateThree = "Candidate Three"
	ballots = set()

	# Candidate-One-preferred ballots
	for i in xrange(2):
		ballot = Ballot()
		ballot.set_candidate_with_rank(candidateOne, 1)
		ballot.set_candidate_with_rank(candidateThree, 2)
		ballots.add(ballot)
		
	# Candidate-Two-preferred ballots
	for i in xrange(2):
		ballot = Ballot()
		ballot.set_candidate_with_rank(candidateTwo, 1)
		ballot.set_candidate_with_rank(Ballot.NO_CONFIDENCE, 2)
		ballots.add(ballot)
	
	# Candidate-Three-preferred ballots
	for i in xrange(1):
		ballot = Ballot()
		ballot.set_candidate_with_rank(candidateThree, 1)
		ballot.set_candidate_with_rank(candidateOne, 2)
		ballot.set_candidate_with_rank(Ballot.NO_CONFIDENCE, 3)
		ballots.add(ballot)

	print("Running election...")
	election = Election()
	election.name = description
	election.seats = 2
	election.ballots = ballots

	winners = election.compute_winners(verbose=True)
	print(winners)

def runTestWithRandomTiebreakBetweenTwoLosers():
	description = "Random Tiebreak Between Losing Candidates Test"
	print(description)
	print("Generating ballots...")
	candidateOne = "Candidate One"
	candidateTwo = "Candidate Two"
	candidateThree = "Candidate Three"
	candidateFour = "Candidate Four"
	num_ballots = 15
	ballots = set()
	
	# Candidate-One-preferred ballots
	for i in xrange(6):
		ballot = Ballot()
		ballot.set_candidate_with_rank(candidateOne, 1)
		ballots.add(ballot)
	
	# Candidate-Two-preferred ballots
	for i in xrange(5):
		ballot = Ballot()
		ballot.set_candidate_with_rank(candidateTwo, 1)
		ballots.add(ballot)
	
	# Candidate-Three-preferred ballots
	for i in xrange(2):
		ballot = Ballot()
		ballot.set_candidate_with_rank(candidateThree, 1)
		ballot.set_candidate_with_rank(candidateFour, 2)
		ballots.add(ballot)
	
	# Candidate-Four-preferred ballots
	for i in xrange(2):
		ballot = Ballot()
		ballot.set_candidate_with_rank(candidateFour, 1)
		ballot.set_candidate_with_rank(candidateThree, 2)
		ballots.add(ballot)

	print("Running election...")
	election = Election()
	election.name = description
	election.seats = 2
	election.ballots = ballots
	election.is_final_tiebreak_manual = True

	winners = election.compute_winners(verbose=True)
	print(winners)

def runTestWithRandomTiebreakToDetermineWinner():
	description = "Random Tiebreak Required To Determine Winner Test"
	print(description)
	print("Generating ballots...")
	candidateOne = "Candidate One"
	candidateTwo = "Candidate Two"
	candidateThree = "Candidate Three"
	candidateFour = "Candidate Four"
	num_ballots = 15
	ballots = set()
		
	# Candidate-One-preferred ballots
	for i in xrange(6):
		ballot = Ballot()
		ballot.set_candidate_with_rank(candidateOne, 1)
		ballots.add(ballot)
		
	# Candidate-Two-preferred ballots
	for i in xrange(3):
		ballot = Ballot()
		ballot.set_candidate_with_rank(candidateTwo, 1)
		ballots.add(ballot)
		
	# Candidate-Three-preferred ballots
	for i in xrange(3):
		ballot = Ballot()
		ballot.set_candidate_with_rank(candidateThree, 1)
		ballots.add(ballot)
		
	# Candidate-Four-preferred ballots
	for i in xrange(3):
		ballot = Ballot()
		ballot.set_candidate_with_rank(candidateFour, 1)
		ballots.add(ballot)

	print("Running election...")
	election = Election()
	election.name = description
	election.seats = 2
	election.ballots = ballots
	election.is_final_tiebreak_manual = True

	winners = election.compute_winners(verbose=True)
	print(winners)

def runTest2000ElectionApproximation():
	description = "2000 Election Approximation Test"
	print(description)
	print("Generating ballots...")
	nader = "Ralph Nader"
	bush = "George Bush"
	gore = "Al Gore"
	num_ballots = 100000
	ballots = set()

	naderPercentage = .03
	bushPercentage = .49
	gorePercentage = .48

	for i in xrange(num_ballots):
		ballot = Ballot()
		if i < naderPercentage * num_ballots:
			ballot.set_candidate_with_rank(nader, 1)
			ballot.set_candidate_with_rank(gore, 2)
		elif i < (naderPercentage + bushPercentage) * num_ballots:
			ballot.set_candidate_with_rank(bush, 1)
			ballot.set_candidate_with_rank(Ballot.NO_CONFIDENCE, 2)
		else:
			ballot.set_candidate_with_rank(gore, 1)
			ballot.set_candidate_with_rank(nader, 2)
		ballots.add(ballot)

	print("Running election...")
	election = Election()
	election.name = description
	election.seats = 1
	election.ballots = ballots

	winners = election.compute_winners(verbose=True)
	print(winners)

def runTestCGPGreyAnimalKingdom():
	description = "CGP Grey's Politics in the Animal Kingdom Test"
	print(description)
	print("Generating ballots...")
	tarsier = "Tarsier"
	gorilla = "Gorilla"
	monkey = "Monkey"
	tiger = "Tiger"
	lynx = "Lynx"
	num_ballots = 10000
	ballots = set()
	
	tarsier_percentage = .05
	gorilla_percentage = .28
	monkey_percentage = .33
	tiger_percentage = .21
	lynx_percentage = .13
	
	tarsier_max_range = tarsier_percentage
	gorilla_max_range = tarsier_max_range + gorilla_percentage
	monkey_max_range = gorilla_max_range + monkey_percentage
	tiger_max_range = monkey_max_range + tiger_percentage
	
	for i in xrange(num_ballots):
		ballot = Ballot()
		if i < tarsier_max_range * num_ballots:
			# tarsier-preferred ballots
			ballot.set_candidate_with_rank(tarsier, 1)
			ballot.set_candidate_with_rank(gorilla, 2)
		elif i < gorilla_max_range * num_ballots:
			# gorilla-preferred ballots
			ballot.set_candidate_with_rank(gorilla, 1)
			ballot.set_candidate_with_rank(tarsier, 2)
			ballot.set_candidate_with_rank(monkey, 3)
		elif i < monkey_max_range * num_ballots:
			# monkey-preferred ballots
			ballot.set_candidate_with_rank(monkey, 1)
		elif i < tiger_max_range * num_ballots:
			# tiger-preferred ballots
			ballot.set_candidate_with_rank(tiger, 1)
		else:
			# lynx-preferred ballots
			ballot.set_candidate_with_rank(lynx, 1)
			ballot.set_candidate_with_rank(tiger, 2)
			ballot.set_candidate_with_rank(tarsier, 3)
			ballot.set_candidate_with_rank(monkey, 4)
			ballot.set_candidate_with_rank(gorilla, 5)
		ballots.add(ballot)

	print("Running election...")
	election = Election()
	election.name = description
	election.seats = 3
	election.ballots = ballots

	winners = election.compute_winners(verbose=True)
	print(winners)

def runTestWikipediaFoodSelection():
	description = "Wikipedia's Food Selection Example Test"
	print(description)
	print("Generating ballots...")
	oranges = "Oranges"
	pears = "Pears"
	chocolate = "Chocolate"
	strawberries = "Strawberries"
	sweets = "Sweets"
	ballots = set()
	
	# Oranges-preferred ballots
	for i in xrange(4):
		ballot = Ballot()
		ballot.set_candidate_with_rank(oranges, 1)
		ballots.add(ballot)
	
	# Pears-preferred ballots
	for i in xrange(2):
		ballot = Ballot()
		ballot.set_candidate_with_rank(pears, 1)
		ballot.set_candidate_with_rank(oranges, 2)
		ballots.add(ballot)
	
	# Chocolate-preferred ballots (type 1)
	for i in xrange(8):
		ballot = Ballot()
		ballot.set_candidate_with_rank(chocolate, 1)
		ballot.set_candidate_with_rank(strawberries, 2)
		ballots.add(ballot)
	
	# Chocolate-preferred ballots (type 2)
	for i in xrange(4):
		ballot = Ballot()
		ballot.set_candidate_with_rank(chocolate, 1)
		ballot.set_candidate_with_rank(sweets, 2)
		ballots.add(ballot)
	
	# Strawberries-preferred ballots
	for i in xrange(1):
		ballot = Ballot()
		ballot.set_candidate_with_rank(strawberries, 1)
		ballots.add(ballot)
	
	# Sweets-preferred ballots
	for i in xrange(1):
		ballot = Ballot()
		ballot.set_candidate_with_rank(sweets, 1)
		ballots.add(ballot)

	print("Running election...")
	election = Election()
	election.name = description
	election.seats = 3
	election.ballots = ballots

	winners = election.compute_winners(verbose=True)
	print(winners)

runTestWikipediaFoodSelection()