import random
import pygame

# Screen dimensions
Screenwide = 1000
Screenheight = 666

# Flag to track reset button hover state
reset_button_hovered = False

sound = True
sound_effect = None
hight_score = None

#region Asteroid Class
class Asteroid:
    def __init__(self):
        # Initialize asteroid properties randomly
        self.skin = random.randint(1, 5)
        self.rotate = random.randint(0, 359)
        self.start = random.randint(37, Screenheight-37)
        self.end = random.randint(37, Screenheight-37)
        self.speed = random.uniform(0.3, 0.7)
        self.direction = random.choice([-1, 1])
        self.x = Screenwide-57
        self.y = self.start

    # Getter and setter methods for asteroid properties
    def getSkin(self):
        return self.skin

    def setSkin(self, value):
        self.skin = value

    def getRotate(self):
        return self.rotate

    def setRotate(self, value):
        self.rotate = value

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def getSpeed(self):
        return self.speed

    def getDirection(self):
        return self.direction

    def getX(self):
        return self.x

    def setX(self, value):
        self.x = value

    def getY(self):
        return self.y

    def setY(self, value):
        self.y = value

    def update_rotation(self):
        # Update asteroid rotation based on speed and direction
        self.rotate += self.speed * self.direction

def create_new_asteroid():
    # Create a new instance of the Asteroid class
    return Asteroid()
#endregion Class Asteroid

