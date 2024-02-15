import pygame as pg
from math import dist, cos, sin, degrees, atan2, pi
from random import choice, gauss
from settings import UI
from projectiles import Projectiles
from path import path


class Enemy(pg.sprite.Sprite):
    enemy_animations = {'destroy': [pg.image.load(path(f'Bomber/destroy/destroy{i}.png')).convert_alpha() for i in range(1, 10+1)],
                        'damage': [pg.image.load(path(f'Bomber/damage/damage{i}.png')).convert_alpha() for i in range(1, 10+1)],
                        'attack1': [pg.image.load(path(f'Bomber/attack1/attack1.{i}.png')).convert_alpha() for i in range(1, 3+1)],
                        'attack2': [pg.image.load(path(f'Bomber/attack2/attack2.1.png')).convert_alpha()],
                        'move': [pg.image.load(path(f'Bomber/move/move{i}.png')).convert_alpha() for i in range(1, 6+1)],
                        'idle': pg.image.load(path('Bomber/idle/idle1.png')).convert_alpha()}

    def __init__(self, time) -> None:
        super().__init__()

        self.time = time

        self.weapons_info = {'weapon1': {'damage': self.time*0.15+1.5,
                                         'attack_speed': self.time*0.2+2,
                                         'bullet_speed': self.time+10},
                             'weapon2': {'damage': self.time*0.6+6,
                                         'attack_speed': 12,
                                         'bullet_speed': self.time*0.4+4}}

        self.max_health = self.time+10
        self.health = self.max_health

        self.spin = 2.5
        self.angle = 0
        self.distance = 0
        self.max_velocity = self.time*0.6+6
        self.velocity = 0
        self.acceleration = 0.25
        self.friction = 0.15

        self.bullets = 0
        self.shot = 0
        self.reload_time = 5
        self.stopwatch_reload = 1
        self.reloading = False
        self.aiming = True
        self.firing = False

        self.electrocute_damage = 0
        self.electrocuting = False
        self.electrocute_count = 0

        self.burn_damage = 0
        self.burning = False
        self.burn_count = 0

        self.fullLife = True
        self.situation = 'alive'
        self.alpha = 255
        self.collide = False
        self.blinked = False

        self.scale = UI.scale * 1.3

        self.blink_color = {'white': (255, 255, 255),
                            'red': (255, 26, 26),
                            'blue': (56, 169, 255)}
        self.current_color = 'white'

        self.animations_time = {'move_speed': 3,
                                'boost_speed': 3,
                                'attack_speed': 1,
                                'damage_speed': 1,
                                'destroy_speed': 1.2,
                                'blink_speed': 0.4,
                                'vanish_speed': 1.5}

        self.index = {'id_destroy': 0,
                      'id_damage': 0, 'id_move': 0,
                      'id_attack1': 0, 'id_attack2': 0}

        self.status = {'is_damaged': False,
                       'is_attacked': False,
                       'is_destroyed': False,
                       'is_moved': False}

        self.image = Enemy.enemy_animations['idle']
        self.current_image = Enemy.enemy_animations['idle']
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)

        self.projectiles = pg.sprite.Group()

        self.position()
        self.sweep_weapon()

    def position(self) -> None:
        points = []
        points.append(
            (gauss(UI.half_width, UI.half_width/4), -self.rect.height/2-10))
        points.append((gauss(UI.half_width, UI.half_width/4),
                      UI.dimension[1] + self.rect.height/2+10))
        points.append(
            (-self.rect.width/2-10, gauss(UI.half_height, UI.half_height/4)))
        points.append((UI.dimension[0] + self.rect.width/2+10,
                      gauss(UI.half_height, UI.half_height/4)))
        spawn = choice(points)
        points.remove(spawn)
        self.target = choice(points)
        self.rect.center = spawn

        self.distance = dist(self.rect.center, self.target)
        self.target_angle = -degrees(atan2(
            self.target[1] - self.rect.centery, self.target[0] - self.rect.centerx))
        self.angle = self.target_angle

    def action(self, dt, player_dead) -> None:
        self.remain = dist(self.rect.center, self.target)
        if (self.distance / 2 < self.remain and not self.status['is_damaged'] and self.situation == 'alive') or player_dead == 'dead':
            self.velocity += self.acceleration * dt
            rotate = (self.target_angle - self.angle + 180) % 360 - 180
            if rotate >= 3:
                self.angle += self.spin * dt
            elif rotate <= -3:
                self.angle -= self.spin * dt
            self.status['is_moved'] = True

    def movement(self, dt) -> None:
        if self.velocity > self.max_velocity:
            self.velocity = self.max_velocity
        elif self.velocity < 0:
            self.velocity = 0

        self.rect.centerx += self.velocity * cos((self.angle*pi/180)) * dt
        self.rect.centery -= self.velocity * sin((self.angle*pi/180)) * dt

        self.velocity -= self.friction * dt

    def sweep_weapon(self) -> None:
        self.weapon = choice([1, 1, 1, 2])
        self.damage = self.weapons_info[f'weapon{self.weapon}']['damage']
        self.attack_speed = self.weapons_info[f'weapon{self.weapon}']['attack_speed']
        self.animations_time['attack_speed'] = 1/self.attack_speed
        self.bullet_speed = self.weapons_info[f'weapon{self.weapon}']['bullet_speed']
        self.bullets = 1 if self.weapon == 2 else 5

    def aim(self, dt, rect_player, player_dead) -> None:
        if self.distance / 2 >= self.remain and self.aiming and player_dead == 'alive':
            self.fire_angle = -degrees(atan2(
                rect_player[1] - self.rect.centery, rect_player[0] - self.rect.centerx))
            rotate = (self.fire_angle - self.angle + 180) % 360 - 180
            if rotate >= 3:
                self.angle += self.spin * dt
            elif rotate <= -3:
                self.angle -= self.spin * dt
            else:
                self.sweep_weapon()
                self.firing = True
                self.aiming = False

    def reload(self) -> None:
        if self.firing:
            self.status['is_attacked'] = True
        if self.reloading:
            self.stopwatch_reload -= 1 / \
                (max(UI.clock.get_fps(), 1) * self.reload_time)
            if self.stopwatch_reload <= 0:
                self.stopwatch_reload = 1
                self.aiming = True
                self.reloading = False

    def spawn_projectiles(self) -> None:
        self.projectiles.add(Projectiles(self.angle, self.rect.centerx,
                             self.rect.centery, f'enemy{self.weapon}', self.scale, self.damage, self.bullet_speed))
        self.shot += 1
        if self.shot >= self.bullets:
            self.shot = 0
            self.firing = False
            self.reloading = True

    def verification_health(self) -> None:
        if self.health <= self.max_health*0.5 and self.fullLife:
            self.status['is_damaged'] = True
            self.fullLife = False
        if self.health <= 0 and self.situation == 'alive':
            self.situation = 'dying'
            self.status['is_destroyed'] = True
            self.alpha = 255
            return self.rect.center
        return False

    def hit(self, damage):
        if self.situation in ['dead', 'dying']:
            return True
        self.health -= damage
        self.collide = True
        self.current_color = 'white'
        return False

    def set_burn(self, damage):
        self.burn_damage = damage
        self.burning = True
        self.burn_count = 0

    def burn(self, time):
        if self.burning:
            if time - self.stopwatch_burn >= 1000:
                self.health -= self.health*self.burn_damage/5
                self.stopwatch_burn = time
                self.burn_count += 1
                self.collide = True
                self.current_color = 'red'
            if self.burn_count >= 5:
                self.burn_count = 0
                self.burning = False
        else:
            self.stopwatch_burn = time

    def set_electrocute(self, damage):
        self.electrocute_damage = damage
        self.electrocuting = True
        self.electrocute_count = 0

    def electrocute(self, time):
        if self.electrocuting:
            if time - self.stopwatch_electrocute >= 600:
                self.health -= self.electrocute_damage*self.health/5
                self.stopwatch_electrocute = time
                self.electrocute_count += 1
                self.collide = True
                self.current_color = 'blue'
            if self.electrocute_count >= 5:
                self.electrocute_count = 0
                self.electrocuting = False
        else:
            self.stopwatch_electrocute = time

    def destroy(self) -> None:
        self.alpha -= 255/(max(UI.clock.get_fps(), 1) *
                           self.animations_time['vanish_speed'])
        self.image.set_alpha(self.alpha)
        if self.alpha <= 0:
            self.kill()

    def animation_state(self) -> None:
        self.current_image = self.enemy_animations['idle']
        if self.status['is_destroyed']:
            self.start_animation('destroy', 'id_destroy',
                                 'destroy_speed', 'is_destroyed')
        elif self.status['is_damaged']:
            self.start_animation('damage', 'id_damage',
                                 'damage_speed', 'is_damaged')
        elif self.status['is_attacked']:
            self.start_animation(f'attack{self.weapon}', f'id_attack{self.weapon}',
                                 'attack_speed', 'is_attacked')
        elif self.status['is_moved']:
            self.start_animation('move', 'id_move', 'move_speed', 'is_moved')
            self.status['is_moved'] = False

    def start_animation(self, action, step, speed, condition) -> None:
        self.current_image = Enemy.enemy_animations[action][int(
            self.index[step])]
        self.index[step] += len(Enemy.enemy_animations[action]) / \
            (max(UI.clock.get_fps(), 1) * self.animations_time[speed])
        if self.index[step] >= len(Enemy.enemy_animations[action]):
            self.index[step] = 0
            self.status[condition] = False
            if condition == 'is_destroyed':
                self.situation = 'dead'
            elif condition == 'is_attacked':
                self.spawn_projectiles()

    def att_sprite(self) -> None:
        self.image = pg.transform.rotozoom(
            self.current_image, self.angle, self.scale)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pg.mask.from_surface(self.image)

    def blink(self) -> None:
        if self.collide:
            if self.current_color == 'red':
                self.alpha = 180
            elif self.current_color == 'white':
                self.alpha = 255
            elif self.current_color == 'blue':
                self.alpha = 180
            self.blinked = True
            self.collide = False
        if self.blinked:
            self.white = self.image.copy()
            if len(self.mask.outline()) > 2:
                pg.draw.polygon(self.white, (self.blink_color[self.current_color][0],
                                             self.blink_color[self.current_color][1],
                                             self.blink_color[self.current_color][2],
                                             self.alpha),
                                self.mask.outline(), 0)
            self.image.blit(self.white, (0, 0))
            self.alpha -= 255/(max(UI.clock.get_fps(), 1) *
                               self.animations_time['blink_speed'])
            if self.alpha <= 0:
                self.blinked = False

    def update(self, dt, time, rect_player, player_dead, freeze) -> None:
        if self.situation == 'alive':
            if not freeze:
                self.action(dt, player_dead)
                self.movement(dt)
                self.aim(dt, rect_player, player_dead)
                self.reload()
                self.animation_state()
                self.projectiles.update(dt, rect_player)
            self.electrocute(time)
            self.burn(time)
            self.att_sprite()
            self.blink()
            self.projectiles.draw(UI.screen)
        elif self.situation == 'dying':
            if not freeze:
                self.movement(dt)
                self.animation_state()
                self.projectiles.update(dt, rect_player)
            self.att_sprite()
            self.projectiles.draw(UI.screen)
        elif self.situation == 'dead':
            if not freeze:
                self.projectiles.update(dt, rect_player)
            self.projectiles.draw(UI.screen)
            self.destroy()
