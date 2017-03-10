# election.py: computes election results using single transferable vote
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

import copy
import string

class Candidate:
    """
    The Candidate class represents a candidate with a name and uid.
    """

    def __init__(self, name, uid):
        # String: Name of the Candidate
        self.name = name

        # String: Unique identifier for the Candidate
        self.uid = uid
    
    def __eq__(self, other):
        if isinstance(other, Candidate):
            return self.uid == other.uid

    def __hash__(self):
        return hash(self.uid)

    def __repr__(self):
        return 'Candidate({!r}, {!r})'.format(self.name, self.uid)

    def __str__(self):
        return '{} ({})'.format(self.name, self.uid)


class NoConfidence(Candidate):
    """
    The NoConfidence class represents the special candidate option
    of voting No Confidence.
    """

    def __init__(self):
        self.name = 'No Confidence'
        self.uid = ''

    def __repr__(self):
        return 'NoConfidence()'


class Ballot:
    """
    The Ballot class represents a ballot consisting of ranked candidates.
    
    The candidate who would be awarded the vote_value of the ballot is the
    preferred_active_candidate, the most preferred candidate that has not been
    eliminated.
    """

    def __init__(self, vote_value=1.0, candidates=None, starting_rank=0):
        # Float: Value of the ballot's vote
        self.vote_value = vote_value

        # [Candidate]: List mapping ranks to candidates
        self._candidates = candidates if candidates != None else list()

        # Int: Rank mapping to the most preferred active candidate
        self._preferred_active_rank = starting_rank

    def candidate_for_rank(self, rank):
        """
        Returns the candidate on the ballot at that rank.

        Returns: a Candidate representing candidate at that rank, or None
        """
        if (0 <= rank < len(self._candidates)):
            return self._candidates[rank]
        else:
            return None

    def preferred_active_candidate(self):
        """
        Returns the most preferred candidate that has not been eliminated.
        
        Returns: a Candidate representing the preferred active candidate, or None
        """
        return self.candidate_for_rank(self._preferred_active_rank)
    
    def eliminate_preferred_candidate(self):
        """
        Increments the rank mapping to the most preferred candidate.
        """
        current_preferred_active_candidate = self.preferred_active_candidate()
        if current_preferred_active_candidate == None:
            print('Ballot Error: This ballot has no active candidates.')
        else:
            self._preferred_active_rank += 1
    
    def set_candidates(self, candidates):
        """
        Sets the ballot rankings to the ordered list of candidates.
        Resets the preferred active rank.
        
        Parameters:
            - candidates: a list containing strings representing candidates
        """
        self._candidates = candidates
        self._preferred_active_rank = 0
    
    def __eq(self, other):
        if isinstance(other, Ballot):
            return (self.vote_value == other.vote_value
                and self._preferred_active_rank == other._preferred_active_rank
                and self._candidates == other._candidates)

    def __copy__(self):
        ballot_copy = Ballot()
        ballot_copy.vote_value = self.vote_value
        ballot_copy._preferred_active_rank = self._preferred_active_rank
        ballot_copy._candidates = copy.deepcopy(self._candidates)
        return ballot_copy
    
    def __repr__(self):
        return 'Ballot(vote_value={!r}, candidates={!r}, starting_rank={!r})'.format(self.vote_value, self._candidates, self._preferred_active_rank)

    def __str__(self):
        ballot_string = 'Ballot (worth {:.3f}) with remaining candidates:'.format(self.vote_value)
        for rank in range(self._preferred_active_rank, len(self._candidates)):
            ballot_string += ' {}'.format(self.candidate_for_rank(rank))
            if rank < len(self._candidates) - 1:
                ballot_string += ','

        return ballot_string


