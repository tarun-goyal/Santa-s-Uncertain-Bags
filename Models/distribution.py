import numpy as np
import matplotlib.pyplot as plt


horse = [max(0, np.random.normal(5,2,1)[0]) for i in xrange(1000000)]
train = [max(0, np.random.normal(10,5,1)[0]) for i in range(1000000)]
doll = [np.random.gamma(5, 1, 1)[0] for i in xrange(1000000)]
blocks = [np.random.triangular(5, 10, 20, 1)[0] for i in xrange(1000000)]
coal = [47 * np.random.beta(0.5,0.5,1)[0] for i in xrange(1000000)]
bike = [max(0, np.random.normal(20,10,1)[0]) for i in xrange(1000000)]
ball = [max(0, 1 + np.random.normal(1,0.3,1)[0]) for i in xrange(1000000)]
book = [np.random.chisquare(2,1)[0] for i in xrange(1000000)]
gloves = [3.0 + np.random.rand(1)[0] if np.random.rand(1) < 0.3 else np.random.rand(1)[0] for i in xrange(1000000)]

# plt.hist(coal)
# plt.show()

gloves_light = [ele for ele in gloves if ele < 2.0]
gloves_heavy = [ele for ele in gloves if ele > 2.0]
coal_light = [ele for ele in coal if ele < 23.0]
coal_heavy = [ele for ele in coal if ele > 23.0]

print 'horse_S: ', np.mean(horse)
print 'train_S: ', np.mean(train)
print 'doll_S: ', np.mean(doll)
print 'blocks_S: ', np.mean(blocks)
print 'gloves: 2.33:1 ', len(gloves_light), np.mean(gloves_light)
print len(gloves_heavy), np.mean(gloves_heavy)
print 'bike_S: ', np.mean(bike)
print 'ball_S: ', np.mean(ball)
print 'book: ', np.mean(book)
print 'coal: 0.973:1', len(coal_light), np.mean(coal_light)
print len(coal_heavy), np.mean(coal_heavy)
