
# Henry Rieger, qyd4fd, Jonny deButts - jhd7fc

import pygame
import gamebox

camera = gamebox.Camera(800, 600)
background = gamebox.from_image(2500, 750, "background.jpg")
camera.y = 1200
enemy_sheet = gamebox.load_sprite_sheet('enemy_Real.png', 2, 3)
enemies_list = []

num_frames = 6
curr_frame = 0
stepcount = 0
direction = True

only_one_power1 = 0
only_one_power2 = 0

jump_frames = 4
jump_ani = 8
jumpcount = 0

hurt_counter = 0

sheet = gamebox.load_sprite_sheet('cool_dude_sprites.png', 4, 8)
character = gamebox.from_image(300, 1430, sheet[curr_frame])
power_up_sheet = gamebox.load_sprite_sheet('power_upped_man (1).png', 4, 8)

background2 = gamebox.from_image(5750, 350, 'background_try2.png')

floor = gamebox.from_color(2500, 1465, "black", 5000, 70)
floor2 = gamebox.from_color(400, 565, "black", 800, 70)
floor3 = gamebox.from_color(5920, 1065, 'white', 3000, 70)

heart_amount = 3
touching_enemy = False
power_counter = 0
pause = False
counter = 0
power_on1 = False
power_on2 = False
power_on3 = False
over = False
platforms_list = []

touch_bonus = False
pipe = gamebox.from_image(4900, 1395, "pipe.png")
pipe_key = gamebox.from_color(4900, 1381, "black", 1, 1)

pipe2 = gamebox.from_image(130, 0, 'pipe.png')
pipe2.rotate(180)
trigger2 = gamebox.from_color(130, -2, 'black', 1, 1)

power_up_list = []

color_frames = 6
now_frame = 0
colorcount = 0

setup = True

touching_closed_chest = False

have_key = False
key = gamebox.from_image(130, 75, 'key_8bit.png')
key.scale_by(0.05)

closed_treasure = gamebox.from_image(6500, 1005, 'closed_treasure.png')
open_treasure = gamebox.from_image(6500, 1005, 'open_treasure.png')

closed_treasure.scale_by(0.3)
open_treasure.scale_by(0.3)

setup_game = True

win = False


def setup(keys):
    """
    displays the start screen at the beginning of the game with instructions, stays until the player presses the P key
    :param keys: if P is pressed, the screen disappears and the game starts
    :return: nothing
    """
    global setup_game
    camera.clear('dark green')
    camera.draw(gamebox.from_text(400, 1000, 'Welcome to Cool Man!', 100, 'white'))
    camera.draw(
        gamebox.from_text(400, 1050, 'Designed by Henry Rieger (qyd4fd) and Jonny deButts (jhd7fc)', 30, 'white'))
    camera.draw(gamebox.from_text(400, 1200, 'How to play:', 50, 'white'))
    camera.draw(gamebox.from_text(400, 1250, 'Use the arrow keys to move left and right', 30, 'white'))
    camera.draw(gamebox.from_text(400, 1275, 'and the space bar to jump!', 30, 'white'))
    camera.draw(gamebox.from_text(400, 1340, 'Open the chest to win the game!', 50, 'white'))
    camera.draw(gamebox.from_text(400, 1450, 'Press the "P" key to play!', 75, 'white'))
    if pygame.K_p in keys:
        setup_game = False


def jump(keys):
    """
    controls the jumping mechanic, if space is pressed the character jumps only if they are touching the floor or a
    platform, stops the player from falling through the floor
    :param keys: space for jumping
    :return: nothing
    """
    global jumpcount, platforms_list
    if character.bottom_touches(floor):
        character.yspeed = 0
        if pygame.K_SPACE in keys:
            character.yspeed = -15
    if character.bottom_touches(floor) or character.bottom_touches(floor2) or character.bottom_touches(floor3):
        character.yspeed = 0
        if pygame.K_SPACE in keys:
            character.yspeed = -15
    for platform in platforms_list:
        if character.bottom_touches(platform):
            character.yspeed = 0
            if pygame.K_SPACE in keys:
                character.yspeed = -15
    character.move_to_stop_overlapping(floor)
    character.move_to_stop_overlapping(floor2)
    character.move_to_stop_overlapping(floor3)


