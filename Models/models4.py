import pandas as pd
import numpy as np
import pickle

# SCORE: 23215.37520


# Additional changes:
# 1. Distribution iterations from 1000 to 10000000
# 2. Merge all toy types dictionaries into one before iterating over it
# 3. Check number of used_gifts before proceeding for iteration
# 4. Remove toy_id from dictionary if already used
# 5. Add minimum of 3 gifts to every bag condition, else remove the busted bag

# Calculating mean weights for every toy type using distribution
def _mean_distribution():
    _horse = np.mean([max(0, np.random.normal(5,2,1)[0]) for i in xrange(10000000)])
    _train = np.mean([max(0, np.random.normal(10,5,1)[0]) for i in xrange(10000000)])
    _doll = np.mean([np.random.gamma(5, 1, 1)[0] for i in xrange(10000000)])
    _blocks = np.mean([np.random.triangular(5, 10, 20, 1)[0] for i in xrange(10000000)])
    _coal = [47 * np.random.beta(0.5,0.5,1)[0] for i in xrange(10000000)]
    _bike = np.mean([max(0, np.random.normal(20,10,1)[0]) for i in xrange(10000000)])
    _ball = np.mean([max(0, 1 + np.random.normal(1,0.3,1)[0]) for i in xrange(10000000)])
    _book = np.mean([np.random.chisquare(2,1)[0] for i in xrange(10000000)])
    _gloves = [3.0 + np.random.rand(1)[0] if np.random.rand(1) < 0.3
               else np.random.rand(1)[0] for i in xrange(10000000)]

    _gloves_light = np.mean([ele for ele in _gloves if ele <= 2.0])
    _gloves_heavy = np.mean([ele for ele in _gloves if ele > 2.0])
    _coal_light = np.mean([ele for ele in _coal if ele < 23.0])
    _coal_heavy = np.mean([ele for ele in _coal if ele >= 23.0])
    return _horse, _train, _doll, _blocks, _bike, _ball, _book, _gloves_light,\
        _gloves_heavy, _coal_light, _coal_heavy


# Generating weights for all types of toys
def _generate_weights():
    _horse, _train, _doll, _blocks, _bike, _ball, _book, _gloves_light, \
        _gloves_heavy, _coal_light, _coal_heavy = _mean_distribution()
    horse, train, doll, blocks = {}, {}, {}, {}
    for i in xrange(1000):
        horse['horse_' + str(i)] = _horse
        train['train_' + str(i)] = _train
        doll['doll_' + str(i)] = _doll
        blocks['blocks_' + str(i)] = _blocks
    gloves = {}
    for j in xrange(140):
        gloves['gloves_' + str(j)] = _gloves_light
    for j in range(140, 200):
        gloves['gloves_' + str(j)] = _gloves_heavy
    coal = {}
    for k in xrange(82):
        coal['coal_' + str(k)] = _coal_light
    for k in range(82, 166):
        coal['coal_' + str(k)] = _coal_heavy
    bike = {}
    for l in xrange(500):
        bike['bike_' + str(l)] = _bike
    ball = {}
    for m in xrange(1100):
        ball['ball_' + str(m)] = _ball
    book = {}
    for n in xrange(1200):
        book['book_' + str(n)] = _book
    toys_dict = _merge_all_dictionaries(horse, ball, bike, train, coal, book,
                                        doll, blocks, gloves)
    return toys_dict


# Merge all dictionaries into one
def _merge_all_dictionaries(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


# Restriction on bag total weight
def _check_bag_weight_restriction(bag_total_weight):
    if bag_total_weight <= 50:
        return True
    else:
        return False


# Restriction on number of gifts in one bag
def _check_minimum_number_of_gifts_in_bag(number_of_gifts):
    if number_of_gifts < 3:
        return False
    else:
        return True


# Creating bags of gifts:
def _fill_bags_with_gifts():
    bags = {}
    toys = _generate_weights()
    toys_copy = toys.copy()
    used_gifts = []
    not_used = []
    not_used_dict = {}
    number_of_bags = 0
    for bag_id in xrange(1100):
        used_gifts = list(set(used_gifts))
        for id in used_gifts:
            if id in toys:
                del toys[id]
        toys = {k: v for k, v in toys.iteritems() if v <= 50 - 2 * min(
            toys.itervalues())}
        if len(used_gifts) == 7166:
            print 'not used: ', len(not_used)
            print not_used
            for rem in not_used:
                not_used_dict[rem] = toys_copy[rem]
            pickle.dump(not_used_dict, open('../Data/toys_remaining.pickle', 'wb'))
            break
        else:
            number_of_bags += 1
            bag = 'bag_' + str(bag_id)
            bags[bag] = {'gifts': [], 'weights': 0.0}
            print number_of_bags, len(used_gifts), len(toys.keys())
            for toy_id, weight in toys.iteritems():
                if toy_id not in used_gifts:
                    bags[bag]['gifts'].append(toy_id)
                    bags[bag]['weights'] += weight
                    used_gifts.append(toy_id)
                if not _check_bag_weight_restriction(bags[bag]['weights']):
                    bags[bag]['gifts'].remove(toy_id)
                    bags[bag]['weights'] -= weight
                    used_gifts.remove(toy_id)
        if not _check_minimum_number_of_gifts_in_bag(len(bags[bag]['gifts'])):
            not_used.extend(bags[bag]['gifts'])
        # used_gifts = [e for e in used_gifts if e not in bags[bag]['gifts']]
            del bags[bag]
    return bags


# Creating the format of submission
def _capture_answer():
    submission = pd.DataFrame(columns=['bag_id', 'Gifts', 'number_of_gifts',
                                       'total_weight'])
    bags = _fill_bags_with_gifts()
    row_counter = 0
    for bag_id, contents in bags.iteritems():
        answer = ''
        for string in contents['gifts']:
            answer += string + " "
        submission.loc[row_counter] = [bag_id, answer, len(contents['gifts']),
                                       contents['weights']]
        row_counter += 1
    return submission


_capture_answer().to_csv('../Submissions/submission_14.csv', index=False)