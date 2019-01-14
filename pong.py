import pygame, random


# DEFINES COLORS
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]

NEON_BLUE = [1, 1, 255]
LIME_GREEN = [50, 205, 50]
NEON_RED = [255, 1, 1]

GAME_FONT = [215, 218, 190]

LINE_COLOR = [180, 180, 180]



class Window:

    # CREATES GAME WINDOW
    width = 1000
    height = 600
    screen = pygame.display.set_mode( (width, height) )



class Globals:

    # GAME RUNNING VARIABLE
    running = True

    # FPS VARIABLE
    fps = 60

    # PLAYING GAME VARIABLE
    play = False

    # START PLAYING GAME VARIABLE
    start_game = False

    # ALLOW UP AND DOWN MOVEMENT FOR PADDLES
    upL, downL = True, True
    upR, downR = True, True

    # COUNTDOWN VARIABLE
    countdown = 3

    # SCORE GOAL VARIABLE
    goal = False

    # KEEPS TRACK OF SCORE FROM EACH PLAYER
    player_score = {'1': 0, '2': 0}

    # DICTIONARY TO DETERMINE WHO SERVES
    player_serve = {'1': False, '2': False}

    # SCORE LIMIT VARIABLE
    score_limit = 5

    # MAX SPEED FOR BALL
    max_speed = False

    # GAME VARIABLES
    GAME_OVER = False
    new_game = True

    # LOSER VARIABLE
    loser = 0

    # FADE IN VARIABLE (CRAPPY)
    vol = 0



# CREATES BALL OBJECT
class BallClass(pygame.sprite.Sprite):
    def __init__(self, location, color, speed, radius):
        pygame.sprite.Sprite.__init__(self)

        # BALL COLOR
        self.color = color

        # BALL RADIUS
        self.radius = radius

        # CENTER LOCATION FOR BALL
        self.center = location

        # CREATES IMAGE SURFACE FOR BALL
        image_surf = pygame.Surface( (self.radius*2, self.radius*2) )
        

        # CONVERTS SURFACE TO AN IMAGE
        self.image = image_surf.convert()
        self.rect = self.image.get_rect()

        self.rect.left, self.rect.top = location

        # SPEED VARIABLE
        self.speed = speed
        


    def update(self):

        # MOVES BALL AND DISPLAYS IT ON SCREEN
        if Globals.play == True and Globals.countdown == 0:
            self.rect = self.rect.move(self.speed)


        # PUTS BALL IN FRONT OF SERVING PADDLE
        if Globals.player_serve['1']:
            self.location[1] = (Objects.paddleL.rect.top + Objects.paddleL.size[1]/2) - self.radius
            self.rect.top = self.location[1]

        elif Globals.player_serve['2']:
            self.location[1] = (Objects.paddleR.rect.top + Objects.paddleR.size[1]/2) - self.radius
            self.rect.top = self.location[1]
            

        # DRAWS BALL
        pygame.draw.circle( Window.screen, self.color, [self.rect.centerx, self.rect.centery], self.radius, 0 )




# CREATES PADDLE OBJECTS
class PaddleClass(pygame.sprite.Sprite):
    def __init__(self, location, color, size):

                # INITIALIZES SPRITE
        pygame.sprite.Sprite.__init__(self)

        # START LOCATION FOR PADDLE
        self.start_pos = location

        # SIZE VARIABLE
        self.size = size

        # CREATES IMAGE SURFACE FOR PADDLES
        image_surf = pygame.Surface(size)

        # FILLS IMAGE SURFACES WITH DESIRED COLORS
        image_surf.fill(color)

        # CONVERTS SURFACE TO AN IMAGE
        self.image = image_surf.convert()
        self.rect = self.image.get_rect()

        self.rect.left, self.rect.top = location

        self.speedUP, self.speedDOWN = 0, 0



    def update(self):

        # DISPLAYS PADDLES ON SCREEN
        Window.screen.blit(self.image, self.rect)



