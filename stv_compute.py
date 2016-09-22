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

import copy
import math
import random

class Ballot:
    """
    The Ballot class represents a ballot consisting of ranked candidates. Each
    candidate on the ballot is mapped to by a ranking. The rankings must be
    continuous with no duplicates.
    
    The candidate who would be awarded the vote_value of the ballot is the
    preferred_active_candidate, the most preferred candidate that has not been
    eliminated. Candidates are represented by strings of their names.
    """
    
    # Static constant that always refers to the No Confidence option on the ballot
    NO_CONFIDENCE = "No Confidence"

    def __init__(self, vote_value=1.0):
        # The value of the ballot's vote
        self.vote_value = vote_value
        
        # The internal rank mapping to the most preferred active candidate
        self._preferred_active_rank = 1
        
        # The internal dictionary mapping ranks to candidates
        self._ranks = dict()

    def preferred_active_candidate(self):
        """
        Returns the most preferred candidate that has not been eliminated.
        
        Returns: a string representing the preferred active candidate, or None
        """
        return self._ranks.get(self._preferred_active_rank)
        
    def eliminate_preferred_candidate(self):
        """
        Increments the rank mapping to the most preferred candidate.
        """
        current_preferred_active_candidate = self.preferred_active_candidate()
        if current_preferred_active_candidate == None:
            print("Ballot Error: This ballot has no active candidates.")
        elif current_preferred_active_candidate == Ballot.NO_CONFIDENCE:
            print("Ballot Error: Cannot eliminate No Confidence from a ballot.")
        else:
            self._preferred_active_rank += 1
        
    def set_candidate_with_rank(self, candidate, rank):
        """
        Maps a rank to a candidate on the ballot.
        
        Parameters:
            - candidate: a string representing the candidate
            - rank: an int representing the candidate's rank
        """
        if self._ranks.get(rank) != None:
            print("Ballot Error: That rank has already been assigned to a candidate.")
            assert False
        self._ranks[rank] = candidate
       
    def __copy__(self):
        """
        Copies a ballot, including its current active rank.
        
        Returns: a Ballot
        """
        ballot_copy = Ballot()
        ballot_copy.vote_value = self.vote_value
        ballot_copy._preferred_active_rank = self._preferred_active_rank
        ballot_copy._ranks = copy.copy(self._ranks)
        return ballot_copy
     
    def __repr__(self):
        """
        Prints the ballot, depicting the candidates and ranks.
        """
        ballot_string = "Ballot %d (worth %.2f votes):" % (id(self), self.vote_value)
        rank = 1
        while True:
            candidate_at_rank = self._ranks.get(rank)
            if candidate_at_rank == None:
                break
            
            rank_string = "\n(%d) " % (rank)
            
            if rank < self._preferred_active_rank:
                rank_string += "[Eliminated] "
                
            rank_string += candidate_at_rank
            
            ballot_string += rank_string
            rank += 1
        return ballot_string


