import pygame

import colors
import config
from text import Text


class Controller:
    def __init__(self):
        self.text = Text(
            posx=0,
            posy=0,
            string="scartezini",
            color=colors.BLACK,
            font=config.font,
            size=26
        )

        self.welcome = {
            'string': "BEM-VINDO(A) À CASA!  PRESSIONE  'E' PARA ABRIR A PORTA",
            'tiles': [[1, 11], [1, 10],
                      [2, 10], [2, 11], [2, 12],
                      [3, 10], [3, 11], [3, 12],
                      [4, 10], [4, 11], [4, 12],
                      [5, 11]]
        }

        self.items1 = {
            'string': "PEGUE A ARMADURA E O KIT MÉDITO NO CHÃO",
            'tiles': [[2, 6], [3, 6], [4, 6],
                      [2, 7], [3, 7], [4, 7]]
        }

        self.arrow = {
            'string': "SIGA A SETA VERDE NO CANTO INFERIOR",
            'tiles': [[2, 5], [3, 5], [4, 5]]
        }

        self.exits = {
            'string': "PRESSIONE  'E' NA SAÍDA PARA FUGIR",
            'tiles': [[2, 1], [3, 1], [4, 1],
                      [2, 2], [3, 2], [4, 2]]
        }

        self.second = {
            'string': "VOCÊ PODE TER UMA ARMA PRIMÁRIA, SECONDÁRIA E UMA CORPO A CORPO",
            'tiles': [[2, 17], [3, 16], [3, 17], [3, 18],
                      [4, 16], [4, 17]]
        }

        self.weapons = {
            'string': "PEGE AS ARMAS E TROQUE COM '1, 2, 3'",
            'tiles': [[2, 12], [3, 12], [4, 12],
                      [1, 13], [2, 13], [3, 13], [4, 13], [5, 13],
                      [1, 14], [2, 14], [3, 14], [4, 14], [5, 14]]
        }

        self.ammo = {
            'string': "CADA ARMA TEM UM TIPO DE CARREGAMENTO.  CARREGUE COM  'R'",
            'tiles': [[2, 7], [3, 7], [4, 7],
                      [2, 8], [3, 8], [4, 8],
                      [2, 9], [3, 9], [4, 9]]
        }

        self.compare = {
            'string': "PARA MELHOR PRESIÇÃO,  BOTÃO DIREITO DO MOUSE",
            'tiles': [[2, 3], [4, 3],
                      [2, 4], [3, 4], [4, 4],
                      [2, 5], [3, 5], [4, 5]]
        }

        self.gauss = {
            'string': "ABRA O INVENTÁRIO COM 'I' ou 'Tab'",
            'tiles': [[3, 3]]
        }

        self.combat = {
            'string': "HORA DE CONHECER AS CRIATURAS DA CASA!",
            'tiles': [[2, 14], [3, 14],
                      [2, 15], [3, 15], [4, 15],
                      [2, 16], [3, 16], [4, 16], ]
        }

        self.items = {
            'string': "AS CRIATURAS TÊM COMPORTAMENTOS DIFERENTES.  AGORA, SE ARME!",
            'tiles': [[2, 10], [3, 10], [4, 10],
                      [2, 11], [3, 11], [4, 11],
                      [2, 12], [3, 12], [4, 12], ]
        }

        self.enemy = {
            'string': "MATE ELE!!  BOTÃO ESQUERDO PARA ATIRAR!",
            'tiles': [[2, 4], [3, 4], [4, 4], [5, 4],
                      [1, 5], [2, 5], [3, 5], [4, 5], [5, 5],
                      [1, 6], [2, 6], [3, 6], [4, 6], [5, 6],
                      [1, 7], [2, 7], [3, 7], [4, 7], [5, 7],
                      [1, 8], [2, 8], [3, 8], [4, 8], [5, 8], ]
        }

        self.done = {
            'string': "MUITO BEM! AGORA, VAMOS JOGAR!",
            'tiles': [[2, 1], [3, 1], [4, 4],
                      [3, 2], [4, 2], ]
        }

    def control(self, canvas):
        if config.current_level == 0:
            if config.player_map_pos in self.welcome['tiles']:
                self.draw(self.welcome, canvas)
            elif config.player_map_pos in self.items1['tiles']:
                self.draw(self.items1, canvas)
            elif config.player_map_pos in self.arrow['tiles']:
                self.draw(self.arrow, canvas)
            elif config.player_map_pos in self.exits['tiles']:
                self.draw(self.exits, canvas)
        elif config.current_level == 1:
            if config.player_map_pos in self.second['tiles']:
                self.draw(self.second, canvas)
            elif config.player_map_pos in self.weapons['tiles']:
                self.draw(self.weapons, canvas)
            elif config.player_map_pos in self.ammo['tiles']:
                self.draw(self.ammo, canvas)
            elif config.player_map_pos in self.compare['tiles']:
                self.draw(self.compare, canvas)
            elif config.player_map_pos in self.gauss['tiles']:
                self.draw(self.gauss, canvas)
        elif config.current_level == 2:
            if config.player_map_pos in self.combat['tiles']:
                self.draw(self.combat, canvas)
            elif config.player_map_pos in self.items['tiles']:
                self.draw(self.items, canvas)
            elif config.player_map_pos in self.enemy['tiles']:
                self.draw(self.enemy, canvas)
            elif config.player_map_pos in self.done['tiles']:
                self.draw(self.done, canvas)

    def draw(self, string, canvas):
        self.text.update_string(string['string'])
        self.text.update_pos((config.actual_width / 2) - (self.text.layout.get_width() / 2), 480)
        self.box = pygame.Surface((self.text.layout.get_width() + 6, self.text.layout.get_height() + 6)).convert_alpha()
        self.box.fill((255, 255, 255, 180))
        canvas.blit(self.box, (self.text.posx - 3, self.text.posy - 3))
        self.text.draw(canvas)
