import pygame
import random
import numpy
import math


class NetworkLayer:
    def __init__(self, shape, weights=None, biases=None):
        self.num_inputs = shape[0]
        self.num_outputs = shape[1]
        self.weights = weights
        self.biases = biases
        if weights is None:
            self.weights = [[random.uniform(-1, 1) for _ in range(self.num_inputs)]
                            for _ in range(self.num_outputs)]
        if biases is None:
            self.biases = [random.uniform(-4, 4) for _ in range(self.num_outputs)]

    def calc(self, inputs):
        outputs = []

        for node_out in range(self.num_outputs):
            output = 0
            for node_in in range(self.num_inputs):
                output += inputs[node_in] * self.weights[node_out][node_in]
            outputs.append(math.tanh(output + self.biases[node_out]))
        return outputs

    def mutated(self, max_mutation):
        new_weights = self.weights.copy()
        for w in range(len(new_weights)):
            new_weights[w] += numpy.random.uniform(-max_mutation, max_mutation, len(self.weights[w]))
        new_biases = self.biases + numpy.random.uniform(-max_mutation, max_mutation, len(self.biases))
        return NetworkLayer((self.num_inputs, self.num_outputs), new_weights, new_biases)


class Network:
    def __init__(self, shape, layers=None):
        self.layers = layers
        if layers is None:
            self.layers = [NetworkLayer(size) for size in shape]

    def feed_forward(self, inputs):
        for layer in self.layers:
            inputs = layer.calc(inputs)
        return inputs

    def mutated(self, max_mutation):
        return Network(None, [layer.mutated(max_mutation) for layer in self.layers])


class Player:
    def __init__(self, net=None):
        self.x = 20
        self.y = 320
        self.alive = True
        self.net = net
        if net is None:
            self.net = Network(((2, 10), (10, 20), (20, 1)))
        self.score = 0

    def update(self, delta_time):
        if self.alive:
            self.y -= speed * delta_time
            self.score += speed * delta_time    # / abs(obstacles[0][1] - 60 - self.y)

            if round(self.net.feed_forward((self.y, obstacles[0][1]))[0]):
                self.y += random.uniform(2, 2.2) * delta_time

            if self.y <= 0 or 550 <= self.y:
                self.alive = False

            if obstacles[0][0] <= 76 and not obstacles[0][1] + 10 > self.y > obstacles[0][1] - 130:
                self.alive = False
        else:
            self.x -= speed * delta_time

    def mutate_x(self, amount: int, max_off):
        return [Player(self.net.mutated(max_off)) for _ in range(amount - 1)]


class RealPlayer:
    def __init__(self):
        self.x = 20
        self.y = 320
        self.alive = True

    def update(self, delta_time):
        if self.alive:
            self.y -= speed * delta_time

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.y += 2 * speed * delta_time

            if self.y <= 0 or 550 <= self.y:
                self.alive = False

            if obstacles[0][0] <= 76 and not obstacles[0][1] + 10 > self.y > obstacles[0][1] - 130:
                self.alive = False
        else:
            self.x -= speed * delta_time


seed = 3     # guter seed: "KI"; schlechter seed als bsp: 3, "Maciej"

random.seed(seed)
pygame.init()
screen = pygame.display.set_mode((640, 640))
clock = pygame.time.Clock()
running = True

gen_size = 30

bird = pygame.transform.scale_by(pygame.image.load("bird.png"), 4.0)
bird_player = pygame.transform.scale_by(pygame.image.load("bird.png"), 4.0)
red_surf = pygame.Surface((64, 64), pygame.SRCALPHA)
red_surf.fill((255, 0, 0, 100))
bird_player.blit(red_surf, (0, 0))
bird_player.set_colorkey((255, 0, 0, 100))
bird.set_alpha(180)
bird_dead = pygame.transform.scale_by(pygame.image.load("bird.png"), 4.0)
bird_dead.set_alpha(30)
players = [Player() for _ in range(gen_size)]
obstacles = [[400, random.randint(200, 480)]]

real_player = RealPlayer()

counter = 0
next_c = 0

speed = 0.15

max_score_prev = -1
best_prev = players[0]

focus_one = False
versus_player = False
paused = False
step = False


while running:
    delta = clock.tick(60)
    screen.fill((0, 210, 230))

    if not paused or step:
        counter += delta
        speed += 0.00005 * speed ** 0.8 * delta

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_i:
                    focus_one = not focus_one
                case pygame.K_e:
                    random.seed(seed)
                    real_player = RealPlayer()
                    obstacles = [[400, random.randint(200, 480)]]
                    counter = 0
                    next_c = 0
                    speed = 0.15
                    versus_player = not versus_player
                case pygame.K_p:
                    paused = not paused
                case pygame.K_w:
                    step = True

    any_alive = False

    alive = []

    for player in players:
        if not paused or step:
            player.update(delta)
        if not player.alive:
            if not focus_one:
                screen.blit(bird_dead, (player.x, 550 - player.y))
        else: alive.append(player)

    for player in alive:
        screen.blit(bird, (player.x, 550 - player.y))
        any_alive = True
        if focus_one:
            break

    if versus_player:
        if not paused or step:
            real_player.update(delta)
        screen.blit(bird_player, (real_player.x, 550 - real_player.y))

    pygame.draw.rect(screen, "red", (0, 600, 640, 40))

    if counter >= 0.15 * next_c / speed:
        obstacles.append([640, random.randint(200, 480)])
        next_c = random.randint(1700, 2475)
        counter = 0

    for i, obstacle in enumerate(obstacles):
        pygame.draw.rect(screen, "green", (obstacle[0], 0, 60, 540 - obstacle[1]))
        pygame.draw.rect(screen, "green", (obstacle[0], 740 - obstacle[1], 60, obstacle[1] - 100))

        if not paused or step:
            obstacle[0] -= speed * delta

    if obstacles[0][0] < -60:
        obstacles = obstacles[1:]

    if not any_alive and (not versus_player or not real_player.alive):
        random.seed(seed)
        players.sort(key=lambda p: p.score, reverse=True)
        print(list(map(lambda p: p.score, players)))

        if players[0].score > max_score_prev:
            max_score_prev = players[0].score
            players = players[0].mutate_x(gen_size, 0.3) + [Player(players[0].net)]
            best_prev = Player(players[0].net)
        else:
            players = best_prev.mutate_x(gen_size, 0.3) + [Player(best_prev.net)]
        real_player = RealPlayer()
        obstacles = [[400, random.randint(200, 480)]]
        counter = 0
        next_c = 0
        speed = 0.15

    step = False

    pygame.display.flip()
