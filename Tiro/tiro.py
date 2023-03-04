# Importando os módulos necessários
import pygame
import random

# Inicializando o Pygame
pygame.init()

# Definindo as dimensões da janela
largura_tela = 800
altura_tela = 600

# Criando a janela
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Jogo de Tiro")

# Definindo as cores
preto = (0, 0, 0)
branco = (255, 255, 255)

# Função para exibir o menu inicial
def menu_inicial():
    # Definindo a fonte para exibir o texto do menu
    fonte_menu = pygame.font.Font(None, 48)

    # Exibindo o texto do menu
    texto_titulo = fonte_menu.render("Jogo de Tiro Levy", True, preto)
    texto_instrucoes = fonte.render("Pressione qualquer tecla para começar", True, preto)
    tela.blit(texto_titulo, (largura_tela/2 - texto_titulo.get_width()/2, altura_tela/2 - texto_titulo.get_height()))
    tela.blit(texto_instrucoes, (largura_tela/2 - texto_instrucoes.get_width()/2, altura_tela/2))

    # Atualizando a tela
    pygame.display.update()

# Criando a classe jogador
class Jogador(pygame.sprite.Sprite):
    def __init__(self, imagem_jogador, posicao_inicial):
        super().__init__()
        self.image = imagem_jogador
        self.rect = self.image.get_rect()
        self.rect.width = 50
        self.rect.height = 50
        self.rect.x = posicao_inicial[0]
        self.rect.y = posicao_inicial[1]
        self.vel_x = 0

    def update(self):
        self.rect.x += self.vel_x
        if self.rect.right > largura_tela:
            self.rect.right = largura_tela
        if self.rect.left < 0:
            self.rect.left = 0

    def mover(self, vel):
        self.vel_x = vel



# Criando a classe inimigo
class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(preto)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, largura_tela - self.rect.width)
        self.rect.y = random.randint(-100, -50)
        self.vel_y = random.randint(1, 5)

    def update(self):
        self.rect.y += self.vel_y
        if self.rect.top > altura_tela:
            self.rect.x = random.randint(0, largura_tela - self.rect.width)
            self.rect.y = random.randint(-100, -50)
            self.vel_y = random.randint(1, 5)

# Criando a classe bala
class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([5, 10])
        self.image.fill(preto)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = -10

    def update(self):
        self.rect.y += self.vel_y
        if self.rect.bottom < 0:
            self.kill()

# Criando o grupo de sprites
todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
balas = pygame.sprite.Group()

# Carregando a imagem do jogador
imagem_jogador = pygame.image.load("C:/Users/levyg/OneDrive/Área de Trabalho/py/Tiro/imagem_jogador.png").convert_alpha()

# Definindo a posição inicial do jogador
posicao_inicial = (largura_tela / 2, altura_tela - imagem_jogador.get_height() - 10)

# Criando o jogador
jogador = Jogador(imagem_jogador, posicao_inicial)

# Adicionando o jogador ao grupo de sprites
todos_sprites.add(jogador)


# Criando os inimigos
for i in range(10):
    inimigo = Inimigo()
    todos_sprites.add(inimigo)
    inimigos.add(inimigo)

# Definindo a fonte para exibir a pontuação
fonte = pygame.font.Font(None, 36)

# Definindo a pontuação inicial
pontuacao = 0

# Loop principal do jogo
while True:
    
    # Tratando os eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jogador.mover(-5)
            if evento.key == pygame.K_RIGHT:
                jogador.mover(5)
            if evento.key == pygame.K_SPACE:
                bala = Bala(jogador.rect.centerx, jogador.rect.top)
                todos_sprites.add(bala)
                balas.add(bala)

    # Atualizando os sprites
    todos_sprites.update()

    # Verificando a colisão entre a bala e o inimigo
    grupo_inimigos = pygame.sprite.Group()
    grupo_inimigos.add(inimigo)
    colisao = pygame.sprite.groupcollide(balas, grupo_inimigos, True, True)
    for bala, inimigos in colisao.items():
        pontuacao += 10

    # Verificando a colisão entre o jogador e o inimigo
    colisao_jogador = pygame.sprite.spritecollide(jogador, grupo_inimigos, False)
    if colisao_jogador:
        pygame.quit()
        quit()

    # Desenhando os sprites na tela
    tela.fill(branco)
    todos_sprites.draw(tela)

    # Exibindo a pontuação na tela
    texto_pontuacao = fonte.render("Pontuação: {}".format(pontuacao), True, preto)
    tela.blit(texto_pontuacao, (10, 10))

    # Atualizando a tela
    pygame.display.update()

    # Definindo a taxa de quadros por segundo
    pygame.time.Clock().tick(60)

