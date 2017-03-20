# run.py: provides an interface to input ballots and run elections
# Copyright (C) 2016 Devin Gund
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

import argparse
import csv
import re

NC_STRING = "No Confidence"
NC_STRING_SHORT = "NC"

def _input_string_is_no_confidence(input_string):
    return (input_string.lower() == NC_STRING.lower
            or input_string.lower() == NC_STRING_SHORT.lower())

def _candidate_from_input(input_string):
    if _input_string_is_no_confidence(input_string):
        return NoConfidence()
    else:
        expr = '(.*?)\s*\((.*?)\)'
        regex = re.compile(expr)
        result = regex.match(input_string)
        if result != None:
            uid = result.group(1)
            name = result.group(2)
        else:
            uid = input_string
            name = None
        return Candidate(uid, name=name)

def _ballot_from_candidate_inputs(candidate_inputs):
    candidates = list()
    for candidate_input in candidate_inputs:
        candidate = _candidate_from_input(candidate_input)
        candidates.append(candidate)
    ballot = Ballot(candidates=candidates)
    return ballot

def ballots_from_input():
    ballots = list()
    ballot_number = 0

    def print_ballot_instructions():
        print('Enter candidates on the ballot in a comma-separated-list of unique identifiers, ordered from most preferred to least preferred.')
        print('{} may also be abbreviated as {}.'.format(NC_STRING, NC_STRING_SHORT))
        print('Press enter in an empty ballot to end input. Type undo to remove the last ballot.')

    print_ballot_instructions()
    while True:
        ballot_input = input('\nBallot {}: '.format(ballot_number)).strip()

        if ballot_input == '':
            return ballots

        elif ballot_input.lower() == 'help':
            print_ballot_instructions()

        elif ballot_input.lower() == 'undo' and ballot_number > 0:
            ballots.pop()
            ballot_number -= 1

        else:
            candidate_inputs = [candidate_input.strip() for candidate_input in ballot_input.split(',')]
            ballot = _ballot_from_candidate_inputs(candidate_inputs)
            ballots.append(ballot)
            ballot_number += 1

def ballots_from_csv(filename):
    ballots = list()
    with open(filename) as f:
        sniffer = csv.Sniffer()
        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)
        has_header = sniffer.has_header(f.read(1024))
        f.seek(0)
        reader = csv.reader(f, dialect)
        for row in reader:
            if reader.line_num > 0 or not has_header:
                ballot = _ballot_from_candidate_inputs(row)
                ballots.append(ballot)
    f.close()
    return ballots

def ballots_from_txt(filename):
    ballots = list()
    with open(filename) as f:
        for line in f:
            if len(line.strip()) > 0:
                candidate_inputs = [candidate_input.strip() for candidate_input in line.split(',')]
                ballot = _ballot_from_candidate_inputs(candidate_inputs)
                ballots.append(ballot)
    f.close()
    return ballots

def ballots_from_file(filename):
    if filename.lower().endswith('.csv'):
        return ballots_from_csv(filename)
    elif filename.lower().endswith('.txt'):
        return ballots_from_txt(filename)
    else:
        raise ValueError('Invalid filetype. Accepts .csv, .txt.')

def main(args):
    if args.ballots != None:
        ballots = ballots_from_file(args.ballots)
    else:
        ballots = ballots_from_input()

    election = Election(
        ballots,
        args.seats,
        can_eliminate_no_confidence=not(args.disallow_nc_elimination),
        can_random_tiebreak=not(args.disallow_random_tiebreak),
        name=args.name,
        random_alphanumeric=args.alphanumeric
    )

    results = election.compute_results()

    if args.verbose:
        pass

    print("Winners:")
    for candidate in results.candidates_elected:
        print(candidate)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Configure and run an election.')
    required_group = parser.add_argument_group('required arguments')
    # Number of seats
    required_group.add_argument('-s','--seats', help='Number of seats', type=int, required=True)

    # Alphanumeric string for breaking ties
    parser.add_argument('-a','--alphanumeric', help='Alphanumeric string for breaking ties')
    # File containing ballots
    parser.add_argument('-b','--ballots', help='File containing ballots')
    # Disallow No Confidence from being eliminated
    parser.add_argument('-c','--disallow-nc-elimination', help='No Confidence cannot be eliminated', action='store_true')
    # Name of election
    parser.add_argument('-n','--name', help='Name of election', default='')
    # Disallow random tiebreaks, ending the election instead
    parser.add_argument('-r','--disallow-random-tiebreak', help='Halt election instead of using random tiebreak', action='store_true')
    # Verbose printing of election results
    parser.add_argument('-v', '--verbose', help='Verbose printing of election results', action='store_true')

    args = parser.parse_args()
    main(args)
