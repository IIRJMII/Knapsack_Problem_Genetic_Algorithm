from random import randint, random, choice, sample
import matplotlib.pyplot as plt

# Parameters
population_size = 100
num_generations = 100
num_parents = 20

mutation_chance = 1 / 50

#knapsack_size = 103
knapsack_size = 156


# 50/50 chance to either add or remove an item
def mutate(knapsack):
    if random() > 0.5:
        r = randint(0, len(knapsack) - 1)
        knapsack.pop(r)
    else:
        potential_items = [i for i in items if i not in knapsack]
        if len(potential_items) > 0:
            knapsack.append(choice(potential_items))


# Returns the fitness of the knapsack
def fitness(knapsack):
    if len(knapsack) == 0:
        return 0

    value, weight = zip(*knapsack)

    if sum(weight) > knapsack_size:
        return 0
    else:
        return sum(value)


# Returns the average fitness of the generation
def average_generation_fitness(gen):
    return sum([fitness(knapsack) for knapsack in gen]) / len(gen)


# Returns the best fitness of the generation
def best_generation_fitness(gen):
    return max([fitness(knapsack) for knapsack in gen])


# Items to choose from
# [[value, weight], [value, weight]...]
items = [[78, 18], [35, 9], [89, 23], [36, 20], [94, 59], [75, 61], [74, 70], [79, 75], [80, 76], [16, 30]]

# Knapsack = [items[x], items[y], items[z]] = [[value, weight], [value, weight], [value, weight]]

# Create a starting population by taking a random sample of items population_size times
starting_pop = [sample(items, k=randint(1, len(items))) for i in range(population_size)]

# Calculate the average fitness of the starting generation and store it
average_fitness_generations = []
starting_pop_average_fitness = average_generation_fitness(starting_pop)
average_fitness_generations.append(starting_pop_average_fitness)

# Calculate the best fitness in the starting generation and store it
best_fitness_generations = []
starting_pop_best_fitness = best_generation_fitness(starting_pop)
best_fitness_generations.append(starting_pop_best_fitness)

current_gen = starting_pop

best_knapsack = max(starting_pop, key=fitness)

for i in range(1, num_generations):
    # Sort from most fit to least fit
    current_gen.sort(key=fitness, reverse=True)

    # Take the fittest knapsacks as parents
    parents = current_gen[:num_parents]

    next_gen = []

    while len(next_gen) < population_size:
        # Take 2 random parents
        parent_1 = choice(parents)
        parent_2 = choice(parents)

        # Calculate the crossover point as a random number between 1 and the min number of items of both parents
        crossover_point = randint(1, min(len(parent_1), len(parent_2)))

        # Create children from the parents
        child_1 = \
            parent_1[:crossover_point] + [x for x in parent_2[crossover_point:] if x not in parent_1[:crossover_point]]
        child_2 = \
            parent_2[:crossover_point] + [x for x in parent_1[crossover_point:] if x not in parent_2[:crossover_point]]

        # Random chance to mutate (either remove a random item or add a random item)
        if random() <= mutation_chance:
            mutate(child_1)
        if random() <= mutation_chance:
            mutate(child_2)

        # Add children to next generation
        next_gen.extend([child_1, child_2])

    current_gen = next_gen

    # Calculate the average fitness of the generation and store it
    current_average_fitness = average_generation_fitness(current_gen)
    average_fitness_generations.append(current_average_fitness)

    # Calculate the best fitness of the generation and store it
    current_best_fitness = best_generation_fitness(current_gen)
    best_fitness_generations.append(current_best_fitness)

    # Calculate the best knapsack and store it
    best_knapsack = max(best_knapsack, max(current_gen, key=fitness), key=fitness)

# Plot the average generational fitness and best generational fitness over the number of generations
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.plot(range(num_generations), average_fitness_generations, 'b')
plt.plot(range(num_generations), best_fitness_generations, 'r')
plt.show()

print(best_knapsack)
