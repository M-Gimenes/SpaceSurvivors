![banner](https://github.com/M-Gimenes/SpaceSurvivors/blob/master/Poster.png)

<div align="center">

# Space Survivors

**A top-down 2D space shooter built from scratch in Python — survive as long as possible, collect upgrades, and climb the global leaderboard.**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.x-00B140?style=flat)](https://www.pygame.org/)
[![Play on itch.io](https://img.shields.io/badge/Play%20on-itch.io-FA5C5C?style=flat&logo=itch.io&logoColor=white)](https://mgimenes.itch.io/space-survivors)

</div>

---

## Overview

Space Survivors started as a personal challenge to move beyond simple scripts and build something with real-time interactivity, physics, and visual feedback. The result is a complete game loop — from the main menu to a global leaderboard — with every system implemented in Python using the Pygame framework.

The project covers a wide range of software engineering concepts: object-oriented design, state machines, physics simulation, sprite animation, network communication, cryptographic save verification, and more. It is deployed as a standalone executable on **[itch.io](https://mgimenes.itch.io/space-survivors)** and includes a live backend for authentication, leaderboard, and auto-updates.

---

## Gameplay

You pilot a fighter ship through endless waves of enemy bombers. Your score is your **survival time** — enemies scale in health, damage, and speed as the match progresses. On each level-up, you choose one of four randomly offered upgrade cards to power up your ship.

### Controls

| Input                | Action                   |
| -------------------- | ------------------------ |
| **Mouse**      | Aim / rotate ship        |
| **Left Click** | Fire                     |
| **W**          | Accelerate forward       |
| **E**          | Boost (consumes stamina) |
| **Q**          | Evasion dodge            |

### Weapon Selection

Two weapons are available before each run, trading off damage for fire rate:

|                        | Weapon 1 | Weapon 2 |
| ---------------------- | -------- | -------- |
| **Damage**       | High     | Low      |
| **Attack Speed** | Slow     | Fast     |
| **Bullet Speed** | Medium   | High     |

A second weapon is locked until you survive 5 minutes, adding a progression layer to the meta-game.

---

## Upgrade System

On every level-up, four cards are drawn at random from your remaining pool. Each card belongs to one of two categories — **Attack** or **Defense** — and has a maximum of two slots per category. This forces meaningful build decisions.

| Category          | Upgrades                                                    |
| ----------------- | ----------------------------------------------------------- |
| **Attack**  | Explosion, Penetration, Attack Damage, Attack Speed, Ignite |
| **Defense** | HP, Stamina, Dodge, Resurrection, Shield                    |

Each upgrade can be stacked up to **level 4**, at which point it evolves into a **Special** variant with an altered or amplified effect:

- `Dodge` → `Dodge Special`: every 4 evasions triggers a **time freeze** around the player
- `Explosion` → `Explosion Special`: explosions apply an **electrocute** status to enemies
- `Resurrection` → `Resurrection Special`: upon death, releases a screen-wide **flash burst** for massive AoE damage
- `Attack Speed Special`: periodic **attack speed buff** on idle time
- `Attack Damage Special`: **lifesteal** on every bullet that deals damage
- ...and more

---

## Architecture & Technical Highlights

### Game Loop & Delta Time

The main loop runs at 60 FPS and passes a normalized `dt` (delta time) to every entity. All movement, physics, and animation speeds are `dt`-scaled, ensuring consistent behavior regardless of frame rate.

### State Machine

`GameStateManager` drives the entire application through discrete states: `menu`, `level`, `login`, `update`, and `offline`. Each state is a self-contained class with its own `run(dt, events)` method, making the flow easy to extend.

### Physics & Movement

The player ship uses a realistic feel with velocity, acceleration, friction, and angular rotation toward the mouse cursor. Boost consumes stamina with a cooldown before regeneration kicks in. Screen wrapping is handled at the edges.

### Animation System

Each entity (player and enemy) has a multi-state animation machine with independent frame counters:

**Player states:** `idle`, `move`, `boost`, `attack`, `move_attack`, `boost_attack`, `evasion`, `damage`, `destroy`, `resurrect`

**Enemy states:** `idle`, `move`, `attack`, `damage`, `destroy`

Animations are speed-controlled via the `dt`-normalized frame counter and paired with a **blink/flash effect** (white for damage, green/blue for buffs) drawn by filling the sprite's pixel mask.

### Collision Detection

Sprite groups and **pixel-perfect mask collision** (`collide_mask`) handle all interactions: player vs. enemy, projectile vs. enemy, projectile penetration, explosion radius, and experience orb pickup. Each projectile tracks which enemies it has already hit to correctly implement the penetration upgrade.

### Online Backend & Security

The game communicates with a REST API for several features:

- **Login & Nickname** — registered before the first run; stored server-side
- **Global Leaderboard** — top scores fetched and displayed in-game
- **Save Synchronization** — player data (score, settings, nickname) is persisted locally and synced to the server
- **RSA Save Integrity** — the save file is serialized with `pickle` and its **RSA-PSS/SHA-256 signature** is verified on every load. A tampered save is detected and deleted automatically, preventing cheating
- **Encrypted API Key** — the API key is never stored in plain text; it is fetched from the server and decrypted at runtime using the `Cryptograph` module
- **Auto-Updater** — on launch, the client compares its version against the server. If a new version exists, it downloads and hot-swaps the executable

A `@has_internet` decorator wraps every network call, gracefully redirecting the game to an `offline` state if the connection fails.

### Internationalization

The game automatically detects the system locale and loads either English (`en_US`) or Brazilian Portuguese (`pt_BR`). Language can also be changed manually through the options menu.

---

## Project Structure

```
script/
├── game.py              # Entry point, main loop
├── gameStateManager.py  # State machine
├── level.py             # Core gameplay: spawning, collision, upgrades
├── player.py            # Player entity: physics, animations, combat
├── enemies.py           # Enemy entity: AI, scaling, animations
├── cards.py             # Upgrade card system
├── projectiles.py       # Bullet logic and penetration
├── explosion.py         # AOE explosion sprites
├── hud.py               # Health, stamina, XP bars
├── menu.py              # Main menu, weapon select, rank, options
├── login.py             # Nickname registration screen
├── rank.py              # Leaderboard display
├── saveManager.py       # Local save + RSA signature verification
├── request.py           # REST API client with @has_internet decorator
├── cryptograph.py       # API key encryption/decryption
├── update.py            # In-game auto-updater
├── offline.py           # Offline fallback screen
├── transition.py        # Fade in/out effects
├── sounds.py            # Background music and SFX management
├── settings.py          # Global UI constants, fonts, i18n loader
├── languages.py         # en_US and pt_BR string tables
└── path.py              # Cross-platform asset path resolver
```

---

## Key Concepts Practiced

| Concept                        | Where                                                                       |
| ------------------------------ | --------------------------------------------------------------------------- |
| Object-Oriented Programming    | Every module is a class; entities use inheritance from `pg.sprite.Sprite` |
| State Machine Pattern          | `GameStateManager` + per-state `run()` method                           |
| Delta-Time Game Loop           | `dt = FPS / current_fps` applied to all physics and animations            |
| Sprite Groups & Mask Collision | `pg.sprite.Group`, `groupcollide`, `collide_mask`                     |
| Animation State Machine        | Per-entity status flags driving frame index progression                     |
| REST API Integration           | `requests` library with custom headers and streaming download             |
| Cryptography                   | RSA-PSS signature verification via `cryptography.hazmat`                  |
| Decorator Pattern              | `@has_internet` wraps all network methods                                 |
| Procedural Difficulty Scaling  | Enemy stats grow as a function of elapsed time                              |
| Internationalization           | Locale-based string table lookup                                            |

---


<div align="center">

*Developed for learning purposes — every system was built from scratch to understand the mechanics behind it.*

</div>