# GAME OBJECTS
class Objects:

    # ----- SETS OBJECT PROPERTIES ----- #
    
    # --- PADDLES --- #
    # SPEED
    paddle_speed = 12
    # SIZE
    paddle_size = [20, 100]
    # CENTER VERTICALLY
    paddle_posY = (Window.height/2) - (paddle_size[1]/2)


    # --- BALL --- #

	# START SPEED
    ball_start_speed = 5

    # SPEED
    ball_speedX = ball_start_speed
    ball_speedY = ball_start_speed

    # RANDOM X DIRECTION
    ball_direction = random.choice([ball_start_speed, -ball_start_speed])


    # CREATES OBJECTS
    paddleL = PaddleClass( [50, paddle_posY], NEON_BLUE, paddle_size )
    paddleR = PaddleClass( [930, paddle_posY], NEON_RED, paddle_size )
    ball = BallClass( [490, 290], LIME_GREEN, [ball_direction, ball_speedY], 10 )



class SpritesClass:

    def __init__(self):

        # CREATES SPRITE GROUPS
        self.paddle_group = pygame.sprite.Group(Objects.paddleL, Objects.paddleR)

        self.ball_group = pygame.sprite.GroupSingle(Objects.ball)

        self.all_sprites = pygame.sprite.Group(self.paddle_group, self.ball_group)



    def animate(self):

        # DRAWS CENTER LINE
        pygame.draw.rect(Window.screen, LINE_COLOR, [499, 0, 1, 800], 2)
        pygame.draw.circle(Window.screen, LINE_COLOR, [500, 300], 80, 1)
    
        # UPDATES SPRITES
        self.all_sprites.update()



    def reset_sprites(self, player):

        # RESETS BALL SPEED
        Objects.ball_speedX = Objects.ball_start_speed
        Objects.ball_speedY = Objects.ball_start_speed

        # RESETS SPRITES TO ORIGINAL POSITIONS FOR NEW SERVE
        if player == 1:
            Objects.ball.location = [860, 290]
            Objects.ball.speed[0] = -Objects.ball_speedX

        elif player == 2:
            Objects.ball.location = [120, 290]
            Objects.ball.speed[0] = Objects.ball_speedX


        Objects.ball.speed[1] = Objects.ball_speedY
        Objects.ball.rect.left = Objects.ball.location[0]
        Objects.ball.rect.top = Objects.ball.location[1]

        Objects.paddleL.rect.top = Objects.paddleL.start_pos[1]
        Objects.paddleR.rect.top = Objects.paddleR.start_pos[1]

        Objects.paddleL.speedUP, Objects.paddleL.speedDOWN = 0, 0
        Objects.paddleR.speedUP, Objects.paddleR.speedDOWN = 0, 0

        Globals.max_speed = False

        



    def collision(self):

        # CHECKS FOR COLLISIONS BETWEEN SPRITES
        # CHECKS FOR OBJECTS LEAVING SCREEN

        # PREVENTS PADDLES FROM GOING ANY HIGHER OR LOWER THAN SCREEN
        if Objects.paddleR.rect.bottom >= Window.height:
            Globals.downR = False
        else: Globals.downR = True

        if Objects.paddleL.rect.bottom >= Window.height:
            Globals.downL = False
        else: Globals.downL = True

        if Objects.paddleR.rect.top <= 0:
            Globals.upR = False
        else: Globals.upR = True

        if Objects.paddleL.rect.top <= 0:
            Globals.upL = False
        else: Globals.upL = True


        # BALL BOUNCES OFF OF TOP AND BOTTOM OF SCREEN
        if Objects.ball.rect.top < 0:
            Objects.ball.speed[1] = Objects.ball_speedY
            
        elif Objects.ball.rect.bottom > Window.height:
            Objects.ball.speed[1] = -Objects.ball_speedY



        # BALL INCREASES IN SPEED WITH EACH PADDLE HIT
        if pygame.sprite.spritecollide(Objects.ball, self.paddle_group, False):
            Game.hit_paddle.play()
            
            if Objects.ball.speed[0] >= 20:
                Globals.max_speed = True
                
            if not Globals.max_speed:

                Objects.ball_speedX += 0.5
                Objects.ball_speedY += 0.5



        # BALL BOUNCES OFF OF RIGHT PADDLE
        if pygame.sprite.spritecollide(Objects.paddleR, self.ball_group, False):
            Objects.ball.speed[0] = -Objects.ball_speedX

            # BALL BOUNCES OFF OF TOP AND BOTTOM OF PADDLE
            if Objects.ball.rect.bottom <= Objects.paddleR.rect.top + Objects.ball.radius:
                Objects.ball.speed[1] = -Objects.ball_speedY

            elif Objects.ball.rect.top >= Objects.paddleR.rect.bottom - Objects.ball.radius:
                Objects.ball.speed[1] = Objects.ball_speedY

            else:
                if Objects.ball.speed[1] > 0:
                    Objects.ball.speed[1] = Objects.ball_speedY

                else:
                    Objects.ball.speed[1] = -Objects.ball_speedY
                
                
        # BALL BOUNCES OFF OF LEFT PADDLE
        elif pygame.sprite.spritecollide(Objects.paddleL, self.ball_group, False):
            Objects.ball.speed[0] = Objects.ball_speedX

            # BALL BOUNCES OFF OF TOP AND BOTTOM OF PADDLE
            if Objects.ball.rect.bottom <= Objects.paddleL.rect.top + Objects.ball.radius:
                Objects.ball.speed[1] = -Objects.ball_speedY

            elif Objects.ball.rect.top >= Objects.paddleL.rect.bottom - Objects.ball.radius:
                Objects.ball.speed[1] = Objects.ball_speedY

            else:
                if Objects.ball.speed[1] > 0:
                    Objects.ball.speed[1] = Objects.ball_speedY

                else:
                    Objects.ball.speed[1] = -Objects.ball_speedY



        # ADDS TO PLAYER SCORE IF BALL IS SCORED IN GOAL
        if Objects.ball.rect.right < -5:
            Globals.player_score['2'] += 1
            Globals.goal = True
            Game.score_goal.play()

            Text.playerGoal(2, NEON_RED, Text.player_goal_pos['2'])
            Globals.goal = False
            Globals.play = False

            Globals.player_serve['1'] = True

            self.reset_sprites(2)


        elif Objects.ball.rect.left > Window.width + 5:
            Globals.player_score['1'] += 1
            Globals.goal = True
            Game.score_goal.play()

            Text.playerGoal(1, NEON_BLUE, Text.player_goal_pos['1'])
            Globals.goal = False
            Globals.play = False

            Globals.player_serve['2'] = True

            self.reset_sprites(1)



