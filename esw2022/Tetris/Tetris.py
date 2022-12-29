from Joystick import Joystick 
from PIL import Image, ImageDraw, ImageFont
from math import sqrt
from random import randint

joystick = Joystick()
background = Image.open("/home/kau-esw/ESW/Tetris_background.jpg")
my_draw = ImageDraw.Draw(background)
font = ImageFont.truetype('/home/kau-esw/ESW/DungGeunMo.ttf', 50)
width = 12                 # 게임판 가로
height = 22                # 게임판 세로
speed = 40                 # 블록 하락 속도
block_size = 7             # 블록 크기
block_grid_size = 10       # 블록 격자 크기
gameboard = []             # 게임판
colors = ((0, 0, 0),(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255), (75, 0, 130), (128, 0, 128), (150, 75, 0))   # 블록 색상
CURRENT_BLOCK = None       # 현재 블록
NEXT_BLOCK = None          # 다음 블록
BLOCK_DATA = (             # 블록 데이터(모양, 방향)
    (
        (0, 0, 1, \
         1, 1, 1, \
         0, 0, 0),
        (0, 1, 0, \
         0, 1, 0, \
         0, 1, 1),
        (0, 0, 0, \
         1, 1, 1, \
         1, 0, 0),
        (1, 1, 0, \
         0, 1, 0, \
         0, 1, 0),
    ), (
        (2, 0, 0, \
         2, 2, 2, \
         0, 0, 0),
        (0, 2, 2, \
         0, 2, 0, \
         0, 2, 0),
        (0, 0, 0, \
         2, 2, 2, \
         0, 0, 2),
        (0, 2, 0, \
         0, 2, 0, \
         2, 2, 0)
    ), (
        (0, 3, 0, \
         3, 3, 3, \
         0, 0, 0),
        (0, 3, 0, \
         0, 3, 3, \
         0, 3, 0),
        (0, 0, 0, \
         3, 3, 3, \
         0, 3, 0),
        (0, 3, 0, \
         3, 3, 0, \
         0, 3, 0)
    ), (
        (4, 4, 0, \
         0, 4, 4, \
         0, 0, 0),
        (0, 0, 4, \
         0, 4, 4, \
         0, 4, 0),
        (0, 0, 0, \
         4, 4, 0, \
         0, 4, 4),
        (0, 4, 0, \
         4, 4, 0, \
         4, 0, 0)
    ), (
        (0, 5, 5, \
         5, 5, 0, \
         0, 0, 0),
        (0, 5, 0, \
         0, 5, 5, \
         0, 0, 5),
        (0, 0, 0, \
         0, 5, 5, \
         5, 5, 0),
        (5, 0, 0, \
         5, 5, 0, \
         0, 5, 0)
    ), (
        (6, 6, \
        6, 6),
        (6, 6, \
        6, 6),
        (6, 6, \
        6, 6),
        (6, 6, \
        6, 6)
    ), (
        (0, 7, 0, 0, \
         0, 7, 0, 0, \
         0, 7, 0, 0, \
         0, 7, 0, 0),
        (0, 0, 0, 0, \
         7, 7, 7, 7, \
         0, 0, 0, 0, \
         0, 0, 0, 0),
        (0, 0, 7, 0, \
         0, 0, 7, 0, \
         0, 0, 7, 0, \
         0, 0, 7, 0),
        (0, 0, 0, 0, \
         0, 0, 0, 0, \
         7, 7, 7, 7, \
         0, 0, 0, 0)
    )
)
 
class Block:                                        # 블록 클래스
    def __init__(self, count):
        self.turn = randint(0,3)                    # 블록 방향
        self.type = BLOCK_DATA[randint(0,6)]        # 블록 종류 
        self.data = self.type[self.turn]            # 블록 데이터 
        self.size = int(sqrt(len(self.data)))       # 블록 크기(n x n)
        self.xpos = randint(2, 8 - self.size)       # 블록 x 좌표
        self.ypos = 1 - self.size                   # 블록 y 좌표
        self.fire = count + speed                   # 블록 이동
 
    def update(self, count):                        # 블록 상태 업데이트        
        erased = 0
        if overlap(self.xpos, self.ypos + 1, self.turn):   # 블록이 겹치는지 확인
            for ypos in range(CURRENT_BLOCK.size):
                for xpos in range(CURRENT_BLOCK.size):
                    index = ypos * self.size + xpos
                    val = CURRENT_BLOCK.data[index]
                    if 0 <= self.ypos+ypos < height and 0 <= self.xpos+xpos < width and val != 0:
                        gameboard[self.ypos+ypos][self.xpos+xpos] = val 
            erased = erase_line()
            next_block(count)
        if self.fire < count:
            self.fire = count + speed
            self.ypos += 1
        return erased
 
    def draw(self):      # 블록 그리기
        for index in range(len(self.data)):
            xpos = index % self.size
            ypos = index // self.size
            val = self.data[index]                
            if 0 <= ypos + self.ypos < height and 0 <= xpos + self.xpos < width and val != 0:
                x_pos = (block_grid_size + (xpos + self.xpos) * block_grid_size)
                y_pos = (block_grid_size + (ypos + self.ypos) * block_grid_size) 
                my_draw.rectangle((x_pos, y_pos, x_pos + block_size, y_pos + block_size), fill=(colors[val]))

