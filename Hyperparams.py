max_bet = 100
learning_rate = 0.8
discount_factor = 0.95
epsilon = 1.0
epsilon_min = 0.01
epsilon_decay = 0.995
num_episodes = 200
num_generations = 10
pop_size = 500
MUTATION_RATE = 0.1
top_n = 25
count_size = 100

if top_n >= pop_size: raise ValueError("top amount is >= than pop size")
if not int(pop_size/top_n) == pop_size/top_n: raise ValueError("pop size is not a multiple of top_n")
#import Player