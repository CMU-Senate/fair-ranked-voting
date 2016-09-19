# stv_compute.py: computes election results using single transferable vote
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

def runTestWithOneCandidateOneSeatNoConfidence():
	description = "One Candidate One Seat No Confidence Test"
	print(description)
	print("Generating ballots...")
	candidate = "Candidate"
	num_ballots = 10
	ballots = set()

	for i in xrange(num_ballots):
		ballot = Ballot()
		ballot.set_candidate_with_rank(Ballot.NO_CONFIDENCE, 1)
		ballot.set_candidate_with_rank(candidate, 2)
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

def runTestWithThreeCandidatesTwoSeatsTiebreak():
	description = "Three Candidates Two Seats Tiebreak"
	print(description)
	print("Generating ballots...")
	candidateOne = "Candidate One"
	candidateTwo = "Candidate Two"
	candidateThree = "Candidate Three"
	num_ballots = 100
	ballots = set()

	for i in xrange(num_ballots):
		ballot = Ballot()
		if i < .32 * num_ballots:
			ballot.set_candidate_with_rank(candidateOne, 1)
			ballot.set_candidate_with_rank(candidateTwo, 2)
		elif i < .64 * num_ballots:
			ballot.set_candidate_with_rank(candidateTwo, 1)
			ballot.set_candidate_with_rank(candidateOne, 2)
		else:
			ballot.set_candidate_with_rank(candidateThree, 1)
		ballots.add(ballot)

	print("Running election...")
	election = Election()
	election.name = description
	election.seats = 2
	election.ballots = ballots

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

runTest2000ElectionApproximation()

