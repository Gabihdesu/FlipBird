import pygame
import os # integrar codigo com arq do pc
import random

# configurações iniciais --------------------------

tela_largura = 500
tela_altura = 800

imagem_cano = pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'cano.png')))
imagem_chao = pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'base.png')))
imagem_background = pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'bg.png')))
imagens_passaro = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'bird3.png')))
]

pygame.font.init()
fonte_pontos = pygame.font.SysFont('arial', 50)

# objetos do jogo ------------------------------------

class Passaro:
    # atributos

    imgs = imagens_passaro
    # animações da rotação
    rotacao_maxima = 25 # 25 graus
    velocidade_rotacao = 20
    tempo_animacao = 5

    #metodos
    def __init__(self, x, y): # x e y é a posicao na tela
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.imgs[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0 # quando muda a posicao o novo tempo é zero
        self.altura = self.y

    def mover(self):
        # calcular o deslocamento usando a fórmula da física S = so + vot + at²/2
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo


        # restringir o deslocamento para no máximo 16 px
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        #angulo do passaro na hr que pula
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.rotacao_maxima:
                self.angulo = self.rotacao_maxima
        else:
            if self.angulo > -90: #se estiver caindo o angulo dele só pode ficar reto e n totalmente virado
                self.angulo -= self.velocidade_rotacao

    #colocar na classe passaro como ele é desenhado pq na func principal ele vai usar essa func
    def desenhar(self, tela):
        # definir qual img do passaro de 5 em 5 frames
        self.contagem_imagem += 1

        # nos primeiros 15 segundos a asa abaixa
        if self.contagem_imagem < self.tempo_animacao:
            self.imagem = self.imgs[0]
        elif self.contagem_imagem < self.tempo_animacao*2:
            self.imagem = self.imgs[1]
        elif self.contagem_imagem < self.tempo_animacao*3:
            self.imagem = self.imgs[2]
        # depois a asa sobe
        elif self.contagem_imagem < self.tempo_animacao*4:
            self.imagem = self.imgs[1]
        elif self.contagem_imagem >= self.tempo_animacao*4 + 1:
            self.imagem = self.imgs[0]
            self.contagem_imagem = 0

        # se o passaro tiver caindo não bate a asa
        if self.angulo <= -80:
            self.imagem = self.imgs[1]
            self.contagem_imagem = self.tempo_animacao+2

        # desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_img = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_img)
        #cria um retangulo em volta da imagem com o intuito de desenhá-la na tela
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

class Cano:
    distancia = 200
    velocidade = 5

    # x é a posição do cano na tela
    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0 #cano de cima
        self.pos_base = 0 #cano de baixo
        self.cano_topo = pygame.transform.flip(imagem_cano, False, True)
        self.cano_base = imagem_cano
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.cano_topo.get_height()
        self.pos_base = self.altura + self.distancia

    def mover(self):
        self.x -= self.velocidade

    def desenhar(self, tela):
        tela.blit(self.cano_topo, (self.x, self.pos_topo))
        tela.blit(self.cano_base, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.cano_topo)
        base_mask = pygame.mask.from_surface(self.cano_base)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        # verifica se houve colisao
        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False



class Chao:
    velocidade = 5
    largura = imagem_chao.get_width()
    imagem = imagem_chao

    def __init__(self, y):
        self.y = y #posição na tela
        self.x1 = 0 # chão 1
        self.x2 = self.largura # chão 2 = self.x1 + self.largura

    def mover(self):
        self.x1 -= self.velocidade # chão está andando no sentido negativo
        self.x2 -= self.velocidade

        if self.x1 + self.largura < 0: # 0 é o fim da tela
            self.x1 = self.x2 + self.largura
        if self.x2 + self.largura < 0:
            self.x2 = self.x1 + self.largura

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x1, self.y))
        tela.blit(self.imagem, (self.x2, self.y))


def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(imagem_background, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)

    for cano in canos:
        cano.desenhar(tela)

    texto = fonte_pontos.render(f'Pontuação: {pontos}', 1, (255, 255, 255))
    tela.blit(texto, (tela_largura - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()

def jogo():
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((tela_largura, tela_altura))
    pontos = 0
    relogio = pygame.time.Clock() # tempo de exibição da tela

    rodando = True
    while rodando:
        relogio.tick(30) # 30 frames por segundo

        # interação com game é um evento pygame.event
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: # clicar no x
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN: # apertar qualquer tecla
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()
        # mover os objetos
        for passaro in passaros:
            passaro.mover()
        chao.mover()

        # Mover cano e verificar colisao
        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro): # se o passaro colidiu
                    passaros.pop(i) # remove o passaro

                if not cano.passou and passaro.x > cano.x: # se o passaro passou do cano
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()
            if cano.x + cano.cano_topo.get_width() < 0: # se a soma da posição do cano com a largura do topo for < 0
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)


        desenhar_tela(tela, passaros, canos, chao, pontos)

if __name__ == '__main__':
    jogo()

