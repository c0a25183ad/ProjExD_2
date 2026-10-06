import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rect: pg.rect) -> tuple[bool,bool]:
    """
    引数：こうかとうまたは爆弾のrect
    戻り値：横方向判定結果、縦方向判定結果
    画面内ならTrue　画面内ならFalse
    """
    yoko,tate=True,True
    if rect.left<0 or WIDTH <rect.right:
        yoko=False
    if rect.top<0 or HEIGHT<rect.bottom:
        tate=False
    return yoko,tate


def gameover(screen:pg.Surface) ->None :
    """
    引数：screen
    戻り値：なし
    """
    gobg_img=pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(gobg_img,(0,0,0),pg.Rect(0,0,WIDTH,HEIGHT))
    gobg_img.set_alpha(100,0)
    screen.blit(gobg_img,[0,0])
    fonto=pg.font.Font(None,100)
    text=fonto.render("Game Over",True,(255,255,255))
    screen.blit(text,[400,300])
    crykk_img=pg.image.load("fig/8.png")
    screen.blit(crykk_img,[200,300])
    pg.display.update()
    time.sleep(5)


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    kk_img=pg.image.load("fig/3.png")
    fli_kk_img=pg.transform.flip(kk_img,True,False)
    kk_dict={
        (0,0): pg.transform.rotozoom(fli_kk_img,0,1),
        (0,5): pg.transform.rotozoom(fli_kk_img,270,1),
        (0,-5) :pg.transform.rotozoom(fli_kk_img,90,1),
        (5,0): pg.transform.rotozoom(fli_kk_img,0,1),
        (5,-5):pg.transform.rotozoom(fli_kk_img,45,1),
        (-5,0) :pg.transform.rotozoom(kk_img,0,1),
        (-5,5):pg.transform.rotozoom(kk_img,45,1),
        (-5,-5):pg.transform.rotozoom(kk_img,315,1),
        (5,5):pg.transform.rotozoom(fli_kk_img,315,1)
    }
    return kk_dict

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img=pg.Surface((20,20))
    bb_img.set_colorkey((0,0,0))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_rct=bb_img.get_rect()
    vx,vy=5,5
    bb_rct.center=random.randint(0,WIDTH),random.randint(0,HEIGHT)

    clock = pg.time.Clock()
    tmr = 0
    while True:
        kk_dict=get_kk_imgs()
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        DELTA={pg.K_UP:(0,-5),pg.K_DOWN:(0,5),pg.K_LEFT:(-5,0),pg.K_RIGHT:(5,0)}
        key_lst = pg.key.get_pressed()
        sum_mv = [0,0]
        for k,tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0]+=tpl[0]
                sum_mv[1]+=tpl[1]
        
        kk_rct.move_ip(sum_mv)
        bb_rct.move_ip(vx, vy) 
        kk_img=kk_dict[tuple(sum_mv)]
        screen.blit(kk_img, kk_rct)
        if check_bound(kk_rct)!=(True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(bb_img, bb_rct)
        yoko,tate=check_bound(bb_rct)
        if not yoko:
            vx*=-1
        if not tate:
            vy*=-1                       
        pg.display.update()
        tmr += 1
        clock.tick(50)
        if kk_rct.colliderect(bb_rct)==True:
            gameover(screen)
            break


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