def draw_score(score):    # 점수 표시
    my_draw.rectangle((180, 20, 240, 40), fill = (colors[0]))
    score_str = str(score).zfill(6)
    my_draw.text((195, 23), score_str)

def erase_line():         # 줄 삭제
    erased = 0
    ypos = 20
    while (ypos >= 0):
        if all(gameboard[ypos]):
            erased += 1
            del gameboard[ypos]
            gameboard.insert(0, [8,0,0,0,0,0,0,0,0,0,0,8])
        else:
            ypos -= 1
    return erased
 
def is_game_over():       # 게임 종료 조건
    count = 0
    for block in gameboard[0]:
        if block != 0:
            count += 1
    if count > 2:
        return True
    else:
        return False
 
def next_block(count):    # 다음 블록
    global CURRENT_BLOCK, NEXT_BLOCK
    if NEXT_BLOCK != None:
        CURRENT_BLOCK = NEXT_BLOCK
    else:
        CURRENT_BLOCK = Block(count)
    NEXT_BLOCK = Block(count)
 
def overlap(xpos, ypos, turn):   # 블록이 겹치는지 확인
    data = CURRENT_BLOCK.type[turn]
    for y_pos in range(CURRENT_BLOCK.size):
        for x_pos in range(CURRENT_BLOCK.size):
            index = y_pos * CURRENT_BLOCK.size + x_pos
            val = data[index]
            if 0 <= xpos+x_pos < width and 0 <= ypos+y_pos < height:
                if val != 0 and gameboard[ypos+y_pos][xpos+x_pos] != 0:
                    return True
    return False
 
def make_game_board():            # 게임판 만들기
    for i in range (height-1):
        gameboard.insert(i, [8,0,0,0,0,0,0,0,0,0,0,8])
    gameboard.insert(height-1, [8,8,8,8,8,8,8,8,8,8,8,8])
 
def draw_game_board():            # 게임판 그리기
    for ypos in range(height):
        for xpos in range(width):
            val = gameboard[ypos][xpos]
            my_draw.rectangle((block_grid_size+xpos*block_grid_size,block_grid_size+ypos*block_grid_size,block_grid_size+xpos*block_grid_size+ block_size ,block_grid_size+ypos*block_grid_size+ block_size), fill=(colors[val]))
 
def draw_current_block():         # 현재 블록 그리기
    CURRENT_BLOCK.draw()

def draw_next_block():            # 다음 블록 그리기
    for ypos in range(4):
        for xpos in range(4):
            index = ypos * NEXT_BLOCK.size + xpos
            x_pos = 200 + xpos * block_grid_size
            y_pos = 70 + ypos * block_grid_size
            my_draw.rectangle((x_pos, y_pos, x_pos + block_size, y_pos + block_size), fill=(colors[0]))

    for ypos in range(NEXT_BLOCK.size):
        for xpos in range(NEXT_BLOCK.size):
            index = ypos * NEXT_BLOCK.size + xpos
            val = NEXT_BLOCK.data[index]
            x_pos = 200 + xpos * block_grid_size
            y_pos = 70 + ypos * block_grid_size
            my_draw.rectangle((x_pos, y_pos, x_pos + block_size, y_pos + block_size), fill=(colors[val]))

def draw_game_over():              # 게임 종료 메시지
    text = "GAME OVER"
    my_draw.text((10, 90), text, fill='white', font=font)

def main():                        
    global speed
    count = 0
    score = 0
    
    next_block(speed)
 
    make_game_board()
 
    while True:
 
        game_over = is_game_over()

        if not game_over:
            count += 5
            if count % 1000 == 0:
                speed = max(1, speed - 5)
            erased = CURRENT_BLOCK.update(count)

            if (erased > 0):
                score += (200 * erased)

            next_x = CURRENT_BLOCK.xpos
            next_y = CURRENT_BLOCK.ypos
            next_t = CURRENT_BLOCK.turn

            if not joystick.button_A.value:
                next_t = (next_t + 1) % 4
            elif not joystick.button_L.value:
                next_x -= 1
            elif not joystick.button_R.value:
                next_x += 1
            elif not joystick.button_D.value:
                next_y += 1
            elif not joystick.button_B.value:
                while not overlap(next_x, next_y + 1, next_t):
                    next_y += 1
            
            if not overlap(next_x, next_y, next_t):
                CURRENT_BLOCK.xpos = next_x
                CURRENT_BLOCK.ypos = next_y
                CURRENT_BLOCK.turn = next_t
                CURRENT_BLOCK.data = CURRENT_BLOCK.type[CURRENT_BLOCK.turn]
 
        draw_game_board()
 
        draw_current_block()

        draw_next_block()

        draw_score(score)

        if game_over:
            draw_game_over()
            
        joystick.disp.image(background)
        
if __name__ == '__main__':
    main()