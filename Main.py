import pygame,sys
from Interactive_Bar import Click_color
class Paint_game:
    def __init__(self):
        pygame.init()

        self.screen_w = 1500
        self.screen_h = 800
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        pygame.display.set_caption('Paint it')

        self.rectangles = {}

        self.rect_width = 10
        self.rect_height = 10

        self.prev_size = [10,10]

        self.index_color  = 0
        self.num = 0
        self.colors = ["Black",'Red','Green',"Blue","Gray",
                       "Yellow","Pink","Brown","Purple",(230,230,230)]
        
        self.handle_size_speed = 3.5

        self.color_click = Click_color(self)
        self.counter = 0
        self.mouse_pos = ()

        self.is_showin_li = False
        self.is_savin  =False

        self.show_pointer = True

        self.clock = pygame.time.Clock()

        
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            self.kd(event)   
            self.color_click.s2_click(event,self.mouse_pos)     

# Keydown.
    def kd(self,event):
        if event.type == pygame.KEYDOWN:    
            # Change colors by keys
            if event.key == pygame.K_e and self.index_color < len(self.colors) - 2:
                self.index_color += 1

            elif event.key == pygame.K_q and self.index_color > 0:
                self.index_color -= 1 

            elif event.key == pygame.K_w :
                self.erase = not getattr(self, 'erase' , False)  # A way to turn on/off the eraser 
                                #   A way to check if an attribute exists or return False/True.
                if self.erase:
                    self.num = self.index_color   # >> How to save a value before switching
                    self.index_color = len(self.colors) - 1
                else:
                    self.index_color = self.num
            else:
                if event.key == pygame.K_q :
                   self.index_color = len(self.colors) -2
                elif event.key == pygame.K_e:
                   self.index_color = 0
            
            # Decrease/ Increment Size Changing's Speed
            if event.key == pygame.K_z:
                self.handle_size_speed += 5
            elif event.key == pygame.K_x:
                self.handle_size_speed -= 3

            # Saving and Displaying Image
            if event.key == pygame.K_s:
                self.show_pointer = False
                self.is_savin = True
                pygame.image.save(self.screen, 'last_image.png')
                self.counter = 50

            elif event.key == pygame.K_d:    
                try:
                    self.l_image = pygame.image.load('last_image.png')
                    self.is_showin_li = not self.is_showin_li
                    self.counter2 = 70
                except FileNotFoundError:
                    self.counter2 = 50
                    self.nothing_saved = True

    def add_rect(self,mouse_pos):
        if 0 <mouse_pos[0] < self.screen_w and 0 < mouse_pos[1] < self.screen_h:# ensure not to draw out_of_sight rect
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0]:
                self.rectangles[(mouse_pos[0] - self.rect_width//2, mouse_pos[1] - self.rect_height//2 ,
                                 self.rect_width,self.rect_height)] = self.colors[self.index_color]
# CHANGE SIZE 
    def old_prev(self):
        if not self.is_showin_li:
            self.prev_size.clear()
            self.prev_size.extend([self.rect_width,self.rect_height])

    def handle_size(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if self.rect_height + self.handle_size_speed < self.screen_h :
                self.rect_height += self.handle_size_speed
                self.old_prev()
                
        elif keys[pygame.K_DOWN]:
            if self.rect_height - self.handle_size_speed > 4:
                self.rect_height -= self.handle_size_speed 
                self.old_prev()

        if keys[pygame.K_RIGHT]:
            if self.rect_width + self.handle_size_speed < self.screen_w:
                self.rect_width += self.handle_size_speed
                self.old_prev()

        elif keys[pygame.K_LEFT]:
            if self.rect_width - self.handle_size_speed > 4:
                self.rect_width -= self.handle_size_speed         
                self.old_prev()

# Pointer invisible
    def invi_pointer(self):
        if 0 < self.mouse_pos[1] < self.color_click.surface.get_rect().h + 5 and self.color_click.display_color == True:
            self.show_pointer = False
        elif self.mouse_pos[0] >= self.color_click.surface2_rect.x - 2 and self.mouse_pos[1] <= self.color_click.surface2_rect.y + self.color_click.surface2_rect.h +2: 
            self.show_pointer = False
        elif self.is_showin_li:
            self.show_pointer = False
        else:
            self.show_pointer = True
# Ur pic content
    def ur_pic(self):
        if self.counter2 > 0:
            mess = self.color_click.font.render('This Is Your Last Saved Drawing ',True,(199, 56, 56))
            rect_mess = mess.get_rect(midtop = (self.screen.get_rect().midtop[0],
                                                self.screen.get_rect().midtop[1]+ 10))
            self.screen.blit(mess,rect_mess)
            self.counter2 -= 1

    def run_game(self):
        while True:
            self.screen.fill((230,230,230))

            self.handle_size()
            
            # Drawing all rectangles
            for rectangle in self.rectangles.keys():
                rect = pygame.Rect(*rectangle) # actually don't need this(just to show)
                pygame.draw.rect(self.screen,self.rectangles[rectangle],rect) # rectangle directly is ok     

            self.mouse_pos = pygame.mouse.get_pos()
            
            self.check_events()
            
            self.invi_pointer()
            if self.show_pointer:
               pygame.draw.rect(self.screen,self.colors[self.index_color],(self.mouse_pos[0] - self.rect_width//2,
                                                                            self.mouse_pos[1] - self.rect_height//2,
                                                                            self.rect_width,self.rect_height))
               self.add_rect(self.mouse_pos)
               
            self.rect_width,self.rect_height  = self.prev_size[0],self.prev_size[1]
            
        
            if self.color_click.display_color :
                self.color_click.show_s1(self)
                self.color_click.change_color(self,self.mouse_pos)
            self.color_click.show_s2(self)
            

            # Saved successfully
            if self.is_savin:
                if self.counter > 0:
                    save_su = pygame.Surface((self.color_click.surface2_rect[2],
                                            self.color_click.surface2_rect[3]))
                    save_su.fill((191,216,211))

                    save_message = self.color_click.font.render('S',True,(0,0,0))
                    save_rect = save_message.get_rect(center = save_su.get_rect().center)#>pygame.Rect(x,y,w,h)
                    #> with x,y = center of s2, w,h = save_message
                    save_su.blit(save_message,save_rect)

                    self.screen.blit(save_su,self.color_click.surface2_rect)

                    self.counter -=1

                
            # Showing the last saved image
            if self.is_showin_li:
                self.color_click.display_color = False
                self.screen.blit(self.l_image,(0,0))            
                self.ur_pic()

            # No image saved situation
            if getattr(self,'nothing_saved',False) and self.counter2 > 0:
                no_s = self.color_click.font.render("You Haven't Saved Anything!", True, (230,0,0))
                pos = no_s.get_rect(center=self.screen.get_rect().center)
                self.screen.blit(no_s, pos)
                self.counter2 -= 1
            
            
            self.clock.tick(60)
            pygame.display.update()

if __name__ == "__main__" :
    paint_game = Paint_game()
    paint_game.run_game()