def pause_game():
    """
    draws a pause button in the top left corner that pauses the game when pressed, as well as a resume button when
    the game is paused which resumes the game when pressed
    :return: nothing
    """
    global pause
    camera.draw(gamebox.from_color(camera.x - 355, camera.y - 255, "grey", 60, 60))
    camera.draw(gamebox.from_color(camera.x - 367, camera.y - 255, "black", 12, 50))
    camera.draw(gamebox.from_color(camera.x - 343, camera.y - 255, "black", 12, 50))
    if camera.mouseclick and camera.x - 385 <= camera.mousex <= camera.x - 325 and camera.y - 285 <= camera.mousey <= camera.y - 225:
        pause = True
        camera.clear("black")
        resume = gamebox.from_color(camera.x, camera.y, "grey", 400, 100)
        camera.draw(gamebox.from_text(camera.x, camera.y - 150, "PAUSED", 50, "white"))
        camera.draw(resume)
        camera.draw(gamebox.from_text(camera.x, camera.y, "Resume", 50, "black"))
    if camera.mouseclick and camera.x - 200 <= camera.mousex <= camera.x + 200 and camera.y - 50 <= camera.mousey <= camera.y + 50:
        pause = False


def gravity():
    """
    controls the gravity for falling in the game
    :return: nothing
    """
    character.yspeed += 1
    character.y = character.y + character.yspeed


def movement(keys):
    """
    controls the movement of the player with left and right arrow keys, controls the sprite frames for character
    movement, controls speed boost and sprites when the power-up is used, keeps the player in the gamebox,
    controls camera movement that follows the player, shows a message when the chest is touched without a key,
    opens the chest when the player has the key, calls the gravity function for it to be used
    :param keys: left and right arrow keys for moving
    :return: nothing
    """
    global power_counter, stepcount, direction, colorcount, have_key, win, touch_bonus
    if not keys and (not power_on1) and (not power_on2):
        character.image = sheet[5]
    if (power_on1 and power_counter <= 100) or (power_on2 and power_counter <= 100):
        if pygame.K_RIGHT in keys:
            character.x += 20
            colorcount += 0.5
            curr_image = int(colorcount) % color_frames
            if not direction:
                character.flip()
                direction = True
            character.image = power_up_sheet[curr_image]
        if pygame.K_LEFT in keys:
            character.x -= 20
            colorcount -= 0.5
            curr_image = int(colorcount) % color_frames
            if direction:
                character.flip()
                direction = False
            character.image = power_up_sheet[curr_image]
        power_counter += 1
    else:
        if pygame.K_RIGHT in keys:
            character.x += 10
            stepcount += 0.5
            curr_image = int(stepcount) % num_frames
            if not direction:
                character.flip()
                direction = True
            character.image = sheet[curr_image]
        if pygame.K_LEFT in keys:
            character.x -= 10
            stepcount -= 0.5
            curr_image = int(stepcount) % num_frames
            if direction:
                character.flip()
                direction = False
            character.image = sheet[curr_image]
    if character.x > 250 and not touch_bonus:
        camera.x = character.x + 150
    if character.x > 4985 and character.y > 1100:
        character.x = 4985
    if character.x > 4450 and character.y > 1000:
        camera.x = 4600
    if character.x < 6300 and (not touch_bonus) and character.y < 1080:
        camera.x = character.x + 150
    if character.x < 15:
        character.x = 15
    if camera.x < 400:
        camera.x = 400
    if character.bottom_touches(floor3):
        camera.y = 805
    if character.y > 1080 or character.bottom_touches(platform1):
        camera.y = 1200
    if character.x > 6300:
        camera.x = 6450
    if character.x > 6835:
        character.x = 6835
    if character.touches(key):
        have_key = True
    if character.touches(closed_treasure):
        camera.draw(gamebox.from_text(6400, 800, 'Uh oh, you\'re missing a key!', 35, 'white'))
    if character.touches(open_treasure) and have_key:
        win = True
    if character.touches(trigger2):
        character.x = 4700
        character.y = 1430
        touch_bonus = False
    for platforms in platforms_list:
        if character.overlap(platforms):
            character.move_to_stop_overlapping(platforms)
    gravity()


