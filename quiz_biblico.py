# Instrucões: execute `pip install pygame` para instalar as dependências.
# Para iniciar o jogo, rode `python3 quiz_biblico.py`.

import json
import os
import random
import pygame
from datetime import datetime

# Cores
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 100, 200)
LIGHT_GRAY = (230, 230, 230)
DARK_GRAY = (50, 50, 50)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Tamanho da tela
WIDTH, HEIGHT = 800, 600

pygame.init()
pygame.display.set_caption("Quiz Bíblico")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 28)
BIG_FONT = pygame.font.SysFont("arial", 40, bold=True)


def draw_text(surface, text, font, color, x, y, center=True):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(img, rect)


class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surface, color_bg, color_text):
        pygame.draw.rect(surface, color_bg, self.rect, border_radius=8)
        draw_text(surface, self.text, FONT, color_text, self.rect.centerx, self.rect.centery)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


def load_questions():
    # Lista de perguntas. Adicione pelo menos 20.
    questions = [
        {
            "q": "Quem construiu a arca?",
            "opts": ["Abraão", "Noé", "Moisés", "Davi"],
            "ans": 1,
        },
        {
            "q": "Quantos dias durou o dilúvio?",
            "opts": ["7", "10", "40", "60"],
            "ans": 2,
        },
        {
            "q": "Quem foi lançado na cova dos leões?",
            "opts": ["Daniel", "Josué", "Elias", "Jonas"],
            "ans": 0,
        },
        {
            "q": "Onde Jesus nasceu?",
            "opts": ["Nazaré", "Belém", "Jerusalém", "Jericó"],
            "ans": 1,
        },
        {
            "q": "Qual o primeiro livro do Novo Testamento?",
            "opts": ["Mateus", "Gênesis", "Atos", "Apocalipse"],
            "ans": 0,
        },
        {
            "q": "Quem traiu Jesus?",
            "opts": ["Pedro", "Paulo", "Judas", "João"],
            "ans": 2,
        },
        {
            "q": "Quem derrotou Golias?",
            "opts": ["Saul", "Sansão", "Samuel", "Davi"],
            "ans": 3,
        },
        {
            "q": "Qual o salmo do Pastor?",
            "opts": ["Salmo 1", "Salmo 23", "Salmo 40", "Salmo 119"],
            "ans": 1,
        },
        {
            "q": "Quem foi engolido por um grande peixe?",
            "opts": ["Jonas", "Jó", "José", "Jacó"],
            "ans": 0,
        },
        {
            "q": "Quem recebeu as tábuas da lei?",
            "opts": ["Arão", "Josué", "Moisés", "Elias"],
            "ans": 2,
        },
        {
            "q": "Quantos livros tem a Bíblia?",
            "opts": ["66", "59", "27", "78"],
            "ans": 0,
        },
        {
            "q": "Quem escreveu a maioria dos salmos?",
            "opts": ["Salomão", "Davi", "Moisés", "Asafe"],
            "ans": 1,
        },
        {
            "q": "Qual livro vem após Juízes?",
            "opts": ["Ester", "Rute", "Samuel", "Gênesis"],
            "ans": 1,
        },
        {
            "q": "Quem interpretou os sonhos de Faraó?",
            "opts": ["José", "Daniel", "Elias", "Eliseu"],
            "ans": 0,
        },
        {
            "q": "Quantos dias Jesus ficou no deserto?",
            "opts": ["20", "30", "40", "50"],
            "ans": 2,
        },
        {
            "q": "Qual era a profissão de Pedro?",
            "opts": ["Pescador", "Coletor de impostos", "Carpinteiro", "Médico"],
            "ans": 0,
        },
        {
            "q": "Quem liderou a saída do Egito?",
            "opts": ["Josué", "José", "Moisés", "Abraão"],
            "ans": 2,
        },
        {
            "q": "Quem foi apóstolo dos gentios?",
            "opts": ["Pedro", "João", "Paulo", "Tiago"],
            "ans": 2,
        },
        {
            "q": "Qual profeta enfrentou os profetas de Baal?",
            "opts": ["Eliseu", "Elias", "Isaías", "Jeremias"],
            "ans": 1,
        },
        {
            "q": "Quem negou Jesus três vezes?",
            "opts": ["Paulo", "Pedro", "Tomé", "Tiago"],
            "ans": 1,
        },
        {
            "q": "Quem recebeu o título de pai da fé?",
            "opts": ["Abraão", "Isaque", "Josué", "Moisés"],
            "ans": 0,
        },
    ]
    random.shuffle(questions)
    return questions[:20]


