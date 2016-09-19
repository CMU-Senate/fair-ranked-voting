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
    NO_CONFIDENCE = "No Confidence"

    def __init__(self, vote_value=1.0):
        self.vote_value = vote_value
        self._preferred_active_rank = 1
        self._ranks = dict()

    def preferred_active_candidate(self):
        return self._ranks.get(self._preferred_active_rank)
        
    def eliminate_preferred_candidate(self):
        current_preferred_active_candidate = self.preferred_active_candidate()
        if current_preferred_active_candidate == None:
            print("Ballot Error: This ballot has no active candidates.")
        elif current_preferred_active_candidate == Ballot.NO_CONFIDENCE:
            print("Ballot Error: Cannot eliminate No Confidence from a ballot.")
        else:
            self._preferred_active_rank += 1
        
    def set_candidate_with_rank(self, candidate, rank):
        if self._ranks.get(rank) != None:
            print("Ballot Error: That rank has already been assigned to a candidate.")
            assert False
        self._ranks[rank] = candidate
       
    def __copy__(self):
        ballot_copy = Ballot()
        ballot_copy.vote_value = self.vote_value
        ballot_copy._preferred_active_rank = self._preferred_active_rank
        ballot_copy._ranks = copy.copy(self._ranks)
        return ballot_copy
     
    def __repr__(self):
        ballot_string = "Ballot %d:" % id(self)
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
    def __init__(self, verbose=False):
        self.voting_round = 0
        self.verbose = verbose
        self.winning_candidates = set()
        self.losing_candidates = set()
        
        self._votes_for_candidate_per_round = list()
        self._votes_for_candidate_per_round.append(dict())
        self._ballots_for_candidate = dict()
    
    def verbose_print(self, *args, **kwargs):
        if self.verbose:
            print(args, kwargs)
    
    def advance_voting_round(self):
        self.voting_round += 1
        self._votes_for_candidate_per_round.append(copy.copy(self._votes_for_candidate_per_round[self.voting_round - 1]))
        assert len(self._votes_for_candidate_per_round) == self.voting_round + 1
    
    def updated_ballot_for_eliminated_candidates(self, ballot):
        updated_ballot = copy.copy(ballot)
        while True:
            preferred_candidate = updated_ballot.preferred_active_candidate()
            if preferred_candidate == None:
                break
            elif not self.is_candidate_eliminated(preferred_candidate):
                break
            else:
                updated_ballot.eliminate_preferred_candidate()
        return updated_ballot
        
    def cast_ballot(self, ballot):
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
        if voting_round is None:
            voting_round = self.voting_round
        return self._votes_for_candidate_per_round[voting_round].keys()

    def is_candidate_eliminated(self, candidate):
        return candidate in self.winning_candidates or candidate in self.losing_candidates

    def ballots_for_candidate(self, candidate):
        return self._ballots_for_candidate.get(candidate)
        
    def votes_for_candidate(self, candidate, voting_round=None):
        if voting_round is None:
            voting_round = self.voting_round
        return self._votes_for_candidate_per_round[voting_round].get(candidate)

    def candidates_reaching_quota(self, quota, limit_to_candidates=None, voting_round=None):
        if voting_round is None:
            voting_round = self.voting_round
        if limit_to_candidates is None:
            limit_to_candidates = self.active_candidates(voting_round)
        
        candidates_reaching_quota = set()
        
        for candidate in limit_to_candidates:
            candidate_votes = self.votes_for_candidate(candidate, voting_round=voting_round)
            if candidate_votes >= quota:
                candidates_reaching_quota.add(candidate)
                
        return candidates_reaching_quota

    def candidates_with_fewest_votes(self, limit_to_candidates=None, voting_round=None):
        if voting_round is None:
            voting_round = self.voting_round
        if limit_to_candidates is None:
            limit_to_candidates = self.active_candidates(voting_round)
            
        candidates_with_fewest_votes = set()
        fewest_votes = -1
        
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
        self.winning_candidates.add(candidate)
        candidate_ballots = self._ballots_for_candidate.pop(candidate)
        candidate_votes = self._votes_for_candidate_per_round[self.voting_round].pop(candidate)
        
        self.verbose_print("%s is declared a winner, with %.2f votes in this round." % (candidate, candidate_votes))
        
        # If a candidate's votes exceed the quota, redistribute
        if candidate_votes > quota and candidate != Ballot.NO_CONFIDENCE:
            surplus = candidate_votes - quota
            surplus_multiplier = (surplus / candidate_votes)
            for candidate_ballot in candidate_ballots:
                updated_ballot = self.updated_ballot_for_eliminated_candidates(candidate_ballot)
                updated_ballot.vote_value *= surplus_multiplier
                self.cast_ballot(updated_ballot)
                
            self.verbose_print("%s's surplus of %.2f votes will be redistributed amongst their ballots, each worth %.2f votes." % (candidate, surplus, surplus_multiplier))

        
    def declare_loser(self, candidate, verbose=False):
        self.losing_candidates.add(candidate)
        candidate_ballots = self._ballots_for_candidate.pop(candidate)
        candidate_votes = self._votes_for_candidate_per_round[self.voting_round].pop(candidate)
        
        self.verbose_print("%s has the fewest votes and will be eliminated, with %.2f votes in this round. Their votes will be redistributed amongst their ballots." % (candidate, candidate_votes))
        
        for candidate_ballot in candidate_ballots:
            updated_ballot = self.updated_ballot_for_eliminated_candidates(candidate_ballot)
            self.cast_ballot(updated_ballot)

