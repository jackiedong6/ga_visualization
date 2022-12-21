from .policy import CribbagePolicy, CompositePolicy, GreedyThrower, GreedyPegger
from .policy import ThrowPolicy, PegPolicy
from .scoring import score, greedy_throw
from collections import defaultdict
from .deck import Deck, Card
import random


simulated_data = {(1, 12): 4.033074606116775, (9, 13): 3.6586538461538463, (3, 10): 4.29975671918443, (1, 1): 5.882240500463392, (3, 11): 4.554940917516219, (3, 7): 4.532611214087118, (2, 3): 7.128649212233549, (2, 9): 4.292342446709917, (6, 7): 5.793964318813717, (4, 5): 7.253185820203893, (1, 3): 4.791647358665431, (1, 2): 4.652166357738647, (2, 5): 5.945493512511585, (9, 11): 4.757530120481928, (3, 9): 4.375521316033364, (3, 12): 4.203834569045412, (1, 13): 4.005010426320667, (10, 13): 3.567597312326228, (1, 9): 4.28003359592215, (1, 10): 4.202415430954588, (4, 8): 4.434835495829471, (2, 11): 4.4766276645041705, (2, 10): 4.221443466172381, (4, 7): 4.526326459684894, (4, 12): 4.187384151992585, (8, 13): 3.7017493049119556, (7, 11): 4.1925683503243745, (3, 13): 4.10235171455051, (8, 10): 4.4720227062094535, (8, 11): 4.099658248378128, (6, 9): 5.961017145505097, (11, 13): 4.509528498609824, (4, 6): 5.166647358665431, (7, 13): 3.8133978220574605, (9, 12): 3.705456441149212, (1, 11): 4.457599629286376, (2, 7): 4.451285912882298, (8, 9): 5.1359476367006485, (1, 8): 4.286086654309546, (10, 10): 5.833352641334569, (2, 4): 5.035507414272475, (2, 8): 4.376679796107507, (3, 6): 4.5592562557924, (7, 10): 3.882703892493049, (2, 13): 4.024038461538462, (6, 8): 5.168935356811863, (7, 8): 7.2876795644114924, (3, 8): 4.453139481000926, (1, 6): 4.524009499536608, (3, 3): 6.569450880444856, (6, 12): 3.9598297034291012, (3, 4): 5.735808619091752, (4, 10): 4.356724976830399, (4, 11): 4.611909175162187, (5, 11): 7.657118860055607, (6, 6): 6.691554680259499, (6, 13): 3.8583468489341985, (9, 10): 5.129894578313253, (10, 11): 5.275283827618165, (6, 10): 3.9823331788693235, (2, 6): 4.539330398517145, (4, 13): 4.085901297497683, (5, 9): 5.902166357738647, (2, 12): 4.125521316033364, (12, 12): 5.633167284522706, (7, 9): 4.546628822984244, (5, 13): 7.277948331788693, (12, 13): 4.1584221501390175, (1, 4): 5.703602873030584, (4, 4): 6.527050509731232, (1, 5): 5.991572057460612, (9, 9): 5.906105189990732, (6, 11): 4.2375173772011125, (13, 13): 5.430201575532901, (10, 12): 4.296628822984244, (11, 11): 6.335379981464319, (5, 8): 5.923250695088044, (7, 12): 3.914880676552363, (1, 7): 4.367411955514365, (2, 2): 6.1741774791473585, (8, 12): 3.8032321594068583, (11, 12): 5.311978683966636, (3, 5): 6.65251390176089, (4, 9): 4.35235171455051, (8, 8): 5.9922961075069505, (7, 7): 6.529599165894346, (5, 6): 7.408856580166821, (5, 10): 7.401934661723819, (5, 12): 7.379431186283596, (5, 7): 6.701836190917517, (5, 5): 9.612546339202966}




SCORE_15 = 0
LEAD_FOUR = 0
OVER_15 = 0

class MyPolicy(CribbagePolicy):
    def __init__(self, game, weights):
        global SCORE_15, LEAD_FOUR, OVER_15
        SCORE_15 = weights[0]
        LOW_CARD = weights[1]
        OVER_15 = weights[2]
        self._policy = CompositePolicy(game, HeuristicThrower(game), HeuristicPegger(game))


    def keep(self, hand, scores, am_dealer):
        return self._policy.keep(hand, scores, am_dealer)


    def peg(self, cards, history, scores, am_dealer):
        return self._policy.peg(cards, history, scores, am_dealer)