class VoteTracker:
    """
    The VoteTracker class tracks votes for candidates.
    """

    def __init__(self, votes_for_candidate=None, votes_cast=0.0):
        # Float: Total value of votes cast
        self.votes_cast = votes_cast

        # {Candidate: Float}: Maps Candidates to their votes
        self._votes_for_candidate = votes_for_candidate if votes_for_candidate != None else dict()

    def cast_vote_for_candidate(self, candidate, vote_value=1.0):
        """
        Casts the vote, updating the stored vote totals for the
        candidate.
        
        Parameters:
            - candidate: the Candidate to receive the vote
            - vote_value: the value of the vote
        """
        
        if candidate == None:
            print('VoteTracker Error: Cannot cast vote for candidate None')
            return

        if vote_value <= 0.0:
            print('VoteTracker Error: Cannot cast non-positive vote')
            return

        # Add the vote_value to the total votes_cast
        self.votes_cast += vote_value

        # Add the candidate to _votes_for_candidate if missing
        if candidate not in self._votes_for_candidate:
            self._votes_for_candidate[candidate] = 0

        # Add vote_value to votes_for_candidate
        self._votes_for_candidate[candidate] += vote_value
        
    def votes_for_candidate(self, candidate):
        """
        Returns the candidate's vote total.
        
        Parameters:
            - candidate: the Candidate for the votes
        Returns: a float representing the vote total
        """
        return self._votes_for_candidate.get(candidate, 0)

    def candidates_reaching_threshold(self, candidates, threshold):
        """
        Returns the Candidate(s) with vote count >= threshold.
        
        Parameters:
            - candidates: set of Candidates to check for
            - threshold: float representing the minimum votes to reach
        Returns: a set of Candidates
        """
        candidates_reaching_threshold = set()
        
        # Cycle through candidates and find those meeting the vote threshold
        for candidate in candidates:
            if self.votes_for_candidate(candidate) >= threshold:
                candidates_reaching_threshold.add(candidate)
                
        return candidates_reaching_threshold

    def candidates_with_fewest_votes(self, candidates):
        """
        Returns the Candidate(s) with the fewest votes.
        
        Parameters:
            - candidates: set of Candidates to check for
        Returns: a set of Candidates
        """ 
        candidates_with_fewest_votes = set()
        fewest_votes = -1
        
        # Cycle through candidates and find those with the fewest votes
        for candidate in candidates:
            is_fewest_votes_unset = (fewest_votes == -1)
            candidate_votes = self.votes_for_candidate(candidate)
            if candidate_votes <= fewest_votes or is_fewest_votes_unset:
                if candidate_votes < fewest_votes or is_fewest_votes_unset:
                    fewest_votes = candidate_votes
                    candidates_with_fewest_votes.clear()
                candidates_with_fewest_votes.add(candidate)
        
        return candidates_with_fewest_votes

    def __repr__(self):
        return 'VoteTracker(votes_for_candidate={!r}, votes_cast={!r})'.format(self._votes_for_candidate, self.votes_cast)

    def __str__(self):
        vote_string = ''
        for candidate in sorted(self._votes_for_candidate, key=self._votes_for_candidate.get, reverse=True):
            vote_string += '\n%s: %d' % (candidate, self._votes_for_candidate[candidate])
        description = '<VoteTracker %s%s>' % (id(self), vote_string)
        return description


class ElectionRound:
    """
    The ElectionRound class tracks all election data for a given round.
    """

    def __init__(self, threshold=0, candidates_elected=None, candidates_eliminated=None, vote_tracker=None):
        # Float: Vote threshold to be elected
        self.threshold = threshold

        # {Candidate}: Set of Candidates elected in this round
        self.candidates_elected = candidates_elected if candidates_elected != None else set()

        # {Candidate}: Set of Candidates eliminated in this round
        self.candidates_eliminated = candidates_eliminated if candidates_eliminated != None else set()

        # VoteTracker: VoteTracker for the round
        self.vote_tracker = vote_tracker if vote_tracker != None else VoteTracker()

    def __repr__(self):
        return 'ElectionRound(threshold={!r}, candidates_elected={!r}, candidates_eliminated={!r}, vote_tracker={!r})'.format(self.threshold, self.candidates_elected, self.candidates_eliminated, self.vote_tracker)


class ElectionResults:

    def __init__(self, name='', seats=0, ballots=None, random_alphanumeric=None, candidates_elected=None, election_rounds=None):
        # String: Name of the election
        self.name = name

        # Int: Number of vacant seats before the election
        self.seats = seats

        # [Ballot]: List of all ballots
        self.ballots = ballots if ballots != None else list()

        # String: Random alphanumeric used for final tiebreaks
        self.random_alphanumeric = random_alphanumeric

        # {Candidate}: Set of all candidates elected
        self.candidates_elected = candidates_elected if candidates_elected != None else set()

        # [ElectionRound]: Ordered list of ElectionRounds
        self.election_rounds = election_rounds if election_rounds != None else list()

    def __repr__(self):
        return 'ElectionResults(name={!r}, seats={!r}, ballots={!r}, random_alphanumeric={!r}, candidates_elected={!r}, election_rounds={!r})'.format(self.name, self.seats, self.ballots, self.random_alphanumeric, self.candidates_elected, self.election_rounds)