class Election:
    def __init__(self, name="", seats=1):
        self.name = name
        self.seats = seats
        self.ballots = list()
    
    def droop_quota(self, votes, seats):
        return math.floor(votes / (seats + 1)) + 1
    
    def compute_winners(self, verbose=False):
        counter = Election_Counter(verbose=verbose)
                    
        # Determine quota
        quota = self.droop_quota(len(self.ballots), self.seats)
        
        if (verbose):
            print("***** Election: %s *****" % self.name)
            print("There were %d ballots cast to fill %d seat(s)." % (len(self.ballots), self.seats))
            print("A quota of %d votes is required to win outright." % (quota))
        
        # Cast initial ballots
        for ballot in self.ballots:
            counter.cast_ballot(ballot)
                
        while len(counter.winning_candidates) < self.seats:
            counter.advance_voting_round()
            
            if (verbose):
                print("\n*** Voting Round %d ***" % counter.voting_round)
            
            # Check for a winner (a candidate whose votes meet the quota)
            winners_for_round = counter.candidates_reaching_quota(quota)
            remaining_candidates = counter.active_candidates()
            
            # Declare any winners, redistributing their surplus votes 
            if len(winners_for_round) > 0:
                for winning_candidate in winners_for_round:
                    counter.declare_winner(winning_candidate, quota)
                    
            # If the remaining seats must be filled by the remaining candidates, fill them.
            elif len(remaining_candidates) + len(counter.winning_candidates) <= self.seats:
                for candidate in remaining_candidates:
                    counter.declare_winner(candidate, quota)
                    if (verbose):
                        print("%s is declared a winner in order to fill a remaining seat." % (candidate))
                if verbose and len(counter.winning_candidates) < self.seats:
                    print("There were not enough candidates to fill all seats.")
                break
                
            # If no winners are declared for the round, eliminate the candidate with the fewest votes
            else:
                # Find the candidate(s) with the fewest votes in the current round            
                candidates_to_eliminate = counter.candidates_with_fewest_votes()
                assert len(candidates_to_eliminate) > 0
                
                # If multiple candidates have the fewest votes in a round, choose the candidate with the fewest votes in the previous round
                # Repeat if multiple candidates remain tied with the fewest votes
                previous_voting_round = counter.voting_round - 1
                while(len(candidates_to_eliminate) > 1 and previous_voting_round >= 0):
                    candidates_to_eliminate = counter.candidates_with_fewest_votes(limit_to_candidates=candidates_to_eliminate, voting_round=previous_voting_round)
                    previous_voting_round -= 1
                
                # If multiple candidates are tied for fewest votes in all previous rounds, choose a random candidate to eliminate
                # If only one candidate remains, choose the only candidate from the set
                losing_candidate = random.sample(candidates_to_eliminate, 1).pop()
                counter.declare_loser(losing_candidate)
        
        if verbose:
            print("\n*** Conclusion ***")
            print("After %d rounds, the following candidate(s) have been declared winner to fill %d seat(s):" % (counter.voting_round, self.seats))
            for winning_candidate in counter.winning_candidates:
                print(winning_candidate)
            print("***** End Election *****\n")
        
        assert len(counter.winning_candidates) <= self.seats
        return counter.winning_candidates