def make_enemies(x, y):
    """
    allows for the creation of multiple enemies using a specific sprite with parameters x and y that determine where
    the enemy will be placed, adds enemy to new_enemy which will draw it
    :param x: x-coordinate of where the enemy is placed
    :param y: y-coordinate of where the enemy is placed
    :return: nothing
    """
    global enemies_list
    new_enemy = gamebox.from_image(x, y, enemy_sheet[0])
    new_enemy.scale_by(0.35)
    new_enemy.flip()
    enemies_list.append([new_enemy, True])


make_enemies(600, 1410)
make_enemies(1200, 1410)
make_enemies(1800, 1410)
make_enemies(2100, 1410)
make_enemies(2800, 1410)
make_enemies(3500, 1410)

make_enemies(4800, 1011)
make_enemies(5300, 1011)
make_enemies(5500, 1011)
make_enemies(5900, 1011)


def enemy():
    """
    controls enemy animation, taking away lives when character touches enemy, set timer so character can't get hurt
    again immediately after being hurt, killing enemies by jumping on them, invincibility when powered up,
    boosting the character up when they kill an enemy
    :return: nothing
    """
    global counter, heart_amount, enemy_alive, touching_enemy, power_on1, enemies_list, hurt_counter, power_on2
    counter += 2
    hurt_counter += 1
    for each_enemy in enemies_list:
        if each_enemy[1]:
            if counter % 60 == 0:
                each_enemy[0].flip()
            camera.draw(each_enemy[0])
            if counter == 120:
                counter = 0
            if counter < 60:
                each_enemy[0].x += 10
            if counter >= 60:
                each_enemy[0].x -= 10
            if not power_on1 and not power_on2:
                if not touching_enemy:
                    if character.right_touches(each_enemy[0]) or character.left_touches(each_enemy[0]):
                        heart_amount -= 1
                        each_enemy[0].image = enemy_sheet[1]
                        touching_enemy = True
                if not touching_enemy:
                    each_enemy[0].image = enemy_sheet[0]
                    if character.bottom_touches(each_enemy[0]) and each_enemy[0].top_touches(character):
                        character.yspeed = -15
                        each_enemy[1] = False
            elif power_on1 or power_on2:
                if character.touches(each_enemy[0]):
                    each_enemy[0].image = enemy_sheet[2]
                    each_enemy[1] = False
            if hurt_counter % 80 == 0:
                touching_enemy = False


powerup1 = gamebox.from_color(840, 1200, "light blue", 20, 20)
powerup2 = gamebox.from_color(3000, 1200, "light blue", 20, 20)


def draw_powerups():
    """
    draws each power-up and makes sure each power-up can only be obtained once
    :return: nothing
    """
    if not power_on1:
        if only_one_power1 == 0:
            camera.draw(powerup1)
    if not power_on2:
        if only_one_power2 == 0:
            camera.draw(powerup2)


def power_up():
    """
    controls the sprite animations of the character when powered up, the duration of the power up, and the picking up
    of the power up
    :return: nothing
    """
    global power_counter, power_on1, color_frames, colorcount, now_frame, direction, power_on2, power_on3, \
        only_one_power1, only_one_power2
    if character.touches(powerup1):
        power_on1 = True
        only_one_power1 += 1
    if character.touches(powerup2):
        power_on2 = True
        only_one_power2 += 1
    if (power_on1 and power_counter <= 100) or (power_on2 and power_counter <= 100):
        if direction:
            colorcount += 0.5
        else:
            colorcount -= 0.5
        curr_image = int(colorcount) % num_frames
        character.image = power_up_sheet[curr_image]
    if power_counter >= 100 and power_on1:
        power_on1 = False
        power_counter = 0
    if power_counter >= 100 and power_on2:
        power_on2 = False
        power_counter = 0