class Election_Counter:
    """
    The Election_Counter class is an internal class used by the Election class
    for tracking votes, ballot distribution, and winning/losing candidates.
    """
    
    def __init__(self, verbose=False):
        # The current round of voting
        # Used for breaking tied by looking at votes from previous rounds
        self.voting_round = 0
        
        # If verbose is True, prints details of vote counting progress
        self.verbose = verbose
        
        # Sets containing the candidates that have won or lost
        self.winning_candidates = set()
        self.losing_candidates = set()
        
        # Array containing a dict for each round
        # Each dict maps candidates to their vote totals for that round
        self._votes_for_candidate_per_round = list()
        self._votes_for_candidate_per_round.append(dict())
        
        # Maps active candidates to their currently-assigned ballots
        self._ballots_for_candidate = dict()
    
    def verbose_print(self, *args, **kwargs):
        """
        Print objects only if self.verbose is True.
        """
        if self.verbose:
            print(args, kwargs)
    
    def advance_voting_round(self):
        """
        Increments the voting round, and copies the previous dict of votes for
        each candidate to the new round.
        """
        self.voting_round += 1
        self._votes_for_candidate_per_round.append(copy.copy(self._votes_for_candidate_per_round[self.voting_round - 1]))
        assert len(self._votes_for_candidate_per_round) == self.voting_round + 1
    
    def updated_ballot_for_eliminated_candidates(self, ballot):
        """
        Returns a ballot with an updates preferred_active_candidate such that
        they are the most preferred candidate is not eliminated, or None.
        
        Parameters:
            - ballot: the Ballot to be updated
        Returns: Ballot copy, with preferred_active_candidate updated or None
        """
        updated_ballot = copy.copy(ballot)
        # Move down the list of preferred candidates for a ballot
        while True:
            preferred_candidate = updated_ballot.preferred_active_candidate()
            # If there are no more preferred candidates, stop
            if preferred_candidate == None:
                break
            # If the new preferred candidate has not been eliminated, stop
            elif not self.is_candidate_eliminated(preferred_candidate):
                break
            else:
                updated_ballot.eliminate_preferred_candidate()
        return updated_ballot
        
    def cast_ballot(self, ballot):
        """
        Casts the ballot, updating the stored vote and ballot totals for the
        preferred candidate on that ballot. If there is no preferred candidate,
        the ballot is discarded.
        
        Parameters:
            - ballot: the Ballot to be cast
        """
        
        if ballot == None:
            print("Election_Counter Error: Cannot cast ballot None")
            assert False
            return
        
        # Cast the ballot for the ballots's preferred active candidate
        preferred_candidate = ballot.preferred_active_candidate()
                
        # If there is no preferred active candidate, the ballot is discarded
        if preferred_candidate == None:
            return
        
        assert not self.is_candidate_eliminated(preferred_candidate)
        
        # Add the ballot to self.ballots_for_candidate
        # Add ballot.vote_value to self.votes_for_candidate_per_round for the current round
        if preferred_candidate in self._ballots_for_candidate:
            self._ballots_for_candidate[preferred_candidate].append(ballot)
            self._votes_for_candidate_per_round[self.voting_round][preferred_candidate] += ballot.vote_value
        else:
            self._ballots_for_candidate[preferred_candidate] = [ballot]
            self._votes_for_candidate_per_round[self.voting_round][preferred_candidate] = ballot.vote_value

    def active_candidates(self, voting_round=None):
        """
        Returns a list of all of the active candidates (i.e. candidates with
        assigned ballots) for a round.
        
        Parameters:
            - voting_round (optional): the round of voting to use
                defaults to the current round
        Returns: a list of candidates
        """
        if voting_round is None:
            voting_round = self.voting_round
        return self._votes_for_candidate_per_round[voting_round].keys()

    def is_candidate_eliminated(self, candidate):
        """
        Returns if a candidate has been eliminated from the election.
        
        Parameters:
            - candidate: the candidate to check for
        Returns: True if the candidate has been eliminated, False otherwise
        """
        return candidate in self.winning_candidates or candidate in self.losing_candidates

    def ballots_for_candidate(self, candidate):
        """
        Returns all of the ballots currently assigned to a candidate.
        
        Parameters:
            - candidate: the candidate for the ballots
        Returns: a set of Ballots
        """
        return self._ballots_for_candidate.get(candidate)
        
    def votes_for_candidate(self, candidate, voting_round=None):
        """
        Returns the candidate's vote total for a round.
        
        Parameters:
            - candidate: the candidate for the votes
            - voting_round (optional): the round of voting to use
                defaults to the current round
        Returns: a float representing the vote total
        """
        if voting_round is None:
            voting_round = self.voting_round
        return self._votes_for_candidate_per_round[voting_round].get(candidate)

    def candidates_reaching_quota(self, quota, limit_to_candidates=None, voting_round=None):
        """
        Returns the candidate(s) with vote count >= quota.
        
        Parameters:
            - quota: float representing the minimum quota to reach
            - limit_to_candidates (optional): set of candidates to check for
                defaults to all active candidates for the round
            - voting_round (optional): the round of voting to use
                defaults to the current round
        Returns: a set of candidates
        """
        if voting_round is None:
            voting_round = self.voting_round
        if limit_to_candidates is None:
            limit_to_candidates = self.active_candidates(voting_round)
        
        candidates_reaching_quota = set()
        
        # Cycle through candidates and find those meeting the vote quota
        for candidate in limit_to_candidates:
            candidate_votes = self.votes_for_candidate(candidate, voting_round=voting_round)
            if candidate_votes >= quota:
                candidates_reaching_quota.add(candidate)
                
        return candidates_reaching_quota

    def candidates_with_fewest_votes(self, limit_to_candidates=None, voting_round=None):
        """
        Returns the candidate(s) with the fewest votes.
        
        Parameters:
            - limit_to_candidates (optional): set of candidates to check for
                defaults to all active candidates for the round
            - voting_round (optional): the round of voting to use
                defaults to the current round
        Returns: a set of candidates
        """
        if voting_round is None:
            voting_round = self.voting_round
        if limit_to_candidates is None:
            limit_to_candidates = self.active_candidates(voting_round)
            
        candidates_with_fewest_votes = set()
        fewest_votes = -1
        
        # Cycle through candidates and find those with the fewest votes
        for candidate in limit_to_candidates:
            candidate_votes = self.votes_for_candidate(candidate, voting_round=voting_round)
            is_fewest_votes_unset = fewest_votes == -1
            if candidate_votes <= fewest_votes or is_fewest_votes_unset:
                if candidate_votes < fewest_votes or is_fewest_votes_unset:
                    fewest_votes = candidate_votes
                    candidates_with_fewest_votes.clear()
                candidates_with_fewest_votes.add(candidate)
        
        return candidates_with_fewest_votes
        
    def declare_winner(self, candidate, quota):
        """
        Marks a candidate as winning, removing them from the election and
        redistributing any surplus votes by splitting them amongst their
        ballots' next preferences.
        
        Parameters:
            - candidate: the candidate to declare winner
            - quota: the quota to use for redistributing surplus votes
        """
        self.winning_candidates.add(candidate)
        candidate_ballots = self._ballots_for_candidate.pop(candidate)
        candidate_votes = self._votes_for_candidate_per_round[self.voting_round].pop(candidate)
        
        self.verbose_print("%s is declared a winner, with %.2f votes in this round." % (candidate, candidate_votes))
        
        # If a candidate's votes exceed the quota, redistribute surplus votes
        if candidate_votes > quota and candidate != Ballot.NO_CONFIDENCE:
            surplus = candidate_votes - quota
            surplus_multiplier = (surplus / candidate_votes)
            # The surplus votes are distributed evenly amongst all ballots
            # This results in fractional votes for each ballot's next preference
            for candidate_ballot in candidate_ballots:
                updated_ballot = self.updated_ballot_for_eliminated_candidates(candidate_ballot)
                updated_ballot.vote_value *= surplus_multiplier
                self.cast_ballot(updated_ballot)
                
            self.verbose_print("%s's surplus of %.2f votes will be redistributed amongst their ballots, each worth %.2f votes." % (candidate, surplus, surplus_multiplier))
        
    def declare_loser(self, candidate, random=False):
        """
        Marks a candidate as losing, removing them from the election and
        redistributing all of their votes to their ballots' next preferences.
        
        Parameters:
            - candidate: the candidate to declare loser
            - random (optional): whether the candidate was removed randomly
        """
        self.losing_candidates.add(candidate)
        candidate_ballots = self._ballots_for_candidate.pop(candidate)
        candidate_votes = self._votes_for_candidate_per_round[self.voting_round].pop(candidate)
        
        self.verbose_print((
            "%s has the fewest votes and will be eliminated%s, with %.2f votes in this round." +
            "Their votes will be redistributed amongst their ballots."
        ) % (candidate, ' randomly' if random else '', candidate_votes))
        
        for candidate_ballot in candidate_ballots:
            updated_ballot = self.updated_ballot_for_eliminated_candidates(candidate_ballot)
            self.cast_ballot(updated_ballot)