Sprites = SpritesClass()




class Fonts:

    def __init__(self):

        # CREATES FONT OBJECTS
        pygame.font.init()
        font_type = pygame.font.match_font('Fixedsys Regular')
        self.countdown_font = pygame.font.SysFont('fixedsys regular', 130)
        self.score_font = pygame.font.SysFont('fixedsys, regular', 35)
        self.loser_font = pygame.font.Font(None, 100)
        self.font = pygame.font.Font(None, 50)

        # CREATES FONT STRINGS
        self.play_again_string = 'Press SPACE to play again, or ESC to quit game'
        self.serve_string = 'PRESS SPACE'


        # CREATES FONT SURFACES
        self.serve_text = self.font.render(self.serve_string, True, GAME_FONT)
        self.play_again_text = self.font.render(self.play_again_string, True, GAME_FONT)


        # CREATES FONT POSITIONS
        self.serve_text_pos = [500 - (self.font.size(self.serve_string)[0]/2), 100]

        self.player_goal_pos = {
        '1': [(Window.width/2) - self.font.size('PLAYER1 GOAL!')[0] - 40 , 30],
        '2': [(Window.width/2) + 40, 30]
        }

        self.player_serve_pos = {
        '1': [(Window.width/2) - self.font.size('PRESS TAB')[0] - 40, 30],
        '2': [(Window.width/2) + 40, 30]
        }



    # DISPLAYS PLAYERS CURRENT SCORES
    def score(self):

        # DISPLAYS PLAYER SCORES
        self.score_text1 = self.score_font.render(str(Globals.player_score['1']), True, \
            NEON_BLUE)
        self.score_text2 = self.score_font.render(str(Globals.player_score['2']), True, \
            NEON_RED)

        Window.screen.blit(self.score_text1, [20, 30])
        Window.screen.blit(self.score_text2, \
            [980 - self.score_font.size(str(Globals.player_score['2']))[0], 30])


        # GAME ENDS IF SCORE LIMIT IS REACHED
        for i in Globals.player_score:
            if Globals.player_score[i] == Globals.score_limit:
                
                # FINDS PLAYER THAT SCORED LESS
                for i in Globals.player_score:
                    if Globals.player_score[i] < Globals.score_limit:
                        
                        Globals.loser = i
                        self.loser_string = 'PLAYER' + str(Globals.loser) + ' LOST!'
                        self.loser_text = self.loser_font.render((self.loser_string), True, GAME_FONT)

                Globals.GAME_OVER = True

                # MAKES PLAYER SERVE VARIABLES FALSE
                for x in Globals.player_serve:
                    Globals.player_serve[x] = False




    # SERVE BALL
    def serve(self):

        # SERVES BALL AT START OF GAME
        if Globals.new_game:

            # SERVES BALL FOR GAME
            Window.screen.blit(self.serve_text, self.serve_text_pos)
            pygame.display.update()



        # GIVES COUNTDOWN AT START OF GAME
        if Globals.start_game:
            while Globals.countdown > 0:
                Window.screen.fill(BLACK)
                Sprites.animate()
                countdown_text = self.countdown_font.render(str(Globals.countdown), \
                    True, GAME_FONT)

                Window.screen.blit(countdown_text, \
                    [ 500 - (self.countdown_font.size(str(Globals.countdown))[0] / 2), \
                    300 - (self.countdown_font.size(str(Globals.countdown))[1] / 2) ])

                pygame.display.update()
                pygame.time.delay(1000)

                # SUBTRACTS 1 SECOND FROM COUNTDOWN VARIABLE
                Globals.countdown -= 1

                # FADES IN MUSIC (CRAPPY)
                Globals.vol += 0.05
                
                pygame.mixer.music.set_volume(Globals.vol)
                

            Globals.start_game = False
            Globals.new_game = False



        # TELLS PLAYER WHAT BUTTON TO PRESS FOR SERVE
        if Globals.player_serve['1'] == True or Globals.player_serve['2'] == True:

            # BUTTON CHANGES DEPENDING ON WHO SERVES
            if Globals.player_serve['1'] == True:
                pos = '1'
                serve_text = self.font.render('PRESS TAB', True, NEON_BLUE)

            elif Globals.player_serve['2'] == True:
                pos = '2'
                serve_text = self.font.render('PRESS ENTER', True, NEON_RED)

            Window.screen.fill(BLACK)
            Sprites.animate()
            self.score()


            Window.screen.blit(serve_text, self.player_serve_pos[pos])
            pygame.display.update()





    # DISPLAYS WHO SCORED
    def playerGoal(self, player, color, pos):
        scoreGoal_string = 'PLAYER' + str(player) + ' GOAL!'

        # DISPLAYS WHICH PLAYERED SCORED
        if Globals.goal:
            scoreGoal = self.font.render((scoreGoal_string), True, color)
            Window.screen.blit(scoreGoal, pos)

            self.score()

            pygame.display.update()

            pygame.time.delay(2000)




