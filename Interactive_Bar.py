import pygame
pygame.init()


class Click_color:
    def __init__(self,p_g):
        # fonts
        self.font = pygame.font.Font(None,30)
        self.font2 = pygame.font.Font(None,25)

        self.colors = p_g.colors    

        self.rotate = False

        self.y = 3
        self.x = 5
        self.distance = 10
        self.rects = []

        # surface1
        self.surface = pygame.Surface((p_g.screen_w,p_g.rect_height + 20),pygame.SRCALPHA)
        self.surface.fill((191,216,211,230))

        # blit each color's rect on the 1st surface
        for color in range(len(self.colors)):
            rect = pygame.Rect(self.x, self.y ,p_g.rect_width +6 ,p_g.rect_height +6)
            self.rects.append(rect)
            pygame.draw.rect(self.surface,(self.colors[color]),rect)
            self.x += p_g.rect_width+10 + self.distance 
        # blit keys on 1st surface
        self.content1 = f':|Q-W-E|{' '*40}| S: Save | D: Show the last image|{' '*30}|Z|X :Increment|Decrease Size Handling\'s Speed|'
        self.content1_s = self.font2.render(self.content1,True,(0,0,0))
        self.surface.blit(self.content1_s,(300,5))

        #surface 2
        self.surface2 = pygame.Surface((30,30))
        self.surface2_rect = self.surface2.get_rect(topright = (p_g.screen_w -1,0))
        #blit content on surface2 
        self.surface2.fill((191,216,211))  
        self.content2 = self.font.render('<',True,(0,0,0))
        self.content_pos  = self.content2.get_rect(center = self.surface2.get_rect().center)
        self.surface2.blit(self.content2,(self.content_pos))


        self.display_color = False
        # rotated surface 2 
        self.rotated_s2 = pygame.transform.rotate(self.surface2,90) 

# If surface 2 is clicked
    def s2_click(self,event,mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and self.surface2_rect.collidepoint(mouse_pos):
            self.display_color = not self.display_color
            if self.display_color:
                self.rotate = True
            else:
                self.rotate = False
# Displaying surface 2 and after it gets clicked
    def show_s2(self,p_g):
        if self.rotate ==  True:
            p_g.screen.blit(self.rotated_s2,self.surface2_rect)
        else:
            p_g.screen.blit(self.surface2,self.surface2_rect)
# Display surface 1            
    def show_s1(self,p_g):
        pos = self.surface.get_rect(midtop = p_g.screen.get_rect().midtop)
        p_g.screen.blit(self.surface,pos)
# When the color's rect gets clicked
    def change_color(self,p_g,mouse_pos):
        for index,rect in enumerate(self.rects):
            if pygame.mouse.get_pressed()[0] and rect.collidepoint(mouse_pos):
                p_g.index_color = index
    


    