def hearts():
    """
    controls the hearts drawn for character lives, draws amount based on lives, calls game over when no lives are left
    :return: nothing
    """
    global heart_amount
    heart = gamebox.from_image(camera.x + 360, camera.y - 260, "heart_adobespark.png")
    heart2 = gamebox.from_image(camera.x + 280, camera.y - 260, "heart_adobespark.png")
    heart3 = gamebox.from_image(camera.x + 200, camera.y - 260, "heart_adobespark.png")
    if heart_amount == 3:
        camera.draw(heart)
        camera.draw(heart2)
        camera.draw(heart3)
    if heart_amount == 2:
        camera.draw(heart)
        camera.draw(heart2)
    if heart_amount == 1:
        camera.draw(heart)
    if heart_amount == 0:
        game_over()


def make_platforms(x, y):
    """
    function for drawing platforms based on x and y coordinates entered
    :param x: x coordinate of said platform
    :param y: y coordinate of said platform
    :return: nothing
    """
    platform = gamebox.from_image(x, y, 'platforms.png')
    platform.scale_by(0.15)
    platforms_list.append(platform)


make_platforms(830, 1340)
make_platforms(3000, 1340)
make_platforms(3900, 1200)
make_platforms(3600, 1300)
make_platforms(3300, 1350)

make_platforms(450, 450)
make_platforms(550, 350)
make_platforms(400, 250)
make_platforms(170, 225)
make_platforms(130, 125)

platform1 = gamebox.from_image(4200, 1100, 'platforms.png')
platform1.scale_by(0.15)
platforms_list.append(platform1)


def game_over():
    """
    displays a game over screen when the character runs out of lives/hearts, ends game
    :return: nothing
    """
    global over
    over = True
    gamebox.pause()
    camera.clear('black')
    camera.draw(gamebox.from_text(camera.x, camera.y, "GAME OVER", 150, "red"))


def bonus_setup():
    """
    controls bonus room that contains the key and teleports player when they enter the pipe
    :return: nothing
    """
    global touch_bonus
    trigger = gamebox.from_color(4900, 1395, "black", 40, 20)
    wall1 = gamebox.from_color(20, 265, "black", 40, 530)
    wall2 = gamebox.from_color(780, 265, "black", 40, 530)
    character.move_to_stop_overlapping(trigger)
    camera.draw(trigger)
    camera.draw(pipe)
    camera.draw(pipe_key)
    camera.draw(wall1)
    camera.draw(wall2)
    character.move_to_stop_overlapping(wall1)
    character.move_to_stop_overlapping(wall2)
    if character.touches(pipe_key):
        touch_bonus = True
        character.x = 700
        character.y = 0
        camera.y = 300
        camera.x = 400


def win_game():
    """
    displays win screen when called
    :return: nothing
    """
    global win
    gamebox.pause()
    camera.clear('dark green')
    camera.draw(gamebox.from_text(camera.x, camera.y - 75, "You win!", 150, "white"))
    camera.draw(gamebox.from_text(camera.x, camera.y, "Nice job!", 75, "white"))


def tick(keys):
    """
    calls every function for the game 30 times per second, controls the set up, pausing, winning the game,
    and controls treasure chest being open/closed
    :param keys: any key pressed by the user (p/spacebar/right arrow/left arrow)
    :return: nothing
    """
    if setup_game:
        setup(keys)
    if not setup_game:
        if not pause:
            setup(keys)
            camera.draw(floor)
            camera.draw(background)
            camera.draw(background2)
            if not have_key:
                camera.draw(closed_treasure)
                camera.draw(key)
            else:
                camera.draw(open_treasure)
            for platform in platforms_list:
                camera.draw(platform)
            draw_powerups()
            movement(keys)
            jump(keys)
            camera.draw(character)
            enemy()
            power_up()
            bonus_setup()
            hearts()
            camera.draw(pipe2)
        if not over:
            pause_game()
        if win:
            win_game()
    camera.display()


gamebox.timer_loop(30, tick)
