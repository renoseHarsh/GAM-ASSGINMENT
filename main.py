import pygame
import random
from helper import Player, Button, Trap


class Jungle:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the screen
        self.screen_width = 800
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Jungle")

        # Load the image
        self.image = pygame.image.load("board.jpg")

        # Resize the image
        self.resized_image = pygame.transform.scale(self.image, (600, 600))
        self.font = pygame.font.Font(None, 32)
        self.players = [Player(1), Player(2), Player(3), Player(4)]
        self.traps = []
        self.trap_button = Button("Set Trap", (650, 300))

    def roll_die(self):
        return random.randint(1, 6)

    def draw_player_board(self):
        for player in self.players:
            diff = player.num**2
            adjest = player.position - 1
            player_x = (adjest % 10) * 60 + 20 + diff
            player_y = (adjest // 10) * 60 + 20 + diff
            pygame.draw.circle(self.screen, player.color, (player_x, player_y), 10)

        for trap in self.traps:
            adjest = trap.position - 1
            trap_x = (adjest % 10) * 60 + 5
            trap_y = (adjest // 10) * 60 + 5
            trap_image = pygame.image.load("trap.png")
            trap_image = pygame.transform.scale(trap_image, (20, 20))
            trap_rect = trap_image.get_rect(topleft=(trap_x, trap_y))
            self.screen.blit(trap_image, trap_rect)

    def display_text(self, text, position):
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=position)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def draw_players_name(self):
        font = pygame.font.Font(None, 36)
        for i, player in enumerate(self.players):
            text_surface = font.render(
                player.name + ": " + " (" + str(player.traps) + " traps)",
                True,
                player.color,
            )
            self.screen.blit(text_surface, (20, 620 + i * 20))
    
    def check_trap(self, num):
        for trap in self.traps:
            if (self.players[num].position == trap.position):
                self.players[num].trapped = True
                trapped_font = pygame.font.Font(None, 32)
                trapped_text_surface = trapped_font.render("TRAPPED", True, (255, 0, 0))
                self.screen.blit(trapped_text_surface, (700, 150))
                self.traps.remove(trap)


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.roll = self.roll_die()
                if self.turn == 4:
                    self.turn = 1
                else:
                    self.turn += 1
                self.status = self.players[self.turn - 1].move(self.roll)
                if (self.status == 'B'):
                    for i in range(len(self.players)):
                        if self.turn - 1 != i:
                            self.players[i].position = 1
                self.check_trap(self.turn - 1)
                if self.roll == 6:
                    for i in range(len(self.players)):
                        if self.turn - 1 != i:
                            self.players[i].move(-1)
                            self.check_trap(self.turn - 1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.trap_button.is_clicked(pygame.mouse.get_pos()):
                    self.traps.append(Trap(self.players[self.turn - 1].position))
                    self.players[self.turn - 1].traps -= 1

    def run(self):
        self.status = "C"
        self.running = True
        self.turn = 0
        self.roll = None
        while self.running:
            if self.status in ['1', '2', '3', '4']:
                font = pygame.font.Font(None, 64)
                text_surface = font.render(
                    f"Player {self.status} wins!", True, (255, 0, 0)
                )
                text_rect = text_surface.get_rect(center=(self.screen_width // 2, 400))
                self.screen.blit(text_surface, text_rect)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

            else:
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.resized_image, (0, 0))
                self.handle_events()
                if self.roll:
                    self.display_text(
                        f"Player:{self.turn}   rolled:{str(self.roll)}", (700, 100)
                    )
                    if self.players[self.turn - 1].trap_available():
                        self.trap_button.draw(self.screen)

                self.draw_players_name()
                self.draw_player_board()
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()


# Usage
if __name__ == "__main__":
    game = Jungle()
    game.run()

    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         running = False
    #     elif event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_SPACE:
    #             # Roll the die
    #             result = self.roll_die()
    #             if last_player:
    #                 pygame.draw.rect(self.screen, (255, 255, 255), last_player)
    #             last_player = self.display_text(
    #                 f"Player:{self.turn}   rolled:{str(result)}", (700, 100)
    #             )
    #             self.roll = result
    #             self.players[self.turn - 1].move(self.roll)
    #             if self.turn == 4:
    #                 self.turn = 1
    #             else:
    #                 self.turn += 1