def ask_question(question, number):
    running = True
    selected = None
    while running:
        screen.fill(LIGHT_GRAY)
        draw_text(screen, f"Pergunta {number+1}", BIG_FONT, DARK_BLUE, WIDTH//2, 50)
        draw_text(screen, question["q"], FONT, DARK_GRAY, WIDTH//2, 120)

        buttons = []
        for i, opt in enumerate(question["opts"]):
            btn = Button(f"{chr(65+i)} - {opt}", 200, 200 + i*70, 400, 50)
            btn.draw(screen, LIGHT_BLUE, DARK_GRAY)
            buttons.append(btn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for i, b in enumerate(buttons):
                    if b.is_clicked(pos):
                        selected = i
                        running = False

        pygame.display.flip()
        clock.tick(30)
    return selected


def update_ranking(username, score):
    ranking_file = "ranking.json"
    ranking = []
    if os.path.exists(ranking_file):
        with open(ranking_file, "r", encoding="utf-8") as f:
            try:
                ranking = json.load(f)
            except json.JSONDecodeError:
                ranking = []
    ranking.append({
        "usuario": username,
        "pontuacao": score,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
    })
    with open(ranking_file, "w", encoding="utf-8") as f:
        json.dump(ranking, f, ensure_ascii=False, indent=2)


def show_ranking():
    ranking_file = "ranking.json"
    ranking = []
    if os.path.exists(ranking_file):
        with open(ranking_file, "r", encoding="utf-8") as f:
            try:
                ranking = json.load(f)
            except json.JSONDecodeError:
                ranking = []
    ranking.sort(key=lambda x: x["pontuacao"], reverse=True)
    showing = True
    back_btn = Button("Voltar", WIDTH//2 - 70, HEIGHT - 80, 140, 50)
    while showing:
        screen.fill(LIGHT_GRAY)
        draw_text(screen, "Ranking", BIG_FONT, DARK_BLUE, WIDTH//2, 50)
        for i, item in enumerate(ranking[:10]):
            text = f"{i+1}. {item['usuario']} - {item['pontuacao']} pts - {item['data']}"
            draw_text(screen, text, FONT, DARK_GRAY, WIDTH//2, 120 + i*40)
        back_btn.draw(screen, LIGHT_BLUE, DARK_GRAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_btn.is_clicked(event.pos):
                    showing = False

        pygame.display.flip()
        clock.tick(30)


def game_over_screen(score):
    over = True
    again_btn = Button("Jogar Novamente", WIDTH//2 - 150, HEIGHT - 140, 300, 50)
    menu_btn = Button("Menu Principal", WIDTH//2 - 150, HEIGHT - 70, 300, 50)
    while over:
        screen.fill(LIGHT_GRAY)
        draw_text(screen, "Fim de Jogo", BIG_FONT, DARK_BLUE, WIDTH//2, 80)
        draw_text(screen, f"Pontuação: {score}", BIG_FONT, DARK_BLUE, WIDTH//2, 160)
        again_btn.draw(screen, LIGHT_BLUE, DARK_GRAY)
        menu_btn.draw(screen, LIGHT_BLUE, DARK_GRAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if again_btn.is_clicked(event.pos):
                    return True
                if menu_btn.is_clicked(event.pos):
                    return False

        pygame.display.flip()
        clock.tick(30)


def main():
    running = True
    while running:
        # Menu principal
        screen.fill(LIGHT_GRAY)
        draw_text(screen, "Quiz Bíblico", BIG_FONT, DARK_BLUE, WIDTH//2, 100)
        btn_start = Button("Iniciar Jogo", WIDTH//2 - 150, 200, 300, 60)
        btn_rank = Button("Ver Ranking", WIDTH//2 - 150, 300, 300, 60)
        btn_exit = Button("Sair", WIDTH//2 - 150, 400, 300, 60)
        btn_start.draw(screen, LIGHT_BLUE, DARK_GRAY)
        btn_rank.draw(screen, LIGHT_BLUE, DARK_GRAY)
        btn_exit.draw(screen, LIGHT_BLUE, DARK_GRAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_start.is_clicked(event.pos):
                    play_game()
                elif btn_rank.is_clicked(event.pos):
                    show_ranking()
                elif btn_exit.is_clicked(event.pos):
                    running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


def play_game():
    # Tela para inserir nome
    typing = True
    username = ""
    while typing:
        screen.fill(LIGHT_GRAY)
        draw_text(screen, "Digite seu nome (ate 12 caracteres)", FONT, DARK_BLUE, WIDTH//2, 200)
        pygame.draw.rect(screen, WHITE, pygame.Rect(WIDTH//2 - 150, 250, 300, 50))
        draw_text(screen, username, FONT, DARK_GRAY, WIDTH//2 - 145, 265, center=False)
        btn_ok = Button("OK", WIDTH//2 - 70, 320, 140, 50)
        btn_ok.draw(screen, LIGHT_BLUE, DARK_GRAY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if 0 < len(username) <= 12:
                        typing = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 12 and event.unicode.isprintable():
                        username += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_ok.is_clicked(event.pos) and 0 < len(username) <= 12:
                    typing = False
        pygame.display.flip()
        clock.tick(30)

    questions = load_questions()
    score = 0
    consecutive = 0
    bonus_awarded = False
    for idx, q in enumerate(questions):
        answer = ask_question(q, idx)
        correct = q["ans"]
        if answer == correct:
            score += 10
            consecutive += 1
            screen.fill(LIGHT_GRAY)
            draw_text(screen, "Acertou!", BIG_FONT, GREEN, WIDTH//2, HEIGHT//2)
            pygame.display.flip()
            pygame.time.delay(800)
            if consecutive % 5 == 0 and not bonus_awarded:
                score += 50
                bonus_awarded = True
                screen.fill(LIGHT_GRAY)
                draw_text(screen, "Bonus +50!", BIG_FONT, GREEN, WIDTH//2, HEIGHT//2)
                pygame.display.flip()
                pygame.time.delay(800)
        else:
            screen.fill(LIGHT_GRAY)
            corr = q["opts"][correct]
            draw_text(screen, f"Errou! A resposta correta é {corr}", FONT, RED, WIDTH//2, HEIGHT//2)
            pygame.display.flip()
            pygame.time.delay(1500)
            break
    update_ranking(username, score)
    again = game_over_screen(score)
    if again:
        play_game()


if __name__ == "__main__":
    main()
