# 🚀 Nave de Combate 🚀

Bem-vindo ao "Nave de Combate", um jogo de tiro com rolagem lateral (side-scroller) no estilo arcade, desenvolvido em Python com a biblioteca Pygame. Pilote sua nave de combate e defenda o setor de ondas de inimigos!

![Placeholder para GIF do Jogo](https://placehold.co/800x400/000000/FFFFFF?text=Gameplay+Nave+de+Combate)
*(Este é um placeholder - substitua por um GIF ou screenshot do seu jogo!)*

---

## 🎯 Sobre o Jogo

Em "Nave de Combate", você pilota uma nave ágil com o objetivo de destruir as naves inimigas que aparecem pela direita da tela. A cada inimigo destruído, você ganha pontos. O jogo continua até que sua nave colida com um inimigo.

## ✨ Funcionalidades

* **Jogabilidade Side-Scroller:** Controle sua nave verticalmente enquanto a tela e os inimigos avançam horizontalmente.
* **Ciclo de Jogo Completo:** O jogo possui um menu inicial, a tela de jogo principal e uma tela de "Game Over".
* **Sistema de Pontuação:** Ganhe pontos por cada inimigo que destruir.
* **Efeitos Visuais e Sonoros:** O jogo inclui um fundo com rolagem, som de tiros, explosões, música de fundo e uma trilha de game over para uma experiência mais imersiva.
* **Loop Infinito:** Os inimigos reaparecem continuamente, oferecendo um desafio constante para testar seus reflexos.

## 🕹️ Como Jogar

* **Seta para Cima (`↑`)**: Move a nave para cima.
* **Seta para Baixo (`↓`)**: Move a nave para baixo.
* **Barra de Espaço (`Espaço`)**: Dispara um míssil.
* **Tecla ESC (`Esc`)**: Fecha o jogo a qualquer momento.

## 🚀 Instalação e Execução

Para rodar o jogo em sua máquina, siga os passos abaixo.

### 1. Pré-requisitos

* **Python 3:** Certifique-se de que você tem o Python 3 instalado. Você pode baixá-lo em [python.org](https://www.python.org/).
* **Pygame:** Você precisará da biblioteca Pygame. Instale-a usando pip:
    ```bash
    pip install pygame
    ```

### 2. Baixe o Projeto

Clone ou baixe este repositório para a sua máquina.

```bash
git clone [https://github.com/seu-usuario/nave-de-combate.git](https://github.com/seu-usuario/nave-de-combate.git)
cd nave-de-combate
```
*(Lembre-se de substituir o URL pelo seu repositório real).*

### 3. Estrutura de Arquivos

O jogo espera que os arquivos de imagem e som estejam organizados em pastas específicas. Certifique-se de que sua estrutura de pastas seja a seguinte:

```
nave-de-combate/
├── game.py             # Seu arquivo de código do jogo
├── images/
│   ├── Background1.jpg
│   ├── NavaCombate1.png
│   ├── NavaRedonda1.png
│   ├── Missil1.png
│   └── explosao1.png
└── sounds/
    ├── laser_shoot.mp3
    ├── explosion.mp3
    ├── game_over.mp3
    └── background_music.mp3
```

### 4. Execute o Jogo

Com tudo configurado, execute o arquivo principal do jogo:

```bash
python game.py
```
*(Renomeie `game.py` para o nome real do seu arquivo, se for diferente).*

## 🛠️ Tecnologias Utilizadas

* **Python:** Linguagem principal do projeto.
* **Pygame:** Biblioteca para desenvolvimento de jogos 2D.

---
*Desenvolvido por Hebert Pereira.*