class Election:
    """
    The Election class is the public top-level class for controlling computing
    the results of an election. The number of seats and the set of all ballots
    is used to compute and return the winners of the election.
    """
    
    def __init__(self, name="", seats=1, random_alphanumeric=None, ballots=list(), can_eliminate_no_confidence=True):
        # String: Name of the election
        self.name = name
        
        # Int: Number of vacant seats
        self.seats = seats
        
        # String: Randomly-sorted alphanumeric for final tiebreaks
        self.random_alphanumeric = random_alphanumeric

        # [Ballot]: List of all ballots
        self.ballots = ballots

        # Bool: Flag for allowing the elimination of No Confidence in election
        self.can_eliminate_no_confidence = can_eliminate_no_confidence
            
    def droop_quota(self, votes, seats_vacant):
        """
        Calculates the Droop Quota, which is the minimum number of votes a
        candidate must receive in order to be elected outright.
        
        Parameters:
            - votes: double representing the value of votes cast
            - seats_vacant: int representing the number of open seats to fill
        Returns: An int representing the vote quota
        """
        return (float(votes) / (float(seats_vacant) + 1.0)) + 1.0
    
    def compute_results(self):
        """
        Run the Election using single transferable vote.
        
        Returns: An ElectionResults object containing the election results
        """

        election_rounds = list()
        current_round = 0

        ballots_active = set(copy.copy(self.ballots))
        ballots_exhausted = set()

        candidates_elected = set()
        candidates_eliminated = set()

        ##########
        # Generate random alphanumeric (if none provided)
        ##########
        tiebreak_alphanumeric = self.random_alphanumeric
        if tiebreak_alphanumeric == None:
            alphanumeric = string.printable
            tiebreak_alphanumeric = ''.join(random.sample(alphanumeric,
                                                          len(alphanumeric)))
        ##########
        # STV Algorithm
        ##########
        while len(candidates_elected) < self.seats:
            current_round += 1
            vote_tracker = VoteTracker()
            ballots_for_candidate = dict()

            election_round = ElectionRound(vote_tracker=vote_tracker)
            election_rounds.append(election_round)

            ##########
            # Count and assign votes from ballots
            ##########
            for ballot in ballots_active:
                # Determine preferred active candidate
                while True:
                    # If no preferred candidate, ballot is exhausted, break
                    # If candidate has not been elected or eliminated, break
                    candidate = ballot.preferred_active_candidate()
                    if (candidate == None or
                        candidate not in candidates_elected and
                        candidate not in candidates_eliminated):
                        break
                    
                    # Otherwise, remove the candidate from the ballot
                    ballot.eliminate_preferred_candidate()

                # If ballot has no active candidates, it is exhausted
                candidate = ballot.preferred_active_candidate()
                if candidate == None:
                    ballots_exhausted.add(ballot)

                # If ballot has no value, it is exhausted
                elif ballot.vote_value <= 0.0:
                    ballots_exhausted.add(ballot)

                # Otherwise, record the ballot and cast its vote
                else:
                    vote_tracker.cast_vote_for_candidate(candidate, vote_value=ballot.vote_value)

                    if candidate not in ballots_for_candidate:
                        ballots_for_candidate[candidate] = set()

                    ballots_for_candidate[candidate].add(ballot)            

            # Remove exhausted ballots
            ballots_active = ballots_active.difference(ballots_exhausted)
            # End election if no candidates remain
            if len(ballots_for_candidate) == 0:
                break

            # If remaining candidates less than or equal to remaining seats
            # elect candidates whose votes exceed that of No Confidence
            seats_vacant = self.seats - len(candidates_elected)
            if len(ballots_for_candidate) <= seats_vacant:
                # Determine the number of votes for No Confidence
                no_confidence_threshold = 0
                for candidate in ballots_for_candidate:
                    if isinstance(candidate, NoConfidence):
                        no_confidence_threshold = vote_tracker.votes_for_candidate(candidate)

                # Elect all candidates with more votes than No Confidence and end election
                candidates_to_elect = vote_tracker.candidates_reaching_threshold(ballots_for_candidate.keys(), no_confidence_threshold)
                candidates_elected.update(candidates_to_elect)
                election_round.candidates_elected = candidates_to_elect
                break

            ##########
            # Calculate threshold
            ##########
            # Threshold changes per round based on votes cast and seats vacant
            threshold = self.droop_quota(vote_tracker.votes_cast, seats_vacant)
            election_round.threshold = threshold

            ##########
            # If winners, transfer surplus, move to next round
            ##########
            candidates_to_elect = vote_tracker.candidates_reaching_threshold(ballots_for_candidate.keys(), threshold)
            candidates_elected.update(candidates_to_elect)
            election_round.candidates_elected = candidates_to_elect

            if len(candidates_to_elect) > 0:
                no_confidence_elected = False
                for candidate in candidates_to_elect:
                    # Calculate vote surplus
                    votes = vote_tracker.votes_for_candidate(candidate)
                    surplus = votes - threshold

                    # Assign fractional value to ballots
                    vote_multiplier = surplus / votes
                    for ballot in ballots_for_candidate[candidate]:
                        ballot.vote_value *= vote_multiplier

                    # Check if elected candidate is No Confidence
                    if isinstance(candidate, NoConfidence):
                        no_confidence_elected = True

                # If No Confidence was elected, end the election
                if no_confidence_elected:
                    break

                # Move on to the next round after transferring surplus
                continue

            ##########
            # Eliminate loser, transfer votes
            ##########
            # Find the candidate(s) (excluding No Confidence) with the fewest votes in the current round
            candidates_to_eliminate = set()
            for candidate in ballots_for_candidate.keys():
                if self.can_eliminate_no_confidence or not isinstance(candidate, NoConfidence):
                    candidates_to_eliminate.add(candidate)

            candidates_to_eliminate = vote_tracker.candidates_with_fewest_votes(candidates_to_eliminate)
            assert len(candidates_to_eliminate) >= 1

            # If multiple candidates have the fewest votes in a round, choose the candidate with the fewest votes in the previous round
            # Repeat if multiple candidates remain tied with the fewest votes
            previous_round = current_round - 1
            while(len(candidates_to_eliminate) > 1 and previous_round >= 0):
                candidates_to_eliminate = election_rounds[previous_round].vote_tracker.candidates_with_fewest_votes(candidates_to_eliminate)
                previous_round -= 1

            # If there is still a tie for elimination, choose the candidate with the fewest votes in ballots' next rank
            # Repeat is multiple candidates remain tied with the fewest votes
            if len(candidates_to_eliminate) > 1:
                ballots_active_copy = copy.deepcopy(ballots_active)
                ballots_exhausted_copy = copy.deepcopy(ballots_exhausted)
                while(len(candidates_to_eliminate) > 1 and len(ballots_active_copy) > 1):
                    forward_vote_tracker = VoteTracker()
                    for ballot in ballots_active_copy:
                        # Determine preferred active candidate
                        if self.can_eliminate_no_confidence or not isinstance(ballot.preferred_active_candidate(), NoConfidence):
                            ballot.eliminate_preferred_candidate()

                        while True:
                            # If no preferred candidate, ballot is exhausted, break
                            # If candidate has not been elected or eliminated, break
                            candidate = ballot.preferred_active_candidate()
                            if (candidate == None or
                                candidate not in candidates_elected and
                                candidate not in candidates_eliminated):
                                break
                            
                            # Otherwise, remove the candidate from the ballot
                            ballot.eliminate_preferred_candidate()

                        candidate = ballot.preferred_active_candidate()
                        # If ballot is exhausted, add it to exhausted ballots
                        if candidate == None:
                            ballots_exhausted_copy.add(ballot)
                        # Remove No Confidence ballots if not eligible to be eliminated
                        elif not self.can_eliminate_no_confidence and isinstance(candidate, NoConfidence):
                            ballots_exhausted_copy.add(ballot)

                        # Otherwise, record the ballot and cast its vote
                        else:
                            forward_vote_tracker.cast_vote_for_candidate(candidate, vote_value=ballot.vote_value)

                    candidates_to_eliminate = forward_vote_tracker.candidates_with_fewest_votes(candidates_to_eliminate)
                    # Remove exhausted ballots
                    ballots_active_copy = ballots_active_copy.difference(ballots_exhausted_copy)
            
            candidate_to_eliminate = None
            # If only one candidate remains, choose the only candidate from the set
            if len(candidates_to_eliminate) == 1:
                (candidate_to_eliminate,) = candidates_to_eliminate
            else:
                # Sort the candidates by uid according to the random alphanumeric
                candidates_random_sort = sorted(candidates_to_eliminate, key=lambda candidate: [tiebreak_alphanumeric.index(c) for c in candidate.uid])
                # Eliminate the first candidate in this random sort that is not No Confidence
                for candidate in candidates_random_sort:
                    if not isinstance(candidate, NoConfidence):
                        candidate_to_eliminate = candidate
                        break

            # Eliminate candidate_to_eliminate and transfer surplus
            candidates_eliminated.add(candidate_to_eliminate)
            election_round.candidates_eliminated = [candidate_to_eliminate]
            
        ##########
        # Election is over; return results
        ##########
        results = ElectionResults(name=self.name,
                                   seats=self.seats,
                                   ballots=self.ballots,
                                   random_alphanumeric=tiebreak_alphanumeric)
        results.candidates_elected = candidates_elected
        results.rounds = election_rounds

        return results