class Election:
    """
    The Election class is the public top-level class for controlling computing
    the results of an election. The number of seats and the set of all ballots
    is used to compute and return the winners of the election.
    """
    
    def __init__(self, name="", seats=1, is_final_tiebreak_manual=False):
        # The name of the election, for bookkeeping and verbose printing
        self.name = name
        
        # The number of open seats this election should fill
        self.seats = seats
        
        # The set of all ballots cast in the election
        self.ballots = list()
        
        # If candidates are tied for fewest votes for all current and previous rounds:
        # If manual tiebreak, the user will be prompted to eliminate a candidate
        # If not manual tiebreak, a random candidate will be eliminated
        self.is_final_tiebreak_manual = is_final_tiebreak_manual
    
    def droop_quota(self, num_ballots, seats):
        """
        Calculates the Droop Quota, which is the minimum number of votes a
        candidate must receive in order to be elected outright.
        
        Parameters:
            - num_ballots: int representing the number of ballots cast
            - seats: int representing the number of open seats to fill
        Returns: An int representing the vote quota
        """
        return math.floor(num_ballots / (seats + 1)) + 1
    
    def compute_winners(self, verbose=False):
        """
        Compute the winners of the Election using single transferable vote.
        
        Parameters:
            - verbose (optional): if True, prints details of election progress
                defaults to False
        Returns: set containing strings representing the winning candidates
        """
        # Initialize the election counter
        counter = Election_Counter(verbose=verbose)
                    
        # Determine the vote quota to be elected
        quota = self.droop_quota(len(self.ballots), self.seats)
        
        if (verbose):
            print("***** Election: %s *****" % self.name)
            print("There were %d ballots cast to fill %d seat(s)." % (len(self.ballots), self.seats))
            print("A quota of %d votes is required to win outright." % (quota))
        
        # Cast initial ballots
        for ballot in self.ballots:
            counter.cast_ballot(copy.copy(ballot))
                
        while len(counter.winning_candidates) < self.seats:
            counter.advance_voting_round()
            
            if (verbose):
                print("\n*** Voting Round %d ***" % counter.voting_round)
            
            remaining_candidates = counter.active_candidates()
            remaining_seats = self.seats - len(counter.winning_candidates)
            
            # Check for a winner (a candidate whose votes meet the quota)
            winners_for_round = counter.candidates_reaching_quota(quota)
            
            # Declare any winners, redistributing their surplus votes 
            if len(winners_for_round) > 0:
                for winning_candidate in winners_for_round:
                    counter.declare_winner(winning_candidate, quota)
                # If No Confidence wins, end the election
                if Ballot.NO_CONFIDENCE in counter.winning_candidates:
                    if(verbose):
                        print("%s has been declared a winner, so no further rounds will be conducted." % (Ballot.NO_CONFIDENCE))
                    break
                    
            # If the remaining seats must be filled by the remaining candidates, fill them
            # No Confidence cannot be eliminated, but if it has the fewest
            # votes, fill the remaining seats with the rest of the candidates
            elif (len(remaining_candidates) <= remaining_seats or
                 (len(remaining_candidates) <= remaining_seats + 1 and
                  Ballot.NO_CONFIDENCE in remaining_candidates and
                  Ballot.NO_CONFIDENCE in counter.candidates_with_fewest_votes())):
                
                remaining_candidates_to_fill = remaining_candidates    
                
                # In the case where No Confidence has the fewest votes and the
                # other candidates fill the remaining seats, discard No Confidence
                if len(remaining_candidates_to_fill) == remaining_seats + 1:
                    remaining_candidates_to_fill.remove(Ballot.NO_CONFIDENCE)

                # Fill the remaining seats with the remaining candidates,
                # even though they will not meet the quota
                assert len(remaining_candidates_to_fill) <= remaining_seats
                for candidate in remaining_candidates_to_fill:
                    counter.declare_winner(candidate, quota)
                    if (verbose):
                        print("%s is declared a winner in order to fill a remaining seat." % (candidate))
                if verbose and len(counter.winning_candidates) < self.seats:
                    print("There were not enough candidates to fill all seats.")
                break
                
            # If no winners are declared for the round, eliminate the candidate with the fewest votes
            else:
                # Find the candidate(s) (excluding No Confidence) with the fewest votes in the current round
                active_candidates = set(counter.active_candidates())
                if Ballot.NO_CONFIDENCE in active_candidates:
                    active_candidates.remove(Ballot.NO_CONFIDENCE)
                candidates_to_eliminate = counter.candidates_with_fewest_votes(limit_to_candidates=active_candidates)
                assert len(candidates_to_eliminate) >= 1
                
                # If multiple candidates have the fewest votes in a round, choose the candidate with the fewest votes in the previous round
                # Repeat if multiple candidates remain tied with the fewest votes
                previous_voting_round = counter.voting_round - 1
                while(len(candidates_to_eliminate) > 1 and previous_voting_round >= 0):
                    candidates_to_eliminate = counter.candidates_with_fewest_votes(limit_to_candidates=candidates_to_eliminate, voting_round=previous_voting_round)
                    previous_voting_round -= 1
                
                # If only one candidate remains, choose the only candidate from the set
                if len(candidates_to_eliminate) == 1:
                    (losing_candidate,) = candidates_to_eliminate
                    counter.declare_loser(losing_candidate)
                
                # If multiple candidates are still tied for fewest votes,
                # a final tiebreak is required.
                else:
                    # If the election has manual final tiebreaks,
                    # prompt the user to eliminate a candidate
                    if self.is_final_tiebreak_manual:
                        print("\nManual Tiebreak Required:")
                        print("The below candidates are tied for fewest votes for all current and previous rounds:")
                        for candidate_to_eliminate in candidates_to_eliminate:
                            print(candidate_to_eliminate)
                        while True:
                            manually_eliminated_candidate = raw_input("\nSelect a candidate to eliminate: ")
                            if manually_eliminated_candidate in candidates_to_eliminate:
                                counter.declare_loser(manually_eliminated_candidate)
                                break
                            else:
                                print("The candidate to eliminate must be in the above list.")
                    else:
                        # Eliminate a random candidate
                        losing_candidate = random.sample(candidates_to_eliminate, 1).pop()
                        counter.declare_loser(losing_candidate, random=True)
        
        if verbose:
            print("\n*** Conclusion ***")
            print("After %d rounds, the following candidate(s) have been declared winner to fill %d seat(s):" % (counter.voting_round, self.seats))
            for winning_candidate in counter.winning_candidates:
                print(winning_candidate)
            print("***** End Election *****\n")
        
        assert len(counter.winning_candidates) <= self.seats
        return counter.winning_candidates