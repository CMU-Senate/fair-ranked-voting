# election.py: Computes election results using single transferable vote.
# Copyright (C) 2017 Carnegie Mellon University Undergraduate Student Senate.
# Created by Devin Gund.
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
import random
import string


class Candidate:
    """Candidate with a name and unique identifier.

    Attributes:
        uid: String representing the unique identifier of the Candidate. Used
            for equality, hashing, and ordering in a random tiebreak.
        name: String representing the name of the Candidate.
    """

    def __init__(self, uid, name=None):
        """Initializes Candidate with name and uid.

        Args:
            uid: String representing the unique identifier of the Candidate.
                Used for equality, hashing, and ordering in a random tiebreak.
            name: String representing the name of the Candidate.
        """
        self.uid = uid
        self.name = name

    def __eq__(self, other):
        """Checks equality between two Candidates using uids.

        Args:
            other: Candidate to check equality with.

        Returns:
            Boolean indicating if the Candidates are equal or not.
        """
        if isinstance(other, Candidate):
            return self.uid == other.uid

    def __hash__(self):
        """Returns the hash value of the Candidate.

        Returns:
            Integer hash value of the Candidate.
        """
        return hash(self.uid)

    def __repr__(self):
        """Returns a printable system representation of the Candidate.

        Returns:
            String containing the printable representation of the Candidate.
        """
        return 'Candidate({!r}, name={!r})'.format(self.uid, self.name)

    def __str__(self):
        """Returns a printable user representation of the Candidate.

        Returns:
            String containing the printable representation of the Candidate.
        """
        return '{} ({})'.format(self.uid, self.name
                                if self.name is not None else self.uid)


class NoConfidence(Candidate):
    """No Confidence ballot option, which is treated like a Candidate.

    Attributes:
        name: String representing the name of NoConfidence.
        uid: String representing the unique identifier of NoConfidence.
    """

    def __init__(self):
        """Initializes NoConfidence."""
        self.uid = 'NC'
        self.name = 'No Confidence'

    def __repr__(self):
        """Returns a printable system representation of NoConfidence.

        Returns:
            String containing the printable representation of NoConfidence.
        """
        return 'NoConfidence()'


class Ballot:
    """Ballot consisting of ranked candidates and a vote value

    The vote value of the ballot is awarded to the most preferred candidate that
    has not been eliminated.

    Attributes:
        candidates: List of Candidates ordered by preferred rank.
        vote_value: Value of the Ballot's vote. Defaults to 1.0.
        _preferred_active_rank: Integer rank of the preferred active candidate.
    """

    def __init__(self, candidates=None, starting_rank=0, vote_value=1.0):
        """Initializes Ballot with vote value, candidates, and starting rank.

        Args:
            candidates: List of Candidates ordered by preferred rank. Defaults
                to an empty list.
            vote_value: Value of the Ballot's vote. Defaults to 1.0.
            starting_rank: Integer rank of the initial preferred candidate.
                Defaults to 0.
        """
        self.candidates = candidates if candidates is not None else list()
        self.vote_value = vote_value
        self._preferred_active_rank = starting_rank

    def __eq__(self, other):
        """Checks equality between two Ballots.

        Args:
            other: Ballot to check equality with.

        Returns:
            Boolean indicating if the Ballots are equal or not.
        """
        if isinstance(other, Ballot):
            return (self.candidates == other.candidates and
                    self.vote_value == other.vote_value and
                    self._preferred_active_rank == other._preferred_active_rank)

    def __repr__(self):
        """Returns a printable system representation of the Ballot.

        Returns:
            String containing the printable representation of the Ballot.
        """
        return 'Ballot(candidates={!r}, vote_value={!r}, starting_rank={!r})'.format(
               self.candidates, self.vote_value, self._preferred_active_rank)

    def description(self):
        """Returns a printable long-form user representation of the Ballot.

        Returns:
            String containing the printable representation of the Ballot.
        """
        description = 'Ballot worth {:.3f}:'.format(self.vote_value)
        for rank in range(len(self.candidates)):
            rank_symbol = ' '
            if rank < self._preferred_active_rank:
                rank_symbol = 'X'
            if rank == self._preferred_active_rank:
                rank_symbol = '>'
            description += '\n{} {}'.format(rank_symbol, self.candidate_for_rank(rank))
        return description

    def candidate_for_rank(self, rank):
        """Returns the Candidate on the Ballot for the given rank.

        Args:
            rank: Integer rank of the Candidate.

        Returns:
            Candidate on the Ballot at that rank, or None.
        """
        if (0 <= rank < len(self.candidates)):
            return self.candidates[rank]
        else:
            return None

    def preferred_active_candidate(self):
        """Returns the most preferred Candidate that has not been eliminated.

        Returns:
            Candidate on the Ballot at the preferred active rank, or None.
        """
        return self.candidate_for_rank(self._preferred_active_rank)

    def eliminate_preferred_candidate(self):
        """Eliminates the current preferred active Candidate."""
        current_preferred_active_candidate = self.preferred_active_candidate()
        if current_preferred_active_candidate is None:
            print('Ballot Error: This ballot has no active candidates.')
        else:
            self._preferred_active_rank += 1

    def set_candidates(self, candidates):
        """Resets the ballot rankings to the ordered list of Candidates.

        Args:
            candidates: List of Candidates ordered by preferred rank.
        """
        self.candidates = candidates
        self._preferred_active_rank = 0