#region Score Handling
def load_score():
    try:
        # Load the score from a file
        with open("score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_score(score):
    # Save the score to a file
    with open("score.txt", "w") as file:
        file.write(str(score))
#endregion Score Handeling

# Initialize pygame
pygame.init()

# Initialize game window
ecran = pygame.display.set_mode((Screenwide, Screenheight))

# Load images
logo = pygame.image.load("./assets/Asteroid/Asteroid1.png").convert_alpha()
CrosshairImg = pygame.image.load("./assets/Target.png").convert_alpha()
background = pygame.image.load("./assets/Background.png").convert()
background_overlay = pygame.image.load("./assets/Background_Overlay.png").convert()
ExplosionImg = pygame.image.load("./assets/Explosion.png").convert_alpha()
soundImg = pygame.image.load("./assets/Sound_On.png").convert_alpha()

#SoundImg Resize
scaled_width = int(soundImg.get_width() * 0.07)
scaled_height = int(soundImg.get_height() * 0.07)
soundImg = pygame.transform.scale(soundImg, (scaled_width, scaled_height))
soundImg_rect = soundImg.get_rect()
soundImg_rect.topleft = (Screenwide-110, Screenheight-35)

#region Game Setup
# Set up game window properties
pos_Crosshair = (Screenwide // 2, Screenheight // 2)
pygame.display.set_icon(logo)
pygame.display.set_caption("Asteroid Shooter")
pygame.mouse.set_visible(False)

# Initialize game variables
continuer = True
game_active = True
asteroid_list = [create_new_asteroid()]
destruction_counter = 0
font = pygame.font.Font(None, 36)
rect_rotated = pygame.transform.rotate(pygame.image.load("./assets/Asteroid/Asteroid1.png").convert_alpha(), 0).get_rect(center=(0, 0))

start_time = pygame.time.get_ticks()
game_duration = 15 * 1000
#endregion Game Setup

#region Explosion Animation
def display_explosion(pos, ecran):
    explosion_scale = 1.0
    explosion_duration = 100

    ExplosionTime = pygame.time.get_ticks()
    explosion_rect = None

    while pygame.time.get_ticks() - ExplosionTime < explosion_duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Calculate the scaling factor based on time
        explosion_scale = min(explosion_scale + 0.08, 2.0)  # Increase scale gradually, up to a maximum of 2

        # Resize the explosion image
        explosion_scaled = pygame.transform.scale(ExplosionImg, (int(ExplosionImg.get_width() * explosion_scale), int(ExplosionImg.get_height() * explosion_scale)))

        # Calculate the position for centering
        explosion_rect = explosion_scaled.get_rect(center=pos)

        # Draw the explosion on a transparent surface
        explosion_surface = pygame.Surface((Screenwide, Screenheight), pygame.SRCALPHA)
        explosion_surface.blit(explosion_scaled, explosion_rect.topleft)

        #Show other asteroids
        for asteroid in asteroid_list:
            AsteroidImglien = "./assets/Asteroid/Asteroid" + str(asteroid.getSkin()) + ".png"
            AsteroidImg = pygame.image.load(AsteroidImglien).convert_alpha()
            image_rotated = pygame.transform.rotate(AsteroidImg, asteroid.getRotate())
            rect_rotated = image_rotated.get_rect(center=(asteroid.getX(), asteroid.getY()))
            ecran.blit(image_rotated, rect_rotated.topleft)
        # Draw lines from the lower corners to the center of the target with a 1-pixel black border
        pygame.draw.line(ecran, (0, 0, 0), (57, Screenheight-37), pos_Crosshair, 14)
        pygame.draw.line(ecran, (0, 0, 0), (Screenwide-57, Screenheight-37), pos_Crosshair, 14)

        pygame.draw.line(ecran, (35, 109, 73), (57, Screenheight-37), pos_Crosshair, 10)
        pygame.draw.line(ecran, (35, 109, 73), (Screenwide-57, Screenheight-37), pos_Crosshair, 10)

        # Blit the explosion surface on the main screen
        ecran.blit(explosion_surface, (0, 0))
        ecran.blit(CrosshairImg, (pos_Crosshair[0] - CrosshairImg.get_width() / 2, pos_Crosshair[1] - CrosshairImg.get_height() / 2))
        ecran.blit(background_overlay, (0, 0))
        ecran.blit(soundImg, soundImg_rect.topleft)
        ecran.blit(counter_text, (70, 5))
        ecran.blit(timer_text, (Screenwide-250, 5))

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        pygame.time.delay(30)
    return explosion_rect
#endregion Explosion Animation

while continuer:
    #region Game Loop
    while game_active:
        # Game logic for active game
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        remaining_time = max(0, (game_duration - elapsed_time) // 1000)
        nbr_asteroid = 1

        if elapsed_time >= game_duration:
            game_active = False

        ecran.fill((0, 0, 0))
        ecran.blit(background, (0, 0))

        # Event handling for active game
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                pos_Crosshair = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                for asteroid in asteroid_list:
                    AsteroidImglien = "./assets/Asteroid/Asteroid" + str(asteroid.getSkin()) + ".png"
                    AsteroidImg = pygame.image.load(AsteroidImglien).convert_alpha()
                    image_rotated = pygame.transform.rotate(AsteroidImg, asteroid.getRotate())
                    rect_rotated = image_rotated.get_rect(center=(asteroid.getX(), asteroid.getY()))

                    # Check if the click is inside the bounding rectangle of the rotated asteroid image
                    if rect_rotated.collidepoint(event.pos):
                        # Handle asteroid destruction for the clicked asteroid
                        asteroid_list.remove(asteroid)
                        asteroid_list.append(create_new_asteroid())
                        destruction_counter += 1
                        game_duration += 500

                        if sound:
                            sound_effect = pygame.mixer.Sound("./assets/sound/Explosion.mp3")
                            sound_effect.play()

                        AsteroidImglien = "./assets/ExplosionAsteroid/ExplosionAsteroid" + str(asteroid.getSkin()) + ".png"
                        AsteroidImg = pygame.image.load(AsteroidImglien).convert_alpha()
                        image_rotated = pygame.transform.rotate(AsteroidImg, asteroid.getRotate())
                        rect_rotated = image_rotated.get_rect(center=(asteroid.getX(), asteroid.getY()))
                        ecran.blit(image_rotated, rect_rotated.topleft)
                        explosion_rect = display_explosion(event.pos, ecran)
                        value = [1, 2, 3]
                        proba = [0.6, 0.3, 0.1]
                        random.choices(value, weights=proba)[0]

                        for asteroid in asteroid_list:
                            asteroid.speed += 0.07

                if soundImg_rect.collidepoint(event.pos):
                    if not sound:
                        sound_effect = pygame.mixer.Sound("./assets/sound/Missed.mp3")
                        sound_effect.play()
                else:
                    if sound:
                        sound_effect = pygame.mixer.Sound("./assets/sound/Missed.mp3")
                        sound_effect.play()
            if event.type == pygame.MOUSEBUTTONDOWN and soundImg_rect.collidepoint(event.pos):
                if sound :
                    sound = False
                    soundImg = pygame.image.load("./assets/Sound_Off.png").convert_alpha()
                else :
                    sound = True
                    soundImg = pygame.image.load("./assets/Sound_On.png").convert_alpha()
                scaled_width = int(soundImg.get_width() * 0.07)
                scaled_height = int(soundImg.get_height() * 0.07)
                soundImg = pygame.transform.scale(soundImg, (scaled_width, scaled_height))
                soundImg_rect = soundImg.get_rect()
                soundImg_rect.topleft = (Screenwide-110, Screenheight-35)
            if event.type == pygame.QUIT:
                continuer = False
                game_active = False

        # Update and draw asteroids
        for asteroid in asteroid_list:
            AsteroidImglien = "./assets/Asteroid/Asteroid" + str(asteroid.getSkin()) + ".png"
            AsteroidImg = pygame.image.load(AsteroidImglien).convert_alpha()

            image_rotated = pygame.transform.rotate(AsteroidImg, asteroid.getRotate())
            rect_rotated = image_rotated.get_rect(center=(asteroid.getX(), asteroid.getY()))
            ecran.blit(image_rotated, rect_rotated.topleft)

            asteroid.setX(asteroid.getX() - asteroid.getSpeed())
            asteroid.update_rotation()

            if asteroid.getX() < 0 and rect_rotated.colliderect(ecran.get_rect()):
                asteroid_list.remove(asteroid)
                asteroid_list.append(create_new_asteroid())
                for asteroid in asteroid_list:
                    asteroid.speed += 0.01
            if len(asteroid_list) <= nbr_asteroid:
                asteroid_list.append(create_new_asteroid())

        # Draw UI elements
        counter_text = font.render(f'Destructions: {destruction_counter}', True, (255, 255, 255))
        timer_text = font.render(f'Time Left: {remaining_time}s', True, (255, 255, 255))

        pygame.draw.line(ecran, (0, 0, 0), (57, Screenheight-37), pos_Crosshair, 14)
        pygame.draw.line(ecran, (0, 0, 0), (Screenwide-57, Screenheight-37), pos_Crosshair, 14)

        pygame.draw.line(ecran, (35, 109, 73), (57, Screenheight-37), pos_Crosshair, 10)
        pygame.draw.line(ecran, (35, 109, 73), (Screenwide-57, Screenheight-37), pos_Crosshair, 10)

        ecran.blit(CrosshairImg, (pos_Crosshair[0] - CrosshairImg.get_width() / 2, pos_Crosshair[1] - CrosshairImg.get_height() / 2))
        ecran.blit(background_overlay, (0, 0))
        ecran.blit(soundImg, soundImg_rect.topleft)
        ecran.blit(counter_text, (70, 5))
        ecran.blit(timer_text, (Screenwide-250, 5))
        pygame.display.flip()
    #endregion Game Loop

    #region Game Over Screen
    # Fill the screen with a black color
    ecran.fill((0, 0, 0))

    # Display the background image
    ecran.blit(background, (0, 0))

    # Load and compare scores for display
    saved_score = load_score()
    if destruction_counter >= saved_score:
        save_score(destruction_counter)
        # Display new high score message in yellow
        score_text = font.render(f'New High Score: {destruction_counter}', True, pygame.Color('yellow'))
    else:
        # Display current score in white
        score_text = font.render(f'Score: {destruction_counter}', True, (255, 255, 255))
        hight_score = font.render(f'High Score: {saved_score}', True, pygame.Color('yellow'))

    # Render the reset button
    reset_button_text = font.render('Reset Score', True, (255, 255, 255))
    reset_button_rect = pygame.Rect(Screenwide-250, 5, reset_button_text.get_width(), reset_button_text.get_height())
    pygame.draw.rect(ecran, (255, 0, 0), reset_button_rect)

    # Draw lines to frame the screen
    pygame.draw.line(ecran, (0, 0, 0), (57, Screenheight-37), pos_Crosshair, 14)
    pygame.draw.line(ecran, (0, 0, 0), (Screenwide-57, Screenheight-37), pos_Crosshair, 14)

    # Draw green overlay lines for style
    pygame.draw.line(ecran, (35, 109, 73), (57, Screenheight-37), pos_Crosshair, 10)
    pygame.draw.line(ecran, (35, 109, 73), (Screenwide-57, Screenheight-37), pos_Crosshair, 10)

    # Event handling for the Game Over Screen
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            pos_Crosshair = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN and reset_button_rect.collidepoint(event.pos):
            # Reset the score and exit the game if the reset button is clicked
            if sound :
                sound_effect = pygame.mixer.Sound("./assets/sound/Explosion.mp3")
                sound_effect.play()
            pygame.time.delay(int(sound_effect.get_length() * 1000))
            save_score(0)
            continuer = False
        if event.type == pygame.QUIT:
            # Exit the game if the window is closed
            continuer = False
            game_active = False
        # Change the hover state of the reset button
        reset_button_hovered = reset_button_rect.collidepoint(pygame.mouse.get_pos())

    # Draw important UI elements
    ecran.blit(CrosshairImg, (pos_Crosshair[0] - CrosshairImg.get_width() / 2, pos_Crosshair[1] - CrosshairImg.get_height() / 2))
    ecran.blit(background_overlay, (0, 0))
    ecran.blit(score_text, (70, 5))
    if destruction_counter < saved_score:
        ecran.blit(hight_score, (220, 5))
    reset_button_text_rect = reset_button_text.get_rect(topleft=(Screenwide-250, 5))
    # Highlight the reset button if hovered
    if reset_button_hovered:
        pygame.draw.rect(ecran, (255, 255, 0), reset_button_text_rect.inflate(6, 6))
        reset_button_text = font.render('Reset Score', True, (0, 0, 0))
    ecran.blit(reset_button_text, (Screenwide-250, 5))
    pygame.display.flip()
    #endregion Game Over Screen

pygame.quit()
