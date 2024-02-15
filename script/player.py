import pygame as pg
from math import pi, cos, sin
from settings import UI
from clock import Clock
from shield import Shield
from projectiles import Projectiles
from path import path


class Player(pg.sprite.Sprite):
    player_animations = {'resurrect': [pg.image.load(path(f'Fighter/destroy/destroy{i}.png')).convert_alpha() for i in range(15, 1-1, -1)],
                         'destroy': [pg.image.load(path(f'Fighter/destroy/destroy{i}.png')).convert_alpha() for i in range(1, 15+1)],
                         'damage': [pg.image.load(path(f'Fighter/damage/damage{i}.png')).convert_alpha() for i in range(1, 9+1)],
                         'evasion': [pg.image.load(path(f'Fighter/evasion/evasion{i}.png')).convert_alpha() for i in range(1, 8+1)],
                         'boost_attack1': [pg.image.load(path(f'Fighter/boost_attack1/boost_attack1.{i}.png')).convert_alpha() for i in range(1, 4+1)],
                         'boost_attack2': [pg.image.load(path(f'Fighter/boost_attack2/boost_attack2.{i}.png')).convert_alpha() for i in range(1, 2+1)],
                         'move_attack1': [pg.image.load(path(f'Fighter/move_attack1/move_attack1.{i}.png')).convert_alpha() for i in range(1, 4+1)],
                         'move_attack2': [pg.image.load(path(f'Fighter/move_attack2/move_attack2.{i}.png')).convert_alpha() for i in range(1, 2+1)],
                         'attack1': [pg.image.load(path(f'Fighter/attack1/attack1.{i}.png')).convert_alpha() for i in range(1, 4+1)],
                         'attack2': [pg.image.load(path(f'Fighter/attack2/attack2.{i}.png')).convert_alpha() for i in range(1, 2+1)],
                         'boost': [pg.image.load(path(f'Fighter/boost/boost{i}.png')).convert_alpha() for i in range(1, 5+1)],
                         'move': [pg.image.load(path(f'Fighter/move/move{i}.png')).convert_alpha() for i in range(1, 6+1)],
                         'idle': pg.image.load(path('Fighter/idle/idle1.png')).convert_alpha()}

    def __init__(self, weapon: int) -> None:
        super().__init__()
        self.weapons_info = {'weapon1': {'damage': 2.5,
                                         'attack_speed': 2,
                                         'bullet_speed': 14},
                             'weapon2': {'damage': 1,
                                         'attack_speed': 5,
                                         'bullet_speed': 20}}

        self.weapon = weapon

        self.damage = self.weapons_info[f'weapon{self.weapon}']['damage']
        self.attack_speed = self.weapons_info[f'weapon{self.weapon}']['attack_speed']
        self.bullet_speed = self.weapons_info[f'weapon{self.weapon}']['bullet_speed']

        self.max_health = 100
        self.health = self.max_health
        self.regen = 0
        self.regeneration = False
        self.max_stamina = 100
        self.stamina = self.max_stamina
        self.stamina_use = 2
        self.stamina_regen = 1
        self.stamina_cooldown = 2
        self.dodge_cooldown = 8
        self.dodge_duration = 1
        self.energy = 1
        self.spin = 3
        self.angle = 0
        self.max_velocity = 5
        self.velocity = 0
        self.acceleration = 0.6
        self.boost = self.acceleration * 1.5
        self.stopwatch_boost = 1

        self.friction = 0.1

        self.buff_cooldown = 5000
        self.buff_duration = 5000
        self.stopwatch_buff = 0
        self.buffed = False

        self.dodge_freeze = 4
        self.start_clock = False
        self.dodge_free = False
        self.dodge_count = 0

        self.shield = Shield()
        self.shielded = False
        self.shield_cooldown = 20000
        self.shield_count = 0
        self.shield_max = 1
        self.stopwatch_shield = 0

        self.xp = 0
        self.lvl = 0
        self.max_xp = int(self.lvl/2+3)

        self.res_heal = 0
        self.res_count = 0
        self.resurrection = False
        self.stopwatch_res = 0
        self.res_wait = 1

        self.fullLife = True
        self.situation = 'alive'
        self.collide = False
        self.blinked = False

        self.scale = UI.scale * 1.5

        self.blink_color = {'white': (255, 255, 255),
                            'green': (203, 242, 87),
                            'blue': (37, 142, 193)}
        self.current_color = 'white'

        self.index = {'id_resurrect': 0,
                      'id_destroy': 0,
                      'id_damage': 0,
                      'id_evasion': 0,
                      'id_attack1': 0,
                      'id_attack2': 0,
                      'id_boost': 0,
                      'id_move': 0}

        self.status = {'is_resurrected': False,
                       'is_destroyed': False,
                       'is_damaged': False,
                       'is_evasioned': False,
                       'is_attacked': False,
                       'is_boosted': False,
                       'is_moved': False}

        self.image = Player.player_animations['idle']
        self.rect = self.image.get_rect(center=UI.center)
        self.mask = pg.mask.from_surface(self.image)

        self.update_animation_time()

        self.projectiles = pg.sprite.Group()
        self.clock_animation = Clock(self.animations_time['resurrect_speed'])

    def update_animation_time(self):
        self.animations_time = {'resurrect_speed': 1.75,
                                'destroy_speed': 1.5,
                                'damage_speed': 1,
                                'evasion_speed': self.dodge_duration,
                                'attack_speed': 1/self.attack_speed,
                                'boost_speed': 1,
                                'move_speed': 1,
                                'blink_speed': 0.4}

    def player_inputs(self, dt) -> None:
        if not self.status['is_damaged']:
            keys = pg.key.get_pressed()
            if keys[pg.K_a] or keys[pg.K_LEFT]:
                self.angle += self.spin * dt
            if keys[pg.K_d] or keys[pg.K_RIGHT]:
                self.angle -= self.spin * dt
            if keys[pg.K_w] or keys[pg.K_UP]:
                self.velocity += self.acceleration
                self.status['is_moved'] = True
            if keys[pg.K_LSHIFT] and self.stamina > 0:
                self.velocity += self.boost
                self.status['is_boosted'] = True
            if keys[pg.K_LCTRL] and not self.status['is_evasioned'] and self.energy >= 1:
                self.status['is_evasioned'] = True
            if (keys[pg.K_SPACE] or keys[pg.K_f]) and not self.status['is_attacked']:
                self.status['is_attacked'] = True

    def apply_boost(self, dt):
        if self.status['is_boosted']:
            self.max_velocity += self.boost
            if self.max_velocity >= 8:
                self.max_velocity = 8
            self.stamina -= self.stamina_use
            if self.stamina <= 0:
                self.stamina = 0
            self.stopwatch_boost = 1
        else:
            self.stopwatch_boost -= 1 / \
                (max(UI.clock.get_fps(), 1) * self.stamina_cooldown)
            if self.stopwatch_boost <= 0:
                self.stamina += self.stamina_regen
            self.max_velocity -= self.friction * 1.5 * dt
            if self.max_velocity <= 5:
                self.max_velocity = 5
            if self.stamina >= self.max_stamina:
                self.stamina = self.max_stamina

    def movement_forwards(self, dt) -> None:
        if self.velocity > self.max_velocity:
            self.velocity = self.max_velocity
        elif self.velocity < 0:
            self.velocity = 0
        self.rect.centerx += self.velocity * \
            cos((self.angle*pi/180)) * dt
        self.rect.centery -= self.velocity * \
            sin((self.angle*pi/180)) * dt
        self.velocity -= self.friction * dt

    def check_evasion(self):
        if self.status['is_evasioned']:
            self.energy -= 1/(max(UI.clock.get_fps(), 1) * self.dodge_duration)
            if self.energy <= 0:
                self.energy = 0
        else:
            self.energy += 1/(max(UI.clock.get_fps(), 1) * self.dodge_cooldown)
            if self.energy >= 1:
                self.energy = 1

    def count_evasion(self):
        if not self.status['is_evasioned']:
            self.dodge_free = True
        if self.dodge_free and self.status['is_evasioned']:
            self.dodge_free = False
            self.dodge_count += 1
            if self.dodge_count >= self.dodge_freeze:
                self.dodge_count = 0
                return True
        return False

    def buff(self, time, atkSPD_buff, bulletSPD_buff):
        if not self.buffed:
            if self.status['is_attacked']:
                self.stopwatch_buff = time
            if time - self.stopwatch_buff >= self.buff_cooldown:
                self.collide = True
                self.current_color = 'green' if self.weapon == 1 else 'blue'
                self.attack_speed *= atkSPD_buff
                self.bullet_speed *= bulletSPD_buff
                self.stopwatch_buff = time
                self.buffed = True
        else:
            if time - self.stopwatch_buff >= self.buff_duration:
                self.attack_speed /= atkSPD_buff
                self.bullet_speed /= bulletSPD_buff
                self.stopwatch_buff = time
                self.buffed = False

    def spawn_projectiles(self) -> None:
        self.projectiles.add(Projectiles(self.angle, self.rect.centerx, self.rect.centery,
                             f'player{self.weapon}', self.scale, self.damage, self.bullet_speed))

    def repositioning(self) -> None:
        if self.rect.top > UI.dimension[1]:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.top = UI.dimension[1]
        elif self.rect.left > UI.dimension[0]:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = UI.dimension[0]

    def regenerate(self):
        if self.regeneration:
            if self.health < self.max_health:
                self.health += (1/(max(UI.clock.get_fps(), 1))
                                * self.regen * self.health)

    def hit(self, damage):
        if damage == 0:
            self.xp += 1
            if self.xp >= self.max_xp and self.lvl < 20:
                self.xp = 0
                self.lvl += 1
                self.max_xp = int(self.lvl/2+3)
                return True
        elif self.status['is_evasioned'] or self.situation != 'alive':
            return False
        elif self.shielded:
            self.shield_count += 1
            if self.shield_count >= self.shield_max:
                self.shield.change('break')
            return True
        else:
            self.health -= damage
            self.collide = True
            self.current_color = 'white'
            return True

    def spawn_shield(self, time):
        if not self.shielded:
            if time - self.stopwatch_shield >= self.shield_cooldown:
                self.shield_count = 0
                self.shield.change('spawn')
                self.shielded = True
        else:
            if self.shield.animation(self.rect.center):
                self.shielded = False
                self.stopwatch_shield = time

    def verification_health(self):
        if self.health <= self.max_health*0.5 and self.fullLife:
            self.status['is_damaged'] = True
            self.fullLife = False
        if self.health <= 0:
            self.situation = 'dying'
            self.health = 0
            self.status['is_destroyed'] = True
            self.alpha = 255

    def resurrect(self):
        if self.resurrection:
            self.stopwatch_res += 1 / \
                (max(UI.clock.get_fps(), 1) * self.res_wait)
            if self.stopwatch_res >= 1:
                self.stopwatch_res = 0
                self.status['is_resurrected'] = True
                self.resurrection = False

    def destroy(self) -> None:
        pass

    def get_info(self):
        return {'max_health': self.max_health,
                'health': self.health,
                'max_stamina': self.max_stamina,
                'stamina': self.stamina,
                'dodge': self.energy,
                'max_xp': self.max_xp,
                'xp': self.xp}

    def animation_state(self) -> None:
        if not self.status['is_moved'] and not self.status['is_boosted']:
            self.index['id_move'] = 0
            self.index['id_boost'] = 0

        if self.situation == 'alive':
            self.current_image = self.player_animations['idle']
            if self.status['is_damaged']:
                self.start_animation('damage', 'id_damage',
                                     'damage_speed', 'is_damaged')

            elif self.status['is_evasioned']:
                self.start_animation('evasion', 'id_evasion',
                                     'evasion_speed', 'is_evasioned')

            elif self.status['is_attacked'] and self.status['is_boosted']:
                if self.start_animation(f'boost_attack{self.weapon}', f'id_attack{self.weapon}',
                                        'attack_speed', 'is_attacked'):
                    self.spawn_projectiles()
                self.status['is_boosted'] = False

            elif self.status['is_attacked'] and self.status['is_moved']:
                if self.start_animation(f'move_attack{self.weapon}', f'id_attack{self.weapon}',
                                        'attack_speed', 'is_attacked'):
                    self.spawn_projectiles()
                self.status['is_moved'] = False

            elif self.status['is_attacked']:
                if self.start_animation(f'attack{self.weapon}', f'id_attack{self.weapon}',
                                        'attack_speed', 'is_attacked'):
                    self.spawn_projectiles()

            elif self.status['is_boosted']:
                self.start_animation('boost', 'id_boost',
                                     'boost_speed', 'is_boosted')
                self.status['is_boosted'] = False

            elif self.status['is_moved']:
                self.start_animation(
                    'move', 'id_move', 'move_speed', 'is_moved')
                self.status['is_moved'] = False
        else:
            if self.status['is_resurrected']:
                if self.start_animation('resurrect', 'id_resurrect',
                                        'resurrect_speed', 'is_resurrected'):
                    self.situation = 'alive'
                    self.res_count += 1
                self.clock_animation.animation('back')
                self.health += self.max_health*self.res_heal / \
                    (max(UI.clock.get_fps(), 1) *
                     self.animations_time['resurrect_speed'])

            elif self.status['is_destroyed']:
                if self.start_animation('destroy', 'id_destroy',
                                        'destroy_speed', 'is_destroyed'):
                    if self.res_heal and self.res_count <= 0:
                        self.resurrection = True
                    else:
                        self.situation = 'dead'

    def start_animation(self, action, step, speed, condition) -> bool:
        self.current_image = Player.player_animations[action][int(
            self.index[step])]
        self.index[step] += len(Player.player_animations[action]) / \
            (max(UI.clock.get_fps(), 1) * self.animations_time[speed])
        if self.index[step] >= len(Player.player_animations[action]):
            self.index[step] = 0
            self.status[condition] = False
            return True
        return False

    def att_sprite(self) -> None:
        self.image = pg.transform.rotozoom(
            self.current_image, self.angle, self.scale)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pg.mask.from_surface(self.image)

    def blink(self) -> None:
        if self.collide:
            if self.current_color == 'green':
                self.alpha = 200
            elif self.current_color == 'white':
                self.alpha = 255
            elif self.current_color == 'blue':
                self.alpha = 200
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

    def att_projectiles(self, dt) -> None:
        self.projectiles.update(dt)
        self.projectiles.draw(UI.screen)

    def update(self, dt, events) -> None:
        if self.situation == 'alive':
            self.update_animation_time()
            self.player_inputs(dt)
            self.apply_boost(dt)
            self.movement_forwards(dt)
            self.regenerate()
            self.check_evasion()
            self.repositioning()
            self.verification_health()
            self.animation_state()
            self.att_sprite()
            self.att_projectiles(dt)
            self.blink()
        elif self.situation == 'dying':
            self.update_animation_time()
            self.apply_boost(dt)
            self.movement_forwards(dt)
            self.repositioning()
            self.animation_state()
            self.att_sprite()
            self.att_projectiles(dt)
            self.resurrect()
        elif self.situation == 'dead':
            self.destroy()
