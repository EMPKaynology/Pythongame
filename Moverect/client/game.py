import pygame
from protocols import Protocols
from client import Client
import time

class RectGame:
    def __init__(self, client):

        self.client = client 
        client.start()

        self.font = None
        self.font_player = None
        self.input_box = pygame.Rect(100, 100, 400, 45)
        self.color_inactive = pygame.Color("lightskyblue3")
        self.color_active = pygame.Color("dodgerblue2")
        self.color = self.color_inactive
        self.vel = 10
        self.clock = pygame.time.Clock()

        self.text = ""
        self.done = False
        self.logged_in = False

    def handle_event(self, event):
        #print("Event handel")
        if not self.logged_in:
            #print("Client eingeloggt")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_box.collidepoint(event.pos):
                    self.color = self.color_active
                else:
                    self.color = self.color_inactive

            if event.type != pygame.KEYDOWN or self.color == self.color_inactive:
                return

            if event.key == pygame.K_RETURN:
                self.client.send(Protocols.Request.NICKNAME, self.text)
                self.client.nickname = self.text
                self.logged_in = True
                self.text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
        elif self.client.started:
            keys=pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.client.send(Protocols.Request.PLAYER_MOVEMENT, [-self.vel,0])
                #time.sleep(0.1)
            elif keys[pygame.K_RIGHT]:
                self.client.send(Protocols.Request.PLAYER_MOVEMENT, [self.vel,0])
                #time.sleep(0.1)
            elif keys[pygame.K_DOWN]:
                self.client.send(Protocols.Request.PLAYER_MOVEMENT, [0,self.vel])
                #time.sleep(0.1)
            elif keys[pygame.K_UP]:
                self.client.send(Protocols.Request.PLAYER_MOVEMENT, [0,-self.vel])
                #time.sleep(0.1)

    def draw_login(self, screen):
        prompt = 'Enter A Nickname'
        prompt_surface = self.font.render(prompt, 1, (0, 0, 0))
        screen.blit(prompt_surface, (100, 50))
        self.draw_input(screen)
        
    def draw_input(self, screen):
        pygame.draw.rect(screen, self.color, self.input_box, 2)
        txt_surface = self.font.render(self.text, 1, self.color)
        screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        self.input_box.w = max(100, txt_surface.get_width()+10)

    def draw_waiting(self, screen):
        text = 'Waiting to log in'
        text_surface = self.font.render(text, 1, (0, 0, 0))
        screen.blit(text_surface, (screen.get_width()/2 - text_surface.get_width()/2, screen.get_height()/2 - text_surface.get_height()/2))

    def draw_game(self, screen):
        text = 'Game screen'
        text_surface = self.font.render(text, 1, (0, 0, 0))
        screen.blit(text_surface, (screen.get_width()/2 - text_surface.get_width()/2, screen.get_height()/2 - text_surface.get_height()/2))

    def draw_game_2(self, screen):
        for player in self.client.players.keys():
            prompt_surface = self.font_player.render(player, 1, (0, 0, 0))
            screen.blit(prompt_surface, (self.client.players[player]["x"], self.client.players[player]["y"]-20))
            pygame.draw.rect(screen,(0,0,255),(self.client.players[player]["x"],self.client.players[player]["y"],20,20))
        #text = 'Game screen'
        #text_surface = self.font.render(text, 1, (0, 0, 0))
        #screen.blit(text_surface, (screen.get_width()/2 - text_surface.get_width()/2, screen.get_height()/2 - text_surface.get_height()/2))
    
    def draw(self, screen):
        screen.fill((255, 255, 255))
        if not self.logged_in and not self.client.started:
            self.draw_login(screen)
        elif not self.client.started:
            self.draw_waiting(screen)
        else:
            self.draw_game_2(screen)

        pygame.display.update()
    
    def run(self):
        #print(self.client.closed)
        pygame.init()
        #print(self.client.closed)
        screen = pygame.display.set_mode((800, 600))
        #print(self.client.closed)
        clock = pygame.time.Clock()
        #print(self.client.closed)
        #print("hi")
        self.font = pygame.font.SysFont("comicsans", 32)
        self.font_player = pygame.font.SysFont("comicsans", 16)
        #print(self.client.closed)

        while not self.client.closed:
            #pygame.time.delay(10)
            self.clock.tick(30)
            #print("hi")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.client.close()
                    pygame.quit()
                else:
                    self.handle_event(event)
            
            self.draw(screen)
        
        pygame.quit()

if __name__ == "__main__":
    game = RectGame(Client())
    game.run()

#pygame.init()
#
#pywindow = pygame.display.set_mode((800,500)) 
#
#pygame.display.set_caption("moving rect")
#
#x = 200
#y = 200
#
#width = 20
#height = 20
#
#vel = 10
#
#run = True
#
#while run:
#    pygame.time.delay(10)
#
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            run = False
#
#    keys = pygame.key.get_pressed()
#
#    if keys[pygame.K_LEFT] and x > 0:
#        x -= vel
#
#    if keys[pygame.K_RIGHT] and x < 800 - width:
#        x += vel
#
#    if keys[pygame.K_DOWN] and y < 500 - height:
#        y += vel
#
#    if keys[pygame.K_UP] and y > 0:
#        y -= vel
#
#    pywindow.fill((0,0,0))
#
#    pygame.draw.rect(pywindow,(0,0,255),(x,y,width,height))
#
#    pygame.display.update()
#
#pygame.quit()