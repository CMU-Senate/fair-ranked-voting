# stv_election.py: runs an election using single transferable vote
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

from election import *

def print_introduction():
	print("Carnegie Mellon Fair Ranked Voting")
	print("Conducting election using single transferable vote")
	print("--------------------------------------------------")

def prompt_election_name():
	election_name = raw_input("\nEnter a name for this election: ")
	return election_name

def prompt_election_seats():
	election_seats = raw_input("How many seats should this election fill: ")
	return int(election_seats)

def print_ballot_instructions(no_confidence_short, run_command, quit_command, undo_command, help_command):
	print("\nInstructions:")
	print("- Input the candidates on a ballot in a comma-separated-list, ordered from most preferred to least preferred.")

	print("- A vote of No Confidence can also be abbreviated as %s." % (no_confidence_short))
	print("- Example: Awesome Candidate, Great Candidate, Average Candidate, No Confidence")

	print("- Special Commands: '%s' to run election, '%s' to remove most recent ballot, '%s' to quit program, '%s' to view these instructions again" % (run_command, quit_command, undo_command, help_command))

def prompt_ballot_command(ballot_count):
	ballot_command = raw_input("\nBallot %d: " % (ballot_count + 1)).strip()
	return ballot_command

def print_conclusion(winners, seats):
	print("\n--------------------------------------------------")
	print("The following candidates(s) have been declared winner to fill %d seat(s):" % (seats))
	for winner in winners:
		print(winner)

def main():
	no_confidence = Ballot.NO_CONFIDENCE
	no_confidence_short = "NC"

	run_command = "run"
	quit_command = "quit"
	undo_command = "undo"
	help_command = "help"

	election_name = None
	election_seats = None
	election_ballots = list()

	print_introduction()

	election_name = prompt_election_name()

	election_seats = prompt_election_seats()

	print_ballot_instructions(no_confidence_short, run_command, quit_command, undo_command, help_command)

	while True:
		ballot_or_command = prompt_ballot_command(len(election_ballots))

		# Empty input
		if len(ballot_or_command) == 0:
			continue

		# 'run' command
		elif ballot_or_command.lower() == run_command:
			# Create the Election
			election = Election(name=election_name, seats=election_seats)
			election.is_final_tiebreak_manual = True
			election.ballots = set(election_ballots)

			# Run the election and compute winners
			winners = election.compute_winners(verbose=True)

			# Print the winners and quit the program
			print_conclusion(winners, election_seats)
			return 0

		# 'quit' command
		elif ballot_or_command.lower() == quit_command:
			# Quit the program
			return 0

		# 'undo' command
		elif ballot_or_command.lower() == undo_command:
			# Pop the last ballot from the list of ballots
			if len(election_ballots) > 0:
				election_ballots.pop()
				print("The most-recent ballot has been removed.")
			else:
				print("There are no ballots to remove.")

		# 'help' command
		elif ballot_or_command.lower() == help_command:
			# Print the instructions again
			print_ballot_instructions(no_confidence_short, run_command, quit_command, undo_command, help_command)

		# Ballot input
		else:
			# Parse the input into a list of strings representing candidates
			ranked_candidates = [candidate_input.strip() for candidate_input in ballot_or_command.split(',')]

			# For each candidate in the list, add them to the Ballot with increasing rank
			ballot = Ballot()
			rank = 1
			for candidate in ranked_candidates:
				# Replace No Confidence abbreviations
				if candidate == no_confidence_short:
					candidate = no_confidence
				ballot.set_candidate_with_rank(candidate, rank)
				rank += 1

			# Add the ballot to the list of ballots
			election_ballots.append(ballot)

if __name__ == "__main__":
	main()