Text = Fonts()




class GameClass:

    def __init__(self):
        
        # INITIALIZES PYGAME MODULES
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()
        pygame.display.set_caption('Pong')

        # LOAD SOUND FILES
        self.hit_paddle = pygame.mixer.Sound('sounds/hit_paddle.wav')
        self.punch = pygame.mixer.Sound('sounds/punch.wav')
        self.score_goal = pygame.mixer.Sound('sounds/score goal.wav')

        # SET SOUND VOLUMES
        self.hit_paddle.set_volume(0.4)
        self.punch.set_volume(0.4)
        self.score_goal.set_volume(0.4)


        self.gameOver_music = False
        

    def events(self):

        # EVENT LOOP
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                Globals.running = False


            elif e.type == pygame.KEYDOWN:


                if e.key == pygame.K_ESCAPE:
                    # QUITS GAME
                    Globals.running = False



                if Globals.player_serve == {'1': False, '2': False}:
                    if e.key == pygame.K_SPACE:
                        if Globals.GAME_OVER:
                            # STARTS NEW GAME
                            pygame.mixer.music.fadeout(150)
                            self.new_game()

                        elif Globals.new_game:
                            # SERVES BALL AT BEGINNING OF GAME
                            Game.play_music('sounds/bg_music.mp3', Globals.vol)
                            Globals.start_game = True
                            Globals.play = True


                # IF PLAYER 1 IS SERVING, CHECK FOR INPUT
                if Globals.player_serve['1'] == True:
                    if e.key == pygame.K_TAB:

                        # PLAYER 1 SERVES
                        Globals.play = True
                        Globals.player_serve['1'] = False

                # IF PLAYER 2 IS SERVING, CHECK FOR INPUT
                elif Globals.player_serve['2'] == True:
                    if e.key == pygame.K_RETURN:

                        # PLAYER 2 SERVES
                        Globals.play = True
                        Globals.player_serve['2'] = False



                # MOVES RIGHT PADDLE
                if e.key == pygame.K_UP:
                    Objects.paddleR.speedUP = -Objects.paddle_speed
                if e.key == pygame.K_DOWN:
                    Objects.paddleR.speedDOWN = Objects.paddle_speed

                # MOVES LEFT PADDLE
                if e.key == pygame.K_w:
                    Objects.paddleL.speedUP = -Objects.paddle_speed
                if e.key == pygame.K_s:
                    Objects.paddleL.speedDOWN = Objects.paddle_speed
                            

            elif e.type == pygame.KEYUP:
                # STOPS MOVING PADDLE(S)
                if e.key == pygame.K_UP:
                    Objects.paddleR.speedUP = 0
                elif e.key == pygame.K_DOWN:
                    Objects.paddleR.speedDOWN = 0

                elif e.key == pygame.K_w:
                    Objects.paddleL.speedUP = 0
                elif e.key == pygame.K_s:
                    Objects.paddleL.speedDOWN = 0


        if not Globals.new_game and not Globals.GAME_OVER:
            if Globals.upL:
                Objects.paddleL.rect.top += Objects.paddleL.speedUP
            if Globals.downL:
                Objects.paddleL.rect.bottom += Objects.paddleL.speedDOWN

            if Globals.upR:
                Objects.paddleR.rect.top += Objects.paddleR.speedUP
            if Globals.downR:
                Objects.paddleR.rect.bottom += Objects.paddleR.speedDOWN
        


    def gameOver(self):

        # PLAYS GAME OVER MUSIC
        if not self.gameOver_music:
            pygame.mixer.music.fadeout(100)
            self.play_music('sounds/Pong game_over.mp3', 1.0)
            self.gameOver_music = True

        
        # DISPLAYS GAME OVER SCREEN
        Window.screen.fill(BLACK)
        
        Window.screen.blit(Text.loser_text, \
            [500 - (Text.loser_font.size(Text.loser_string)[0] / 2), 150])

        Window.screen.blit(Text.play_again_text, \
            [500 - (Text.font.size(Text.play_again_string)[0] / 2), 400])

        

        # UPDATES DISPLAY TO SHOW TEXT
        pygame.display.update()


    def new_game(self):

        # RESETS EVERYTHING FOR A NEW GAME
        Objects.ball.location = Objects.ball.center
        Objects.ball.speed[0] = Objects.ball_speedX
        Objects.ball.speed[1] = Objects.ball_speedY

        # RESETS SPRITE POSITIONS
        Sprites.reset_sprites(0)

        # RESETS VARIABLES
        self.gameOver_music = False
        Globals.vol = 0
        Globals.countdown = 3
        Globals.play = False
        Globals.start_game = False
        Globals.new_game = True
        Globals.GAME_OVER = False

        # RESETS PLAYERS' SCORES
        for i in Globals.player_score:
            Globals.player_score[i] = 0



    def play_music(self, track, vol):

        # PLAY MUSIC IN GAME
        pygame.mixer.music.load(track)
        pygame.mixer.music.set_volume(vol)
        pygame.mixer.music.play(-1)





Game = GameClass()




def GameLoop():
    # GAME LOOP

    # CHECKS FOR ANY KEY INPUT AND
    # EXECUTES ACCORDINGLY
    Game.events()

    if not Globals.GAME_OVER:

        # FILLS BACKGROUND WITH BLACK
        Window.screen.fill(BLACK)

        # ANIMATES ALL OBJECTS ON SCREEN
        Sprites.animate()

        # CHECKS FOR COLLISIONS BETWEEN PADDLES AND BALL
        Sprites.collision()

        # DISPLAYS PLAYERS' SCORES
        Text.score()


        if Globals.countdown > 0 or Globals.player_serve['1'] == True or Globals.player_serve['2'] == True:
            Text.serve()


    if Globals.GAME_OVER:
        # DISPLAYS GAME OVER SCREEN
        Game.gameOver()

        


# MODULE FOR CONTROLLING FRAME RATE
clock = pygame.time.Clock()



# STARTS GAME LOOP
while Globals.running:

    # STARTS GAME LOOP
    GameLoop()


    # UPDATE PYGAME DISPLAY
    pygame.display.update()

    # CONTROL FPS
    clock.tick(Globals.fps)


# QUITS PYGAME
pygame.quit()

