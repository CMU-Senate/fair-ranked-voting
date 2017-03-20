#!/usr/bin/python3
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

# String representing the input for No Confidence
NC_STRING = 'No Confidence'

# String representing the abbreviated input for No Confidence
NC_STRING_SHORT = 'NC'

def input_string_is_no_confidence(candidate_input):
    """Checks if an input string represents No Confidence.

    Args:
        candidate_input: String representing user input for a Candidate. The
            expected format is 'uid' or optionally 'uid (name)'.

    Returns:
        Boolean indicating if the input string represents No Confidence or not.
    """
    return (candidate_input.lower() == NC_STRING.lower
            or candidate_input.lower() == NC_STRING_SHORT.lower())

def candidate_from_input(candidate_input):
    """Returns a Candidate representing the input string.

    Args:
        candidate_input: String representing user input for a Candidate. The
            expected format is 'uid' or optionally 'uid (name)'.

    Returns:
        Candidate representing the input uid (and optionally name).
    """
    if input_string_is_no_confidence(candidate_input):
        return NoConfidence()
    else:
        expr = '(.*?)\s*\((.*?)\)'
        regex = re.compile(expr)
        result = regex.match(candidate_input)
        if result != None:
            uid = result.group(1)
            name = result.group(2)
        else:
            uid = candidate_input
            name = None
        return Candidate(uid, name=name)

def ballot_from_candidate_inputs(candidate_inputs):
    """Returns a Ballot of Candidates representing the input strings.

    Args:
        candidate_inputs: List of Strings representing user input for a
            Candidate. The expected format is 'uid' or optionally 'uid (name)'.

    Returns:
        Ballot representing the input Candidates.
    """
    candidates = list()
    for candidate_input in candidate_inputs:
        candidate = candidate_from_input(candidate_input)
        candidates.append(candidate)
    ballot = Ballot(candidates=candidates)
    return ballot

def ballots_from_input():
    """Return Ballots from command-line user input.

    Returns:
        List of Candidates representing user input.
    """
    ballots = list()
    ballot_number = 0

    def print_ballot_instructions():
        """"Prints ballot input instructions."""
        print('Instructions:')
        print('Enter candidates on the ballot in a comma-separated list of',
              'unique identifiers, ordered from most to least preferred.')
        print('The expected input format for a candidate is \'uid\' or',
              'optionally \'uid (name)\'.')
        print('{} may also be abbreviated as {}.'.format(NC_STRING,
                                                         NC_STRING_SHORT))
        print('Press enter with an empty ballot to end input.',
              'Type \'undo\' to remove the last ballot.',
              'Type \'help\' to view these instructions again.')

    print_ballot_instructions()
    while True:
        ballot_input = input('\nBallot {}: '.format(ballot_number)).strip()

        if ballot_input == '':
            return ballots

        elif ballot_input.lower() == 'help':
            print_ballot_instructions()

        elif ballot_input.lower() == 'undo':
            if ballot_number > 0:
                ballots.pop()
                ballot_number -= 1

        else:
            candidate_inputs = [candidate_input.strip()
                                for candidate_input in ballot_input.split(',')]
            ballot = ballot_from_candidate_inputs(candidate_inputs)
            ballots.append(ballot)
            ballot_number += 1

def ballots_from_csv(filename):
    """Return Ballots from CSV user input.

    Args:
        filename: The filepath of the CSV file containing the user input.

    Returns:
        List of Ballots representing user input.
    """
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
                ballot = ballot_from_candidate_inputs(row)
                ballots.append(ballot)
    f.close()
    return ballots

def ballots_from_txt(filename):
    """Return Ballots from TXT user input.

    Args:
        filename: The filepath of the TXT file containing the user input.

    Returns:
        List of Ballots representing user input.
    """
    ballots = list()
    with open(filename) as f:
        for line in f:
            if len(line.strip()) > 0:
                candidate_inputs = [candidate_input.strip()
                                    for candidate_input in line.split(',')]
                ballot = ballot_from_candidate_inputs(candidate_inputs)
                ballots.append(ballot)
    f.close()
    return ballots

def ballots_from_file(filename):
    """Return Ballots from file user input.

    Args:
        filename: The filepath of the CSV or TXT file containing the user input.

    Returns:
        List of Ballots representing user input.
    """
    if filename.lower().endswith('.csv'):
        return ballots_from_csv(filename)
    elif filename.lower().endswith('.txt'):
        return ballots_from_txt(filename)
    else:
        raise ValueError('Invalid filetype. Accepts .csv, .txt.')

def parse_args():
    """Parses command-line election arguments.

    Returns:
        argparse.Namespace containing election arguments.
    """
    description = ('Configure and run an election. Ballots ranking candidates '
                   'may be imported from a CSV or TXT file, or manual input if '
                   'no file is specified. The expected input format for a '
                   'candidate is \'uid\' or optionally \'uid (name)\'.')
    parser = argparse.ArgumentParser(description=description)
    required_group = parser.add_argument_group('required arguments')
    
    # Number of seats (required)
    required_group.add_argument('-s','--seats', help='Number of seats',
                                type=int, required=True)

    # Alphanumeric string for breaking ties
    parser.add_argument('-a','--alphanumeric',
                        help='Alphanumeric string for breaking ties')
    
    # File containing ballots
    parser.add_argument('-b','--ballots', help='File containing ballots')
    
    # Disallow No Confidence from being eliminated
    parser.add_argument('-c','--disallow-nc-elimination',
                        help='No Confidence cannot be eliminated',
                        action='store_true')
    
    # Name of Election
    parser.add_argument('-n','--name', help='Name of election', default='')
    
    # Disallow random tiebreaks, ending the election instead
    parser.add_argument('-r','--disallow-random-tiebreak',
                        help='Halt election instead of using random tiebreak',
                        action='store_true')
    
    # Verbose printing of election results
    parser.add_argument('-v', '--verbose',
                        help='Verbose printing of election results',
                        action='store_true')

    args = parser.parse_args()
    return args

def process_args(args):
    """Processes command-line election arguments and runs election.

    Args:
        argparse.Namespace containing election arguments.
    """
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

    print('Winners:')
    for candidate in results.candidates_elected:
        print(candidate)


if __name__ == '__main__':
    election_args = parse_args()
    process_args(election_args)