class HeuristicThrower(ThrowPolicy):
    """ A greedy policy for keep/throw in cribbage.  The greedy decision is
        based only on the score obtained by the cards kept and thrown, without
        consideration for how they might interact with the turned card or
        cards thrown by the opponent.
    """



    def __init__(self, game):
        """ Creates a greedy keep/throw policy for the given game.
            game -- a cribbage Game
        """
        super().__init__(game)

        self.seenThrow = {}
        self.seenTurn = {}
        self.counts = {}
        self.seenTriple = set()
    def heuristic_throw(self, deal, crib, deck):
        # Generates all 15 possible splits


        def score_split(indices):
            keep = []
            throw = []
            for i in range(len(deal)):
                if i in indices:
                    throw.append(deal[i])
                else:
                    keep.append(deal[i])

            total_score = 0
            throwTuple = tuple(sorted([throw[0].rank(), throw[1].rank()]))
            total_turn_cards = len(deck._cards)

            for card in deck._cards:
                total_score += score(self._game, keep, card, False)[0] + crib * simulated_data[throwTuple]


            average_score = total_score / total_turn_cards

            return keep, throw, average_score





        throw_indices = self._game.throw_indices()

        return max(map(lambda i: score_split(i), throw_indices), key=lambda t: t[2])


    def keep(self, hand, scores, am_dealer):
        """ Selects the cards to keep to maximize the net score for those cards
            and the cards in the crib.  Points in the crib count toward the
            total if this policy is the dealer and against the total otherwise.
            hand -- a list of cards
            scores -- the current scores, with this policy's score first
            am_dealer -- a boolean flag indicating whether the crib
                         belongs to this policy
        """


        # samples = []
        deck = self._game.deck()
        deck.remove(hand)
        # for i in range(10000):
        #     deck.shuffle()
        #     turnCard = deck._cards[0]
        #     newHand = deck.peek(7)[1:]
        #     samples.append([turnCard, greedy_throw(self._game, newHand, 1 if am_dealer else -1)[1]])
        # self.simulations = samples
        keep, throw, net_score = self.heuristic_throw(hand, 1 if am_dealer else -1, deck)


        return keep, throw





class HeuristicPegger(PegPolicy):
    """ A cribbage pegging policy that plays the card that maximizes the
        points earned on the current play.
    """

    def __init__(self, game):
        """ Creates a greedy pegging policy for the given game.
            game -- a cribbage Game
        """
        super().__init__(game)
        self.game = game

    def peg(self, cards, history, scores, am_dealer):
        """ Returns the card that maximizes the points earned on the next
            play.  Ties are broken uniformly randomly.
            cards -- a list of cards
            history -- the pegging history up to the point to decide what to play
            scores -- the current scores, with this policy's score first
            am_dealer -- a boolean flag indicating whether the crib
                         belongs to this policy
        """


        # shuffle cards to effectively break ties randomly
        ## Cards start with 4 then 3 then 2 then 1
        # maybe we want to lead with a 10 if we have two fives
        # maybe we want to lead with a 7 if we have a 9


        card_weight = dict.fromkeys(cards, 0)
        currentTotal = history.total_points()


        # history.has_passed(1 if am dealer else 0)

        if cards:
            # The current total is 0
            if currentTotal == 0:

                # Create a dictionary of card ranks as keys with values as lists of cards with a certain rank
                card_count = defaultdict(list)

                # Heuristic here is to lead with a 4 or bait the greedy opponent
                for card in cards:
                    card_count[self._game.rank_value(card.rank())].append(card)
                    if card.rank() == 4:

                        card_weight[card] += LEAD_FOUR
                    if card.rank() == 5:
                        card_weight[card] -= 1


                # change the values to counts
                if 7 in card_count and 9 in card_count:
                    for element in card_count[7]:
                        card_weight[element] += 2.25

                if 5 in card_count and 10 in card_count:
                    if len(card_count[5]) > 1:
                        for element in card_count[10]:

                            card_weight[element] += 2.25

            # Heuristic here is to play a low card
            elif currentTotal < 5:
                # Total is low and opponent has played low card, if i play a low card -> then it can set opponent up for a run / double
                for card in cards:
                    if card.rank() < 4:
                        card_weight[card] += 1


            # Heuristic here is to get 15 to score or over 15 to prevent the opponent from scoring
            elif currentTotal < 15:
                for card in cards:


                    ## Might be redundant
                    if self._game.rank_value(card.rank()) + currentTotal == 15:
                        card_weight[card] += SCORE_15
                    if self._game.rank_value(card.rank()) + currentTotal > 15:
                        card_weight[card] += OVER_15
            else:
                max_rank = 0
                max_card = None
                for card in cards:

                    if self._game.rank_value(card.rank()) + currentTotal == 21 or self._game.rank_value(card.rank()) + currentTotal == 26:
                        card_weight[card] -= 0.5

                    # Redundant
                    if self._game.rank_value(card.rank()) + currentTotal == 31:
                        card_weight[card] += 2

                    if self._game.rank_value(card.rank()) > max_rank and (self._game.rank_value(card.rank()) + currentTotal) < 31:
                        max_card = card
                        max_rank = self._game.rank_value(card.rank())

                if max_card:
                    card_weight[max_card] += 1.5

            for card in cards:
                score = history.score(self._game, card, 0 if am_dealer else 1)
                if score is not None:
                    card_weight[card] += score


            vals = list(card_weight.values())
            keys = list(card_weight.keys())
            maxWeight = keys[vals.index(max(vals))]

            return maxWeight if history.is_legal(self._game, maxWeight, am_dealer) else None
