import pygame, sys, random, time

pygame.mixer.pre_init(frequency=44100,size=-16, channels=1,buffer=512)
pygame.init()

# Game Variables
gravity = 0.2
bird_movement = 0
game_active = True
score = 0
high_score = 0
game_font = pygame.font.Font('04B_19.ttf', 40)

def score_display(game_state):
    if game_state == 'game_active':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 140))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 140))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 770))
        screen.blit(high_score_surface, high_score_rect)

def draw_floor():
    screen.blit(floor_surface, (floor_x_position, 800))
    screen.blit(floor_surface, (floor_x_position + 576, 800))

def create_pipe():
    random_pipe_pos = random.choice(pip_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))

    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 300))
    return  bottom_pipe, top_pipe

def move_pipe(pipes):
    global score
    for pipe in pipes:
        pipe.centerx -= 5
        if(pipe.centerx == 100):
            score += 0.5
            if(score.is_integer()):
                score_sound.play()
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            time.sleep(0.3)
            death_sound.play()
            # print('Collides')
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 800:
        # print('collision')
        death_sound.play()
        return False
    return True

def reset_game():
    global bird_movement
    global game_active
    bird_movement = 0
    global score
    score = 0
    bird_rect.center = 100, 512
    pipe_list.clear()
    game_active = True

def anim_game_over():
    while not game_active:
        # for i in range(12):
        screen.blit(game_over_surface, (90, 312))

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery ))
    return new_bird, new_bird_rect

screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
print(screen.get_size())

back_surf = pygame.image.load('assets/background-day.png').convert()
back_surf = pygame.transform.scale2x(back_surf)

floor_surface = pygame.image.load ('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_position = 0

bird_midflap_surface = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap_surface = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
bird_downflap_surface = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_frames = [ bird_upflap_surface, bird_midflap_surface, bird_downflap_surface]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 512))

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pip_height = [480, 500, 600, 700]

game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_surface = pygame.transform.scale2x(game_over_surface)

BIRDANIM = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDANIM, 150)

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
death_sound = pygame.mixer.Sound('sound/sfx_die.wav')
swoosh_sound = pygame.mixer.Sound('sound/sfx_swooshing.wav')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 7
                bird_rect.centery -= bird_movement
                flap_sound.play()
            elif event.key == pygame.K_SPACE and not game_active:
                reset_game()
        elif event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        elif event.type == BIRDANIM:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    # Background image
    screen.blit(back_surf, (0,0))

    if game_active:
        # Bird
        bird_movement += gravity
        moving_bird = pygame.transform.rotozoom(bird_surface, -bird_movement * 3, 1)
        bird_rect.centery += bird_movement
        screen.blit(moving_bird, bird_rect)
        # screen.blit(bird_surface, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipe(pipe_list)
        draw_pipes(pipe_list)
        score_display("game_active")
    else:
        if score > high_score:
            high_score = score
        score_display("game_over")
        screen.blit(game_over_surface, (90, 185))
        bird_done = pygame.transform.flip(bird_surface,True, True)
        bird_rect.centery += 5
        screen.blit(bird_done, bird_rect)

    # Floor
    floor_x_position -= 1
    draw_floor()
    if floor_x_position <= -576:
        floor_x_position = 0

    pygame.display.update()
    clock.tick(120)
