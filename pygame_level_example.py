import pygame, sys, random

class Crosshair(pygame.sprite.Sprite):
    def __init__(self,picture_path) -> None:
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.gunshot = pygame.mixer.Sound("/home/admin/Desktop/Python Projects/pygame sprite example/gunshot.wav")
    def shoot(self):
        global shots
        self.gunshot.set_volume(.5)
        self.gunshot.play()
        shots += 1
        pygame.sprite.spritecollide(crosshair,target_group,True)
    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Target(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x,pos_y) -> None:
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x,pos_y]

class GameState():
    def __init__(self) -> None:
        self.state = "intro"
    
    def intro(self):
        global start_time, high_score, high_score_text, score, shots
        # Input Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #crosshair.shoot()
                self.state = "main_game"
                start_time = pygame.time.get_ticks()
                shots = 0
            
        #checking for targets
        if not target_group:
            draw_targets()

        # Updating the Window
        screen.blit(background,(0,0))
        screen.blit(ready_text,(screen_width/2 - 200,screen_height/2 - 300))
        screen.blit(high_score_text,(screen_width/2 - 300,screen_height/2 - 100))
        screen.blit(lowest_shots_text,(screen_width/2 - 300,screen_height/2))
        crosshair_group.draw(screen)
        crosshair_group.update()
        pygame.display.flip()

    def main_game(self):
        global score, high_score, high_score_text, shots, lowest_shots, lowest_shots_text
        # Input Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                crosshair.shoot()
            
        #checking for targets
        if not target_group:
            game_state.state = "intro"
            if score < high_score:
                high_score = score
                high_score_text = title_font.render(f"High Score: {high_score} Seconds", False, (50,50,50))
            if shots < lowest_shots:
                lowest_shots = shots
                lowest_shots_text = title_font.render(f"Lowest Shots: {lowest_shots}", False, (50,50,50))

        # Updating the Window
        screen.blit(background,(0,0))
        target_group.draw(screen)
        score = display_score()
        
        crosshair_group.draw(screen)
        crosshair_group.update()
        pygame.display.flip()

    def state_manager(self):
        if self.state == "intro":
            self.intro()
        if self.state == "main_game":
            self.main_game()

def draw_targets():
    for target in range(20):
        new_target = Target("/home/admin/Desktop/Python Projects/pygame sprite example/target.png",random.randrange(0,screen_width),random.randrange(0,screen_height))
        target_group.add(new_target)

def display_score():
    current_time = (pygame.time.get_ticks() - start_time) /1000
    score_surface = test_font.render(f"{current_time}s",False,(text_color))
    score_rect = score_surface.get_rect(center = (screen_width/2, 50))
    screen.blit(score_surface,score_rect)
    return current_time

#General setup
pygame.init()
clock = pygame.time.Clock()
game_state = GameState()
title_font = pygame.font.Font("/home/admin/Desktop/Python Projects/Space J_mp (OOP rework)/font/Pixeltype.ttf", 100)
start_time = 0
score = 0
high_score = 1000
shots = 0
lowest_shots = 1000
test_font = pygame.font.Font("/home/admin/Desktop/Python Projects/Space J_mp (OOP rework)/font/Pixeltype.ttf", 50)
text_color = (64,64,64)

# Setting up main window
screen_width = 1920
screen_height = 1010
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Shoot the Targets")
background = pygame.transform.smoothscale(pygame.image.load("/home/admin/Desktop/Python Projects/pygame sprite example/BG.png"),(screen_width,screen_height))
ready_text = title_font.render("Ready to Play?", False, (50,50,50))
high_score_text = title_font.render(f"High Score: {0} Seconds", False, (50,50,50))
lowest_shots_text = title_font.render(f"Lowest Shots: {0}", False, (50,50,50))
pygame.mouse.set_visible(False)

# Crosshair
crosshair = Crosshair("/home/admin/Desktop/Python Projects/pygame sprite example/crosshair.png")
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

# Target
target_group = pygame.sprite.Group()
draw_targets()

while True:
    game_state.state_manager()
    clock.tick(60)