class VoteTracker:
    """Vote Tracker for assigning votes to Candidates.

    Attributes:
        votes_cast: Float value of the total votes cast.
        _votes_for_candidate: Dict mapping Candidates to float values of votes.
    """

    def __init__(self, votes_cast=0.0, votes_for_candidate=None):
        """Initializes VoteTracker with votes cast and votes for candidates.

        Args:
            votes_cast: Float value of the total votes cast.
            votes_for_candidate: Dict mapping Candidates to float values of
                votes.
        """
        self.votes_cast = votes_cast
        self._votes_for_candidate = (votes_for_candidate
                                     if votes_for_candidate is not None else dict())

    def __eq__(self, other):
        """Checks equality between two VoteTrackers.

        Args:
            other: VoteTracker to check equality with.

        Returns:
            Boolean indicating if the VoteTrackers are equal or not.
        """
        if isinstance(other, VoteTracker):
            return (self.votes_cast == other.votes_cast and
                    self._votes_for_candidate == other._votes_for_candidate)

    def __repr__(self):
        """Returns a printable system representation of the VoteTracker.

        Returns:
            String containing the printable representation of the VoteTracker.
        """
        return 'VoteTracker(votes_for_candidate={!r}, votes_cast={!r})'.format(
                self._votes_for_candidate, self.votes_cast)

    def decription(self):
        """Returns a printable long-form user representation of the VoteTracker.

        Returns:
            String containing the printable representation of the VoteTracker.
        """
        description = 'VoteTracker for {} votes:'.format(self.votes_cast)
        for candidate in sorted(self._votes_for_candidate, key=self._votes_for_candidate.get, reverse=True):
            description += '\n{}: {}'.format(candidate, self._votes_for_candidate[candidate])
        return description

    def cast_vote_for_candidate(self, candidate, vote_value):
        """Casts the vote for the Candidate, updating the stored vote totals.

        Args:
            candidate: Candidate to receive the vote.
            vote_value: Float value of the vote.
        """

        if candidate is None:
            print('VoteTracker Error: Cannot cast vote for candidate None')
            return

        if vote_value < 0.0:
            print('VoteTracker Error: Cannot cast negative vote')
            return

        # Add the vote_value to the total votes_cast
        self.votes_cast += vote_value

        # Add the candidate to _votes_for_candidate if missing
        if candidate not in self._votes_for_candidate:
            self._votes_for_candidate[candidate] = 0.0

        # Add vote_value to _votes_for_candidate
        self._votes_for_candidate[candidate] += vote_value

    def votes_for_candidate(self, candidate):
        """Returns the value of the votes for the given Candidate.

        Args:
            Candidate: Candidate to obtain the vote value.

        Returns:
            Float value of the votes for the Candidate.
        """
        return self._votes_for_candidate.get(candidate, 0.0)

    def candidates(self):
        """Returns the Candidate(s) being tracked.

        Returns:
            Set of candidates being tracked.
        """
        return set(self._votes_for_candidate.keys())

    def candidates_reaching_threshold(self, candidates, threshold):
        """Returns the Candidate(s) with vote values meeting the threshold.

        Args:
            candidates: Set of Candidates to check.
            threshold: Float value of the vote threshold.

        Returns:
            Set of Candidates meeting the vote threshold.
        """
        candidates_reaching_threshold = set()

        # Cycle through candidates and find those meeting the vote threshold
        for candidate in candidates:
            if self.votes_for_candidate(candidate) >= threshold:
                candidates_reaching_threshold.add(candidate)

        return candidates_reaching_threshold

    def candidates_with_fewest_votes(self, candidates):
        """Returns the Candidate(s) with the fewest votes.

        Args:
            candidates: Set of Candidates to check.

        Returns:
            Set of Candidates with the fewest votes.
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


class ElectionRound:
    """Election data for a round of voting.

    Attributes:
        candidates_elected: Set of Candidates elected in this round.
        candidates_eliminated: Set of Candidates eliminated in this round.
        threshold: Float value of the vote threshold to be elected.
        random_tiebreak_occured: Boolean indicating if a random tiebreak
                occurred or not in this round.
        vote_tracker: VoteTracker for counting votes in this round.
    """

    def __init__(self, candidates_elected=None, candidates_eliminated=None,
                 threshold=0, random_tiebreak_occurred=False,
                 vote_tracker=None):
        """Initializes ElectionRound with threshold, Candidate, and vote data.

        Args:
            candidates_elected: Set of Candidates elected in this round.
            candidates_eliminated: Set of Candidates eliminated in this round.
            threshold: Float value of the vote threshold to be elected.
            random_tiebreak_occured: Boolean indicating if a random tiebreak
                occurred or not in this round.
            vote_tracker: VoteTracker for counting votes in this round.
        """
        self.threshold = threshold
        self.candidates_elected = (candidates_elected if candidates_elected is not None else set())
        self.candidates_eliminated = (candidates_eliminated if candidates_eliminated is not None else set())
        self.random_tiebreak_occurred = random_tiebreak_occurred
        self.vote_tracker = (vote_tracker if vote_tracker is not None else VoteTracker())

    def __repr__(self):
        """Returns a printable system representation of the ElectionRound.

        Returns:
            String containing the printable representation of the ElectionRound.
        """
        return 'ElectionRound(threshold={!r}, candidates_elected={!r}, candidates_eliminated={!r}, random_tiebreak_occurred={}, vote_tracker={!r})'.format(
            self.threshold, self.candidates_elected, self.candidates_eliminated, self.random_tiebreak_occurred, self.vote_tracker)

    def description(self):
        """Returns a printable long-form user representation of the
            ElectionRound.

        Returns:
            String containing the printable representation of the ElectionRound.
        """
        description = 'ElectionRound with threshold {}:\n'.format(self.threshold)
        description += self.vote_tracker.decription()
        if len(self.candidates_elected) > 0:
            summary_elected = '\nCandidates elected in this round:'
            for candidate in self.candidates_elected:
                summary_elected += ' {},'.format(candidate)
            description += summary_elected[:-1]
        if len(self.candidates_eliminated) > 0:
            summary_eliminated = '\nCandidates eliminated in this round:'
            for candidate in self.candidates_eliminated:
                summary_eliminated += ' {},'.format(candidate)
            description += summary_eliminated[:-1]
        if self.random_tiebreak_occurred:
            description += '\nA random tiebreak occurred in this round'
        return description


class ElectionResults:
    """Election results and data for all rounds.

    Attributes:
        ballots: List of all Ballots.
        candidates_elected: Set of Candidates elected.
        election_rounds: List of ElectionRounds.
        name: String representing the name of the election.
        random_alphanumeric: String containing the random alphanumeric used for
            final tiebreaks.
        seats: Number of vacant seats before the election.
    """

    def __init__(self, ballots, candidates_elected,
                 election_rounds, random_alphanumeric,
                 seats, name=''):
        """Initializes ElectionResults with election results and data.

        Args:
            ballots: List of all Ballots.
            candidates_elected: Set of Candidates elected.
            election_rounds: List of ElectionRounds.
            random_alphanumeric: String containing the random alphanumeric used
                for final tiebreaks.
            seats: Number of vacant seats before the election.
            name: String representing the name of the election.
        """
        self.ballots = ballots
        self.candidates_elected = candidates_elected
        self.election_rounds = election_rounds
        self.name = name
        self.random_alphanumeric = random_alphanumeric
        self.seats = seats

    def __repr__(self):
        """Returns a printable system representation of the ElectionResults.

        Returns:
            String containing the printable representation of the
            ElectionResults.
        """
        return 'ElectionResults(name={!r}, seats={!r}, ballots={!r}, random_alphanumeric={!r}, candidates_elected={!r}, election_rounds={!r})'.format(
                    self.name, self.seats, self.ballots, self.random_alphanumeric, self.candidates_elected, self.election_rounds)

    def description(self):
        """Returns a printable long-form user representation of the
            ElectionResults.

        Returns:
            String containing the printable representation of the
                ElectionResults.
        """
        description = 'Results for election {}:\n'.format(self.name)
        if len(self.candidates_elected) > 0:
            summary_elected = 'Elected:'
            for candidate in self.candidates_elected:
                summary_elected += ' {},'.format(candidate)
            description += summary_elected[:-1]

        for round_index in range(len(self.election_rounds)):
            round_description = self.election_rounds[round_index].description()
            summary_round = '\nRound {}:\n{}'.format(round_index, round_description)
            description += summary_round
        return description


class Election:
    """Election configuration and computation.

    Attributes:
        ballots: List of all Ballots.
        seats: Number of vacant seats before the election.
        can_eliminate_no_confidence: Boolean indicating if No Confidence may be
            eliminated in the election.
        can_random_tiebreak: Boolean indicating if random elimination may be
            used for final tiebreaks. Otherwise, the election is halted.
        name: String representing the name of the election. Defaults to an empty
            string.
        random_alphanumeric: String containing the random alphanumeric used for
            final tiebreaks.
    """

    def __init__(self, ballots, seats, can_eliminate_no_confidence=True,
                 can_random_tiebreak=True, name='', random_alphanumeric=None):
        """Initializes Election with ballots, seats, and configuration data.

        Args:
            ballots: List of all Ballots.
            seats: Number of vacant seats before the election.
            can_eliminate_no_confidence: Boolean indicating if No Confidence may
                be eliminated in the election.
            can_random_tiebreak: Boolean indicating if random elimination may be
                used for final tiebreaks. Otherwise, the election is halted.
            name: String representing the name of the election.
            random_alphanumeric: String containing the rcandom alphanumeric used
                for final tiebreaks.
        """
        self.ballots = ballots
        self.can_eliminate_no_confidence = can_eliminate_no_confidence
        self.can_random_tiebreak = can_random_tiebreak
        self.seats = seats
        self.name = name
        self.random_alphanumeric = random_alphanumeric

    def droop_quota(self, seats, votes):
        """Calculates the Droop Quota as the vote threshold.

        This threshold is the minimum number of votes a candidate must receive
        in order to be elected outright.

        Args:
            seats_vacant: Integer value of the seats vacant.
            votes: Float value of the value of votes cast.
        Returns: An int representing the vote quota
        """
        return (float(votes) / (float(seats) + 1.0)) + 1.0

    def compute_results(self):
        """Run the election using the single transferable vote algorithm.

        Returns:
            ElectionResults containing the election results and data.
        """

        election_rounds = list()
        current_round = 0

        ballots_active = copy.deepcopy(self.ballots)
        ballots_exhausted = list()

        candidates_elected = set()
        candidates_eliminated = set()

        ##########
        # Generate random alphanumeric (if none provided)
        ##########
        tiebreak_alphanumeric = self.random_alphanumeric
        if tiebreak_alphanumeric is None:
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
            ballots_to_exhaust = list()
            for ballot in ballots_active:
                # Determine preferred active candidate.
                while True:
                    # If no preferred candidate, ballot is exhausted, break.
                    # If candidate has not been elected or eliminated, break.
                    candidate = ballot.preferred_active_candidate()
                    if (candidate is None or
                            candidate not in candidates_elected and
                            candidate not in candidates_eliminated):
                        break

                    # Otherwise, remove the candidate from the ballot.
                    ballot.eliminate_preferred_candidate()

                # Ensure that vote tracker contains every active candidate
                for candidate in ballot.candidates:
                    if (candidate not in candidates_elected and
                            candidate not in candidates_eliminated):
                        vote_tracker.cast_vote_for_candidate(candidate, 0.0)

                # If ballot has no active candidates, it is exhausted.
                candidate = ballot.preferred_active_candidate()
                if candidate is None:
                    ballots_to_exhaust.append(ballot)

                # If ballot has no value, it is exhausted.
                elif ballot.vote_value <= 0.0:
                    ballots_to_exhaust.append(ballot)

                # Otherwise, record the ballot and cast its vote.
                else:
                    # Add vote to vote tracker.
                    vote_tracker.cast_vote_for_candidate(candidate,
                                                         ballot.vote_value)

                    # Add ballot to ballot tracker.
                    if candidate not in ballots_for_candidate:
                        ballots_for_candidate[candidate] = []
                    ballots_for_candidate[candidate].append(ballot)

            # Remove exhausted ballots.
            for ballot in ballots_to_exhaust:
                ballots_active.remove(ballot)
            ballots_exhausted.extend(ballots_to_exhaust)

            # End election if no candidates remain.
            if len(vote_tracker.candidates()) == 0:
                break

            # If remaining candidates less than or equal to remaining seats
            # elect candidates whose votes exceed that of No Confidence.
            seats_vacant = self.seats - len(candidates_elected)
            if len(vote_tracker.candidates()) <= seats_vacant:
                # Determine the number of votes for No Confidence.
                nc_vote = 0
                for candidate in vote_tracker.candidates():
                    if isinstance(candidate, NoConfidence):
                        nc_vote = vote_tracker.votes_for_candidate(candidate)
                        break

                # Elect all candidates with more votes than No Confidence and end election.
                candidates_to_elect = vote_tracker.candidates_reaching_threshold(vote_tracker.candidates(), nc_vote)
                candidates_elected.update(candidates_to_elect)
                election_round.candidates_elected = candidates_to_elect
                break

            ##########
            # Calculate threshold
            ##########
            # Threshold changes per round based on votes cast and seats vacant.
            threshold = self.droop_quota(seats_vacant, vote_tracker.votes_cast)
            election_round.threshold = threshold

            ##########
            # If winners, transfer surplus, move to next round.
            ##########
            candidates_to_elect = vote_tracker.candidates_reaching_threshold(vote_tracker.candidates(), threshold)
            candidates_elected.update(candidates_to_elect)
            election_round.candidates_elected = candidates_to_elect

            if len(candidates_to_elect) > 0:
                no_confidence_elected = False
                for candidate in candidates_to_elect:
                    # Calculate vote surplus
                    votes = vote_tracker.votes_for_candidate(candidate)
                    surplus = votes - threshold

                    # Assign fractional value to ballots.
                    vote_multiplier = surplus / votes
                    for ballot in ballots_for_candidate[candidate]:
                        ballot.vote_value *= vote_multiplier

                    # Check if elected candidate is No Confidence.
                    if isinstance(candidate, NoConfidence):
                        no_confidence_elected = True

                # If No Confidence was elected, end the election.
                if no_confidence_elected:
                    break

                # Move on to the next round after transferring surplus.
                continue

            ##########
            # Eliminate loser, transfer votes
            ##########
            # Find the candidate(s) (excluding No Confidence) with the fewest
            # votes in the current round.
            candidates_eligible_to_eliminate = set()
            candidates_to_eliminate = set()
            for candidate in vote_tracker.candidates():
                if self.can_eliminate_no_confidence or not isinstance(candidate, NoConfidence):
                    candidates_eligible_to_eliminate.add(candidate)

            candidates_to_eliminate = vote_tracker.candidates_with_fewest_votes(candidates_eligible_to_eliminate)

            # If multiple candidates have the fewest votes in a round, and their
            # combined vote total is less than that of the next-highest
            # candidate, eliminate all of the tied candidates. Otherwise, a
            # tiebreak is required to select the candidate to eliminate.
            tiebreak_required = False
            if len(candidates_to_eliminate) > 1:
                tied_combined_vote_value = len(candidates_to_eliminate) * vote_tracker.votes_for_candidate(next(iter(candidates_to_eliminate)))
                next_highest_candidates = vote_tracker.candidates_with_fewest_votes(candidates_eligible_to_eliminate.difference(candidates_to_eliminate))
                if len(next_highest_candidates) > 0:
                    next_highest_vote_value = vote_tracker.votes_for_candidate(next(iter(next_highest_candidates)))
                else:
                    next_highest_vote_value = 0
                tiebreak_required = (tied_combined_vote_value >=
                                     next_highest_vote_value)

            # If there is still a tie for elimination, choose the candidate with
            # the fewest votes in the previous round. Repeat if multiple
            # candidates remain tied with the fewest votes.
            if tiebreak_required:
                previous_round = current_round - 1
                while(len(candidates_to_eliminate) > 1 and previous_round >= 0):
                    candidates_to_eliminate = election_rounds[previous_round].vote_tracker.candidates_with_fewest_votes(candidates_to_eliminate)
                    previous_round -= 1

                tiebreak_required = len(candidates_to_eliminate) > 1

            # If there is still a tie for elimination, choose the candidate with
            # the fewest votes in ballots' next rank. Repeat is multiple
            # candidates remain tied with the fewest votes.
            if tiebreak_required:
                ballots_active_tiebreak = copy.deepcopy(ballots_active)
                ballots_exhausted_tiebreak = copy.deepcopy(ballots_exhausted)
                while(len(candidates_to_eliminate) > 1 and len(ballots_active_tiebreak) > 1):
                    forward_vote_tracker = VoteTracker()
                    ballots_to_exhaust_tiebreak = list()
                    for ballot in ballots_active_tiebreak:
                        # Determine preferred active candidate.
                        if (self.can_eliminate_no_confidence or not isinstance(ballot.preferred_active_candidate(), NoConfidence)):
                            ballot.eliminate_preferred_candidate()

                        while True:
                            # Update ballots
                            candidate = ballot.preferred_active_candidate()
                            if (candidate is None or
                                    candidate not in candidates_elected and
                                    candidate not in candidates_eliminated):
                                break

                            # Otherwise, remove the candidate from the ballot.
                            ballot.eliminate_preferred_candidate()

                        # Ensure that vote tracker contains every active candidate
                        for candidate in ballot.candidates:
                            if (candidate not in candidates_elected and
                                    candidate not in candidates_eliminated):
                                forward_vote_tracker.cast_vote_for_candidate(candidate, 0.0)

                        candidate = ballot.preferred_active_candidate()
                        # If ballot is exhausted, add it to exhausted ballots.
                        if candidate is None:
                            ballots_to_exhaust_tiebreak.append(ballot)
                        # Remove No Confidence ballots if not eligible to be
                        # eliminated.
                        elif not self.can_eliminate_no_confidence and isinstance(candidate, NoConfidence):
                            ballots_to_exhaust_tiebreak.append(ballot)

                        # Otherwise, record the ballot and cast its vote.
                        else:
                            forward_vote_tracker.cast_vote_for_candidate(candidate, vote_value=ballot.vote_value)

                    candidates_to_eliminate = forward_vote_tracker.candidates_with_fewest_votes(candidates_to_eliminate)
                    # Remove exhausted ballots
                    for ballot in ballots_to_exhaust_tiebreak:
                        ballots_active_tiebreak.remove(ballot)
                    ballots_exhausted_tiebreak.extend(ballots_to_exhaust)

                tiebreak_required = len(candidates_to_eliminate) > 1

            # If there is still a tie for elimination, choose a random candidate
            # according to the random tiebreak alphanumeric.
            random_tiebreak_occurred = False
            if tiebreak_required:
                random_tiebreak_occurred = True

                # If random tiebreaks are not allowed, end the election.
                if not self.can_random_tiebreak:
                    break

                # Sort the candidates by uid according to the random
                # alphanumeric.
                candidates_random_sort = sorted(candidates_to_eliminate, key=lambda candidate: [tiebreak_alphanumeric.index(c) for c in candidate.uid])
                # Eliminate the first candidate in this random sort that is not
                # No Confidence.
                for candidate in candidates_random_sort:
                    if not isinstance(candidate, NoConfidence):
                        candidates_to_eliminate = [candidate]
                        break

            # Eliminate candidates_to_eliminate.
            candidates_eliminated.update(candidates_to_eliminate)
            election_round.candidates_eliminated = candidates_to_eliminate
            election_round.random_tiebreak_occurred = random_tiebreak_occurred

        ##########
        # Election is over; return results.
        ##########
        results = ElectionResults(self.ballots, candidates_elected,
                                  election_rounds, tiebreak_alphanumeric,
                                  self.seats, name=self.name)
        return results
