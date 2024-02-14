import pygame as pg
from settings import UI
from player import Player
from enemies import Enemy
from experience import Experience
from explosion import Explosion
from cards import Cards
from hud import Hud
from button import Button
from transition import Transition
from sounds import Sounds
from path import path


class Level():
    def __init__(self, gameStateManager, saveManager, request) -> None:
        self.gameStateManager = gameStateManager
        self.saveManager = saveManager
        self.request = request

        self.sound = Sounds(['Laser.ogg',
                             'Neon.ogg',
                             'Nota.ogg',
                             'Sandblaster.ogg',
                             'Action.ogg',
                             'Concentration.ogg',
                             'Industrial.ogg'])
        self.soundDead = Sounds(['GameOver.ogg'])

        background_surf = pg.image.load(
            path('Images/backStars.png')).convert_alpha()
        self.background_surf = pg.transform.scale(
            background_surf, UI.dimension)

        self.dark_background = pg.surface.Surface(
            self.background_surf.get_size(), pg.SRCALPHA)
        self.dark_background.fill((0, 0, 0, 150))
        self.dark_death = pg.surface.Surface(
            self.background_surf.get_size(), pg.SRCALPHA)
        self.darkness = 0

        self.freeze_bg = pg.surface.Surface(UI.dimension, pg.SRCALPHA)
        for r in range(50):
            alpha = int(150 - r*150/50)
            self.freeze_bg.fill((173, 216, 230, alpha),
                                (r, r, UI.dimension[0]-r*2, UI.dimension[1]-r*2))

        self.flash_duration = 0.5
        self.flash_alpha = 0

        self.score = 0

        self.fade = Transition()
        self.transition = False

        buttons_tutorial1 = [
            Button('W', UI.fonts['sm'], UI.half_width *
                   0.7, UI.half_height - 175, 0, 'button'),
            Button(UI.display_text(
                'control1'), UI.fonts['sm'], UI.half_width*0.7, UI.half_height - 135, 0, 'text'),
            Button('A', UI.fonts['sm'], UI.half_width *
                   1, UI.half_height - 175, 0, 'button'),
            Button(UI.display_text(
                'control2.1'), UI.fonts['sm'], UI.half_width*1, UI.half_height - 135, 0, 'text'),
            Button('D', UI.fonts['sm'], UI.half_width *
                   1.3, UI.half_height - 175, 0, 'button'),
            Button(UI.display_text(
                'control2.2'), UI.fonts['sm'], UI.half_width*1.3, UI.half_height - 135, 0, 'text'),
            Button('LShift', UI.fonts['sm'], UI.half_width *
                   0.7, UI.half_height - 60, 0, 'button'),
            Button(UI.display_text(
                'control3'), UI.fonts['sm'], UI.half_width*0.7, UI.half_height - 20, 0, 'text'),
            Button('LCtrl', UI.fonts['sm'], UI.half_width *
                   1.3, UI.half_height - 60, 0, 'button'),
            Button(UI.display_text(
                'control4'), UI.fonts['sm'], UI.half_width*1.3, UI.half_height - 20, 0, 'text'),
            Button(UI.display_text('spacebar'),
                   UI.fonts['sm'], UI.half_width, UI.half_height - 60, 0, 'button'),
            Button(UI.display_text('control5'),
                   UI.fonts['sm'], UI.half_width, UI.half_height - 20, 0, 'text'),
            Button(UI.display_text('continue'),
                   UI.fonts['m'], UI.half_width, UI.half_height + 175, 4, 'menu')
        ]

        buttons_tutorial2 = [
            Button(UI.display_text('up'), UI.fonts['sm'], UI.half_width *
                   0.7, UI.half_height - 175, 0, 'button'),
            Button(UI.display_text(
                'control1'), UI.fonts['sm'], UI.half_width*0.7, UI.half_height - 135, 0, 'text'),
            Button(UI.display_text('left'), UI.fonts['sm'], UI.half_width *
                   1.0, UI.half_height - 175, 0, 'button'),
            Button(UI.display_text(
                'control2.1'), UI.fonts['sm'], UI.half_width*1, UI.half_height - 135, 0, 'text'),
            Button(UI.display_text('right'), UI.fonts['sm'], UI.half_width *
                   1.3, UI.half_height - 175, 0, 'button'),
            Button(UI.display_text(
                'control2.2'), UI.fonts['sm'], UI.half_width*1.3, UI.half_height - 135, 0, 'text'),
            Button('LShift', UI.fonts['sm'], UI.half_width *
                   0.7, UI.half_height - 60, 0, 'button'),
            Button(UI.display_text(
                'control3'), UI.fonts['sm'], UI.half_width*0.7, UI.half_height - 20, 0, 'text'),
            Button('LCtrl', UI.fonts['sm'], UI.half_width *
                   1.3, UI.half_height - 60, 0, 'button'),
            Button(UI.display_text(
                'control4'), UI.fonts['sm'], UI.half_width*1.3, UI.half_height - 20, 0, 'text'),
            Button(UI.display_text('spacebar'),
                   UI.fonts['sm'], UI.half_width, UI.half_height - 60, 0, 'button'),
            Button(UI.display_text('control5'),
                   UI.fonts['sm'], UI.half_width, UI.half_height - 20, 0, 'text'),
            Button(UI.display_text('continue'),
                   UI.fonts['m'], UI.half_width, UI.half_height + 175, 4, 'menu')
        ]

        buttons_game = [
            Button('| |', UI.fonts['m'],
                   UI.dimension[0] - 45, 45, 1, 'button'),
        ]

        buttons_pause = [
            Button(UI.display_text('resume'),
                   UI.fonts['m'], UI.half_width, UI.half_height-75, 2, 'menu'),
            Button(UI.display_text('skip_song'),
                   UI.fonts['m'], UI.half_width, UI.half_height, 5, 'menu'),
            Button('Menu', UI.fonts['m'], UI.half_width,
                   UI.half_height+75, 3, 'menu'),
        ]

        buttons_gameover = [
            Button(UI.display_text('deadmessage1'),
                   UI.fonts['m'], UI.half_width, UI.half_height - 150, 0, 'text'),
            Button(UI.display_text('deadmessage2'),
                   UI.fonts['m'], UI.half_width, UI.half_height - 100, 0, 'text'),
            Button('Menu', UI.fonts['m'], UI.half_width,
                   UI.half_height+150, 3, 'menu')
        ]

        buttons_level_up = [
            Button(UI.display_text('skip_lvl'),
                   UI.fonts['m'], UI.half_width, UI.half_height + 250, 6, 'menu'),
        ]

        button_empty = []

        self.buttons = {'buttons_tutorial1': buttons_tutorial1,
                        'buttons_tutorial2': buttons_tutorial2,
                        'buttons_game': buttons_game,
                        'buttons_level_up': buttons_level_up,
                        'buttons_pause': buttons_pause,
                        'buttons_gameover': buttons_gameover,
                        '': button_empty}

        self.current_buttons = 'buttons_tutorial1'
        self.pressed = False

        self.player = pg.sprite.GroupSingle()

        self.enemies = pg.sprite.Group()

        self.experience = pg.sprite.Group()
        self.up = False

        self.explosions = pg.sprite.Group()

        self.hud = Hud()

    def spawn_enemies(self) -> None:
        self.enemies_cooldown = -0.01 * \
            (self.time/60000)**2-0.2*(self.time/60000)+8
        if (self.time - self.stopwatch_enemy)/1000 > max(self.enemies_cooldown, 0.5):
            self.stopwatch_enemy = self.time
            self.enemies.add(Enemy((self.time/60000)))

    def collide(self) -> None:
        if self.player:
            # enemies and projectiles
            enemy_hit_projectiles = pg.sprite.groupcollide(
                self.enemies, self.player.sprite.projectiles, False, False, pg.sprite.collide_mask)
            for enemy, projectiles in enemy_hit_projectiles.items():
                if enemy.situation == 'alive':
                    for projectile in projectiles:
                        if enemy not in projectile.enemies_hit:
                            print(projectile.damage)
                            enemy.hit(projectile.damage)
                            if self.cards.owned['ignite']:
                                enemy.set_burn(self.burn_damage)
                            if self.cards.owned['atkDMG_special']:
                                self.player.sprite.health += projectile.damage*self.life_steel
                            projectile.enemies_hit.add(enemy)
                            projectile.change_damage(self.damage_reduction)
                            if len(projectile.enemies_hit) >= self.penetration:
                                projectile.kill()

            # enemies and explosion
            enemy_hit_explosion = pg.sprite.groupcollide(
                self.enemies, self.explosions, False, False, pg.sprite.collide_mask)
            for enemy, explosions in enemy_hit_explosion.items():
                if enemy.situation == 'alive':
                    for explosion in explosions:
                        if enemy not in explosion.enemies_hit:
                            enemy.hit(explosion.damage)
                            if self.cards.owned['explosion_special']:
                                enemy.set_electrocute(self.electrocute_damage)
                            explosion.enemies_hit.add(enemy)

            #enemies and resurrection
            if self.flash:
                if self.cards.owned['resurrection_special'] and self.player.sprite.res_count >= 1:
                    self.flash_surface = pg.surface.Surface(UI.dimension, pg.SRCALPHA)
                    self.flash_surface.fill((255, 255, 255, self.flash_alpha))
                    UI.screen.blit(self.flash_surface, (0,0))
                    self.flash_alpha += 200/(max(UI.clock.get_fps(), 1)*self.flash_duration)
                    if self.flash_alpha >= 200: 
                        self.flash_alpha = 200
                        self.flash_duration *= -1
                        for enemy in self.enemies:
                            if enemy.situation == 'alive':
                                enemy.hit(self.flash_damage*enemy.max_health)
                    elif self.flash_alpha < 0:
                        self.flash_alpha = 0
                        self.flash = False

            # player and projectiles
            for enemy in self.enemies:
                enemy_projectile = pg.sprite.spritecollide(
                    self.player.sprite, enemy.projectiles, False, pg.sprite.collide_mask)
                for projectile in enemy_projectile:
                    if self.player.sprite.hit(projectile.damage):
                        projectile.kill()

            # player and enemies
            collide_enemy = pg.sprite.spritecollide(
                self.player.sprite, self.enemies, False, pg.sprite.collide_mask)
            for enemy in collide_enemy:
                if enemy.situation == 'alive':
                    self.player.sprite.hit(0.1)

            # player and experience
            if pg.sprite.spritecollide(self.player.sprite, self.experience, True):
                level_up = self.player.sprite.hit(0)
                if level_up:
                    self.up = True
                    self.paused = True
                    self.cards.create_cards()
                    self.current_buttons = 'buttons_level_up'

    def enemies_health(self):
        for enemy in self.enemies:
            pos = enemy.verification_health()
            if pos:
                if self.player.sprite.lvl < 20: self.experience.add(Experience(pos))
                if self.cards.owned['explosion'] >= 1:
                    self.explosions.add(
                        Explosion(pos, self.cards.owned['explosion']))

    def check_dodge(self):
        if self.cards.owned['dodge_special'] >= 1:
            if self.player.sprite.count_evasion():
                self.stopwatch_freeze = self.time
            if self.time - self.stopwatch_freeze <= self.freeze_time:
                UI.screen.blit(self.freeze_bg, (0, 0))
                return True
        return False

    def check_buff(self):
        if self.cards.owned['atkSPD_special']:
            self.player.sprite.buff(self.time, self.atkSPD_buff, self.bulletSPD_buff)

    def check_shield(self):
        if self.cards.owned['shield']:
            self.player.sprite.spawn_shield(self.time)

    def upgrades(self, card):
        if card:
            if card == 'skip':
                pass
            elif card == 'hp':
                self.player.sprite.health += self.player.sprite.max_health*0.15
                self.player.sprite.max_health *= 1.15
            elif card == 'hp_special':
                self.player.sprite.regeneration = True
                self.player.sprite.regen = 0.001
            elif card == 'stamina':
                self.player.sprite.max_stamina *= 1.2
            elif card == 'stamina_special':
                self.player.sprite.stamina_use /= 2
                self.player.sprite.stamina_regen *= 2
            elif card == 'dodge':
                self.player.sprite.dodge_cooldown -= 1
            elif card == 'dodge_special':
                self.freeze_time = 2500
            elif card == 'resurrection':
                self.player.sprite.res_heal += 0.05
            elif card == 'resurrection_special':
                self.player.sprite.res_count -= 1
                self.flash = True
                self.flash_damage = 0.5
            elif card == 'shield':
                self.player.sprite.shield_cooldown -= 2500
            elif card == 'shield_special':
                self.player.sprite.shield_max = 3
            elif card == 'penetration':
                self.penetration += 1
                self.damage_reduction = 0.5
            elif card == 'penetration_special':
                self.damage_reduction = 1
            elif card == 'atkDMG':
                self.player.sprite.damage *= 1.15
            elif card == 'atkDMG_special':
                self.life_steel = 0.01
            elif card == 'atkSPD':
                self.player.sprite.attack_speed *= 1.1
                self.player.sprite.bullet_speed *= 1.1
            elif card == 'atkSPD_special':
                self.atkSPD_buff = 2
                self.bulletSPD_buff = 1.5
            elif card == 'ignite':
                self.burn_damage += 0.1
            elif card == 'ignite_special':
                self.burn_damage *= 2
                self.electrocute_damage *= 2
            elif card == 'explosion':
                pass 
            elif card == 'explosion_special':
                self.electrocute_damage = 0.50
                if self.cards.owned['ignite_special']:
                    self.electrocute_damage *= 2

            self.up = False
            self.current_buttons = 'buttons_game'
            self.paused = False

    def action(self, events) -> None:
        for event in events:
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                for button in self.buttons[self.current_buttons]:
                    act = button.collide()
                    if act:
                        if act == 1:
                            self.current_buttons = 'buttons_pause'
                            self.paused = True
                        elif act == 2 or act == 4:
                            self.current_buttons = 'buttons_game'
                            self.paused = False
                        elif act == 3:
                            self.paused = False
                            self.transition = True
                        elif act == 5:
                            self.sound.skip()
                            self.current_buttons = 'buttons_game'
                            self.paused = False
                        elif act == 6:
                            self.upgrades('skip')

    def tutorials(self):
        if self.stopwatch_time - self.stopwatch_tutorial >= 1500:
            self.current_buttons = 'buttons_tutorial2' if self.current_buttons == 'buttons_tutorial1' else 'buttons_tutorial1'
            self.stopwatch_tutorial = self.stopwatch_time

    def show_time(self):
        self.image_time_text = UI.fonts['l'].render(
            self.format_time(), False, (UI.colors['white']))
        self.rect_time_text = self.image_time_text.get_rect(
            center=(UI.half_width, 40))
        UI.screen.blit(self.image_time_text, self.rect_time_text)

    def format_time(self):
        seconds = self.time // 1000
        minutes = seconds // 60
        seconds %= 60
        milliseconds = self.time % 1000
        tempo_formatado = f"{minutes:02d}:{seconds:02d}"
        return tempo_formatado

    def save_score(self):
        if not self.saved:
            self.score = self.time // 1000
            data = self.saveManager.load()
            if self.score > data['score']:
                data['score'] = self.score
                self.saveManager.save(data)
                self.request.set_data(data)
            self.saved = True

    def dark_screen(self) -> None:
        self.dark_death.fill((0, 0, 0, self.darkness))
        UI.screen.blit(self.dark_death, (0, 0))
        if self.darkness < 200:
            self.darkness += 200/(max(UI.clock.get_fps(), 1) * 3)
        else:
            self.current_buttons = 'buttons_gameover'

    def fades(self) -> None:
        if self.fade.draw(self.transition):
            self.transition = False
            self.player.empty()
            self.enemies.empty()
            self.current_buttons = 'buttons_tutorial1'
            self.gameStateManager.set_state('menu')

    def reset(self):
        self.flash_damage = 0
        self.flash = False
        self.atkSPD_buff = 0
        self.bulletSPD_buff = 0
        self.electrocute_damage = 0
        self.burn_damage = 0
        self.life_steel = 0
        self.damage_reduction = 0
        self.penetration = 1
        self.freeze_time = 2000
        self.cards = Cards()
        self.darkness = 0
        self.saved = False
        self.paused = True
        self.time = 0
        self.stopwatch_enemy = 0
        self.stopwatch_freeze = 0
        self.stopwatch_tutorial = 0
        self.stopwatch_buff = 0
        self.stopwatch_time = pg.time.get_ticks()

        self.player.add(Player(self.gameStateManager.infos['weapon']))

    def run(self, dt, events) -> None:
        if not self.player:
            self.reset()
        
        if self.current_buttons in ['buttons_tutorial1','buttons_tutorial2']:
            self.tutorials()

        UI.screen.blit(self.background_surf, (0, 0))
        UI.screen.blit(self.dark_background, (0, 0))
        if self.paused:
            self.stopwatch_time = pg.time.get_ticks() - self.time
            self.dark_death.fill((0, 0, 0, 200))
            UI.screen.blit(self.dark_death, (0, 0))
            self.sound.pause()
        else:
            self.sound.unpause()
            self.show_time()
            self.player.update(dt, events)
            self.player.draw(UI.screen)
            self.spawn_enemies()
            self.experience.update()
            self.experience.draw(UI.screen)
            self.enemies.update(
                dt, self.time, self.player.sprite.rect.center, self.player.sprite.situation, self.check_dodge())
            self.enemies.draw(UI.screen)
            self.explosions.update()
            self.explosions.draw(UI.screen)
            self.hud.draw(self.player.sprite.get_info())
            self.check_buff()
            self.check_shield()
            self.enemies_health()
            self.collide()

            if self.player.sprite.situation == 'dying':
                if self.player.sprite.res_count >= 1:
                    self.sound.stop(1000)
                elif self.player.sprite.status['is_resurrected']:
                    self.sound.high_volume()
                else:
                    self.sound.low_volume()
            elif self.player.sprite.situation == 'dead':
                self.soundDead.play(self.transition)
                self.save_score()
                self.dark_screen()
            else:
                self.sound.reset()
                self.sound.play(self.transition)
                self.time = pg.time.get_ticks() - self.stopwatch_time

        if self.up:
            self.upgrades(self.cards.draw(events))
        for button in self.buttons[self.current_buttons]:
            button.draw()
        self.action(events)
        self.fades()
