import random
import os
import time

# Configurações do jogo
LABIRINTO = [
    "#############################",
    "#..#......#.........#........#",
    "#......#.....######...##.....#",
    "#......#...#.......#.....#...#",
    "#.#...#....#..#..#........#..#",
    "#.#.....#...#.#.......#...#..#",
    "#.###.....###...##....#.....##",
    "#.......#...#...#.....#.....##",
    "######...........#....#..#####",
    "#.......#...#.........#......#",
    "##############################"
]

# Códigos ANSI para cores
COR_VERDE = "\033[92m"
COR_AMARELO = "\033[93m"
COR_VERMELHO = "\033[91m"
COR_AZUL = "\033[94m"
COR_ROSA = "\033[95m"
COR_RESETAR = "\033[0m"

def inicio():
    print('Carregando jogo...')
    time.sleep(2)
    print('\033[92m Mova o PacPy, pegue todos os pontos e fuja dos Fasminhas!\033[0m')

def imprimir_labirinto(pacpy_pos, fasminhas_pos, pontos_restantes, vidas):
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpar a tela
    for y, linha in enumerate(LABIRINTO):
        nova_linha = ""
        for x, char in enumerate(linha):
            if (y, x) == pacpy_pos:
                nova_linha += COR_AMARELO + 'P' + COR_RESETAR
            elif (y, x) in fasminhas_pos:
                cor_fasminha = COR_VERMELHO
                if fasminhas_pos[(y, x)] == 'azul':
                    cor_fasminha = COR_AZUL
                elif fasminhas_pos[(y, x)] == 'rosa':
                    cor_fasminha = COR_ROSA
                nova_linha += cor_fasminha + 'F' + COR_RESETAR
            elif char == '.':
                nova_linha += COR_VERDE + '.' + COR_RESETAR
            else:
                nova_linha += char
        print(nova_linha)
    print(f"\nPontos restantes: {pontos_restantes}")
    print(f"Vidas restantes: {vidas}")
    print("Use WASD para mover o PacPy. Pressione Q para sair.")

def movimentar_pacpy(pacpy_pos, direcao):
    y, x = pacpy_pos
    if direcao == 'w':  # Cima
        y -= 1
    elif direcao == 's':  # Baixo
        y += 1
    elif direcao == 'a':  # Esquerda
        x -= 1
    elif direcao == 'd':  # Direita
        x += 1
    return y, x

def movimentar_fasminha(fasminha_pos, pacpy_pos, perseguir):
    y, x = fasminha_pos
    if perseguir:
        # Movimento em direção ao PacPy
        dy, dx = pacpy_pos
        if y < dy:
            y += 1
        elif y > dy:
            y -= 1
        if x < dx:
            x += 1
        elif x > dx:
            x -= 1
    else:
        # Movimento aleatório
        mov = random.choice(['w', 's', 'a', 'd'])
        if mov == 'w':  # Cima
            y -= 1
        elif mov == 's':  # Baixo
            y += 1
        elif mov == 'a':  # Esquerda
            x -= 1
        elif mov == 'd':  # Direita
            x += 1

    # Verifica se o novo local do fasminha é uma parede ou fora dos limites
    if y < 0 or y >= len(LABIRINTO) or x < 0 or x >= len(LABIRINTO[0]) or LABIRINTO[y][x] == '#':
        return fasminha_pos  # Retorna a posição atual se a movimentação for inválida

    return y, x

def atualizar_fasminhas(fasminhas_pos, pacpy_pos, pontos_coletados):
    perseguir = pontos_coletados >= 20
    novas_pos_fasminhas = {}
    for pos, cor in fasminhas_pos.items():
        nova_pos_fasminha = movimentar_fasminha(pos, pacpy_pos, perseguir)
        # Se a nova posição estiver disponível ou vazia e não colidir com outro Fasminha, atualiza a posição do fasminha
        if nova_pos_fasminha not in novas_pos_fasminhas:
            novas_pos_fasminhas[nova_pos_fasminha] = cor

    return novas_pos_fasminhas

def contar_pontos_restantes():
    return sum(1 for linha in LABIRINTO for char in linha if char == '.')

def jogo_pacpy():
    inicio()
    pacpy_pos = (1, 1)
    fasminhas_pos = {
        (5, 5): 'vermelho',
        (2, 7): 'azul',
        (6, 10): 'rosa'
    }
    pontos_restantes = contar_pontos_restantes()
    pontos_coletados = 0
    vidas = 3  # Número de vidas

    while True:
        imprimir_labirinto(pacpy_pos, fasminhas_pos, pontos_restantes, vidas)
        direcao = input("Movimento: ").strip().lower()
        if direcao == 'q':
            print("Saindo do jogo...")
            break

        if direcao in ['w', 's', 'a', 'd']:
            nova_pacpy_pos = movimentar_pacpy(pacpy_pos, direcao)
            ny, nx = nova_pacpy_pos

            # Verifica se a nova posição é uma parede
            if LABIRINTO[ny][nx] != '#':
                pacpy_pos = nova_pacpy_pos

                # Coleta pontos
                if LABIRINTO[ny][nx] == '.':
                    LABIRINTO[ny] = LABIRINTO[ny][:nx] + ' ' + LABIRINTO[ny][nx + 1:]
                    pontos_restantes -= 1
                    pontos_coletados += 1

            fasminhas_pos = atualizar_fasminhas(fasminhas_pos, pacpy_pos, pontos_coletados)

            # Verifica colisão entre PacPy e qualquer fasminha
            if pacpy_pos in fasminhas_pos:
                vidas -= 1
                print("Você encontrou um fasminha!")
                if vidas <= 0:
                    print("Você ficou sem vidas! Game Over!")
                    break
                else:
                    print(f"Você tem {vidas} vidas restantes.")
                    # Move o PacPy para a posição inicial após perder uma vida
                    pacpy_pos = (1, 1)
                    time.sleep(1)  # Pequena pausa após perder uma vida

            if pontos_restantes == 0:
                print("Parabéns! Você coletou todos os pontos!")
                break

        time.sleep(0.5)

if __name__ == "__main__":
    jogo_pacpy()

