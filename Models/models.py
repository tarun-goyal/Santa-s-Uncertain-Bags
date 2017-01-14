import pandas as pd
import numpy as np

# SCORE: 22419.17560


# Generating weights for all types of toys
def _generate_weights():
    horse, train, doll, blocks = {}, {}, {}, {}
    for i in xrange(1000):
        horse['horse_' + str(i)] = max(0, np.random.normal(5,2,1)[0])
        train['train_' + str(i)] = max(0, np.random.normal(10,5,1)[0])
        doll['doll_' + str(i)] = np.random.gamma(5,1,1)[0]
        blocks['blocks_' + str(i)] = np.random.triangular(5,10,20,1)[0]
    gloves = {}
    for j in xrange(200):
        gloves['gloves_' + str(j)] = 3.0 + np.random.rand(1)[0] if np.random.rand(1) < 0.3 else np.random.rand(1)[0]
    coal = {}
    for k in xrange(166):
        coal['coal_' + str(k)] = 47 * np.random.beta(0.5,0.5,1)[0]
    bike = {}
    for l in xrange(500):
        bike['bike_' + str(l)] = max(0, np.random.normal(20,10,1)[0])
    ball = {}
    for m in xrange(1100):
        ball['ball_' + str(m)] = max(0, 1 + np.random.normal(1,0.3,1)[0])
    book = {}
    for n in xrange(1200):
        book['book_' + str(n)] = np.random.chisquare(2,1)[0]
    return {'horse': horse,
            'ball': ball,
            'bike': bike,
            'train': train,
            'coal': coal,
            'book': book,
            'doll': doll,
            'blocks': blocks,
            'gloves': gloves
    }


# Restriction on bag total weight
def _check_bag_weight_restriction(bag_total_weight):
    if bag_total_weight < 50:
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
def _create_bags():
    bags = {}
    toys = _generate_weights()
    for i in xrange(1000):
        bags['bag_' + str(i)] = {'gifts': [], 'weights': 0.0}
    used_gifts = []
    for bag_id, contents in bags.iteritems():
        for toy_type, toy in toys.iteritems():
            for toy_id, weight in toy.iteritems():
                if toy_id not in used_gifts:
                    contents['gifts'].append(toy_id)
                    updated_weight = contents['weights'] + weight
                    contents['weights'] = updated_weight
                    used_gifts.append(toy_id)
                if not _check_bag_weight_restriction(contents['weights']):
                    contents['gifts'].remove(toy_id)
                    updated_weight = contents['weights'] - weight
                    contents['weights'] = updated_weight
                    used_gifts.remove(toy_id)
    return bags


# Creating the format of submission
def _capture_answer():
    submission = pd.DataFrame({'bag_id': [], 'Gifts': [], 'number_of_gifts':[], 'total_weight': []})
    bags = _create_bags()
    row_counter = 0
    for bag_id, contents in bags.iteritems():
        answer = ''
        for string in contents['gifts']:
            answer += string + " "
        submission.loc[row_counter, 'bag_id'] = bag_id
        submission.loc[row_counter, 'Gifts'] = answer
        submission.loc[row_counter, 'number_of_gifts'] = len(contents['gifts'])
        submission.loc[row_counter, 'total_weight'] = contents['weights']
        row_counter += 1
    return submission


_capture_answer().to_csv('../Submissions/submission_2.csv', index=False)