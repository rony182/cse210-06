import csv
from ctypes.wintypes import POINT
from random import randint
from constants import *
from game.casting.animation import Animation
from game.casting.body import Body
from game.casting.zombie import Zombie
from game.casting.bullet import Bullet
from game.casting.image import Image
from game.casting.label import Label
from game.casting.player import Player
from game.casting.point import Point
from game.casting.stats import Stats
from game.casting.text import Text 
from game.scripting.add_zombie_action import AddZombieAction
from game.scripting.change_scene_action import ChangeSceneAction
from game.scripting.collide_borders_action import CollideBordersAction
from game.scripting.collide_zombie_action import CollideZombieAction
from game.scripting.collide_bullet_action import CollideBulletAction
from game.scripting.control_player_action import ControlPlayerAction
from game.scripting.control_bullet_action import ControlBulletAction
from game.scripting.draw_bullet_action import DrawBulletAction
from game.scripting.draw_dialog_action import DrawDialogAction
from game.scripting.draw_hud_action import DrawHudAction
from game.scripting.draw_sprite_action import DrawSpriteAction
from game.scripting.draw_player_action import DrawPlayerAction
from game.scripting.draw_zombies_action import DrawZombiesAction
from game.scripting.end_drawing_action import EndDrawingAction
from game.scripting.initialize_devices_action import InitializeDevicesAction
from game.scripting.load_assets_action import LoadAssetsAction
from game.scripting.move_bullet_action import MoveBulletAction
from game.scripting.move_zombie_action import MoveZombieAction
from game.scripting.play_sound_action import PlaySoundAction
from game.scripting.release_devices_action import ReleaseDevicesAction
from game.scripting.start_drawing_action import StartDrawingAction
from game.scripting.timed_change_scene_action import TimedChangeSceneAction
from game.scripting.unload_assets_action import UnloadAssetsAction
from game.scripting.change_player_action import ChangePlayerAction
from game.services.raylib.raylib_audio_service import RaylibAudioService
from game.services.raylib.raylib_keyboard_service import RaylibKeyboardService
from game.services.raylib.raylib_physics_service import RaylibPhysicsService
from game.services.raylib.raylib_video_service import RaylibVideoService
from game.services.physics_service import PhysicsService



class SceneManager:
    """The person in charge of setting up the cast and script for each scene."""
    
    AUDIO_SERVICE = RaylibAudioService()
    KEYBOARD_SERVICE = RaylibKeyboardService()
    PHYSICS_SERVICE = RaylibPhysicsService()
    VIDEO_SERVICE = RaylibVideoService(GAME_NAME, SCREEN_WIDTH, SCREEN_HEIGHT)

    ADD_ZOMBIE_ACTION = AddZombieAction(VIDEO_SERVICE)
    COLLIDE_BORDERS_ACTION = CollideBordersAction(PHYSICS_SERVICE, AUDIO_SERVICE)
    COLLIDE_ZOMBIE_ACTION = CollideZombieAction(PHYSICS_SERVICE, AUDIO_SERVICE)
    COLLIDE_BULLET_ACTION = CollideBulletAction(PHYSICS_SERVICE, AUDIO_SERVICE)
    CONTROL_PLAYER_ACTION = ControlPlayerAction(KEYBOARD_SERVICE)
    CONTROL_BULLET_ACTION = ControlBulletAction(KEYBOARD_SERVICE)
    # CHANGE_PLAYER_ACTION = ChangePlayerAction(KEYBOARD_SERVICE)
    DRAW_BULLET_ACTION = DrawBulletAction(VIDEO_SERVICE)
    DRAW_DIALOG_ACTION = DrawDialogAction(VIDEO_SERVICE)
    DRAW_HUD_ACTION = DrawHudAction(VIDEO_SERVICE)
    DRAW_PLAYER_ACTION = DrawPlayerAction(VIDEO_SERVICE)
    DRAW_SPRITE_ACTION = DrawSpriteAction(VIDEO_SERVICE)
    DRAW_ZOMBIES_ACTION = DrawZombiesAction(VIDEO_SERVICE)
    END_DRAWING_ACTION = EndDrawingAction(VIDEO_SERVICE)
    INITIALIZE_DEVICES_ACTION = InitializeDevicesAction(AUDIO_SERVICE, VIDEO_SERVICE)
    LOAD_ASSETS_ACTION = LoadAssetsAction(AUDIO_SERVICE, VIDEO_SERVICE)
    MOVE_BULLET_ACTION = MoveBulletAction(PHYSICS_SERVICE, AUDIO_SERVICE)
    MOVE_ZOMBIE_ACTION = MoveZombieAction()
    RELEASE_DEVICES_ACTION = ReleaseDevicesAction(AUDIO_SERVICE, VIDEO_SERVICE)
    START_DRAWING_ACTION = StartDrawingAction(VIDEO_SERVICE)
    UNLOAD_ASSETS_ACTION = UnloadAssetsAction(AUDIO_SERVICE, VIDEO_SERVICE)

    ########

    STATS = Stats()

    # -----------------------
    # SCENE CONSTANTS
    # -----------------------

    # NEW GAME SCENE
    SCENE_0_NAME = "Zombie Invasion"
    START_GAME = "Press ENTER to play"
    HOW_TO_PLAY = "Press H for help"

    # HOW TO PLAY SCENE
    SCENE_1_NAME = "How to play"

    INSTRUCTIONS = f"1# Choose a character to start playing\n"\
    f"2# Move the character to left or right with the arrow keys\n"\
    f"3# Press the space bar to shoot the zombies\n"\
    f"!! You will lose a life if you get bitten by a zombie\n"\
    f"!! You will lose a life if 10 or more zombies walk past you\n"\
    f"GOOD LUCK AND STAY ALIVE!"

    SCORE_TABLE = f"Zombie 1 10 points\n"\
        f"Zombie 2  20 points\n"\
        f"Zombie 3  30 points\n"\
        f"Zombie 4  40 points\n"\

    # PLAYER SELECTION SCENE
    SCENE_2_NAME = "Choose your character"
    SELECT_CHARACTER = "Press ENTER to start"
    PREVIOUS_CHARACTER = "Previous"
    NEXT_CHARACTER = "Next"

    # GAME OVER SCENE:
    SCORE = F"Score {STATS.get_score()}"

    # Player Image Filepath
    PLAYER_FILEPATH = "zombie_invasion\\assets\\images\\player_1_30px.png"

    def __init__(self):
        pass

    def prepare_scene(self, scene, cast, script):
        if scene == NEW_GAME:
            self._prepare_new_game(cast, script)
        elif scene == HOW_TO_PLAY:
             self._prepare_how_to_play(cast, script)
        elif scene == PLAYER_SELECTION:
            self._prepare_player_selection(cast, script)
        elif scene == IN_PLAY:
            self._prepare_in_play(cast, script)
        elif scene == YOU_WIN:
            self._prepare_you_win(cast, script)
        elif scene == GAME_OVER:    
            self._prepare_game_over(cast, script)
    
    # ----------------------------------------------------------------------------------------------
    # scene methods
    # ----------------------------------------------------------------------------------------------
    
    def _prepare_new_game(self, cast, script):

        cast.clear_actors(DIALOG_GROUP)
        self._add_dialog(cast, self.SCENE_0_NAME, CENTER_X, 100)
        self._add_dialog(cast, self.START_GAME)
        # Adds video and audio service initialization
        self._add_initialize_script(script)
        # Adds assets
        self._add_load_script(script)
        script.clear_actions(INPUT)
        script.add_action(INPUT, ChangeSceneAction(self.KEYBOARD_SERVICE, HOW_TO_PLAY))
        
        self._add_output_script(script)
        self._add_unload_script(script)
        self._add_release_script(script)
        # script.add_action(OUTPUT, PlaySoundAction(self.AUDIO_SERVICE, BACKGROUND_MENU))
        
    def _prepare_how_to_play(self, cast, script):
        
        cast.clear_actors(DIALOG_GROUP)
        self._add_dialog(cast, self.SCENE_1_NAME, CENTER_X, 100)
        self._add_dialog(cast, self.INSTRUCTIONS, CENTER_X, 185)
        self._add_dialog(cast, self.SCORE_TABLE, CENTER_X, CENTER_Y + 150)

        script.clear_actions(INPUT)
        script.add_action(INPUT, ChangeSceneAction(self.KEYBOARD_SERVICE, PLAYER_SELECTION))

    def _prepare_player_selection(self, cast, script):
        cast.clear_actors(DIALOG_GROUP)
        self._add_dialog(cast, self.SCENE_2_NAME, CENTER_X, 100)
        self._add_dialog(cast, self.PREVIOUS_CHARACTER, 100, CENTER_Y)
        self._add_dialog(cast, self.NEXT_CHARACTER, SCREEN_WIDTH - 100)
        self._add_dialog(cast, self.SELECT_CHARACTER, CENTER_X, SCREEN_HEIGHT - 100)

        # Cast all images under "Sprites" list:
        for i in range(0, 4):
            img = Image(PLAYER_IMAGES_BIG[i])
            cast.add_actor(SPRITES_GROUP, img)

        # Call the ChangePlayerAction class:
        


        script.clear_actions(INPUT)
        script.add_action(INPUT, ChangeSceneAction(self.KEYBOARD_SERVICE, IN_PLAY))
        self._add_output_script(script)
        script.add_action(OUTPUT, self.DRAW_SPRITE_ACTION)
        script.add_action(OUTPUT, PlaySoundAction(self.AUDIO_SERVICE, WELCOME_SOUND))
        
        
    def _prepare_in_play(self, cast, script):
        # Clear all previous dialogs
        cast.clear_actors(DIALOG_GROUP)
        cast.clear_actors(SPRITES_GROUP)
        # Add the player
        self._add_player(cast)
        # Add the zombies
        self._add_zombies(cast)

        cast.add_actor(STATS_GROUP, self.STATS)
        score_lbl = Label(Text(""), Point(SCORE_MARGIN, HUD_MARGIN))
        lives_lbl = Label(Text(""), Point(LIVES_MARGIN, HUD_MARGIN))
        cast.add_actor(SCORE_GROUP, score_lbl)
        cast.add_actor(LIVES_GROUP, lives_lbl)
        script.add_action(OUTPUT, PlaySoundAction(self.AUDIO_SERVICE, BACKGROUND_SOUND))

        # Clear previous INPUT actions
        script.clear_actions(INPUT)
        # Add the CONTROL_PLAYER_ACTION to make the player go left or right
        script.add_action(INPUT, self.CONTROL_BULLET_ACTION)
        script.add_action(INPUT, self.CONTROL_PLAYER_ACTION)
        # Add the MOVE_ZOMBIE_ACTION to make zombies go down automatically
        script.add_action(UPDATE, self.MOVE_ZOMBIE_ACTION)
        script.add_action(UPDATE, self.MOVE_BULLET_ACTION)
        # Add the collision action between Zombie and Player
        script.add_action(UPDATE, self.COLLIDE_ZOMBIE_ACTION)
        script.add_action(UPDATE, self.COLLIDE_BULLET_ACTION)
        script.add_action(UPDATE, self.ADD_ZOMBIE_ACTION)
        # Add the colission action with the borders
        script.add_action(UPDATE, self.COLLIDE_BORDERS_ACTION)
        # Add the DRAW_PLAYER and DRAW_ZOMBIES actions to make them appear
        script.add_action(OUTPUT, self.DRAW_HUD_ACTION)
        script.add_action(OUTPUT, self.DRAW_PLAYER_ACTION)
        script.add_action(OUTPUT, self.DRAW_ZOMBIES_ACTION)
        script.add_action(OUTPUT, self.DRAW_BULLET_ACTION)

    def _prepare_you_win(self, cast, script):
        pass

    def _prepare_game_over(self, cast, script):
        # self._add_bullet(cast)
        self._add_player(cast)
        self._add_dialog(cast, self.SCORE, CENTER_X, 100)
        self._add_dialog(cast, WAS_GOOD_GAME)
        self._add_dialog(cast, "Press ENTER to play again", CENTER_X, SCREEN_HEIGHT - 100)

        script.clear_actions(INPUT)
        script.clear_actions(UPDATE)
        script.add_action(INPUT, ChangeSceneAction(self.KEYBOARD_SERVICE, IN_PLAY))
        self._add_output_script(script)

        self.STATS.reset()

    # ----------------------------------------------------------------------------------------------
    # casting methods
    # ----------------------------------------------------------------------------------------------

    def _add_zombies(self, cast):
        # Clear any previous zombies from Cast
        cast.clear_actors(ZOMBIE_GROUP)
        
        for _ in range(ZOMBIE_MAX_NUMBER):

            i = randint(0, 3)
            img = Image(ZOMBIE_IMAGES[i])
            # Get random positions for the zombie to appear
            y = randint(0, 200)
            x = randint(0, SCREEN_WIDTH)
            # Create the Zombie body
            body = Body(Point(x, y), Point(ZOMBIE_WIDTH, ZOMBIE_HEIGHT), Point(0, ZOMBIE_VELOCITY))
            # Create Zombie
            zombie = Zombie(body, img, (i + 1) * 10)
            # Add Zombie to the cast
            cast.add_actor(ZOMBIE_GROUP, zombie)

    def _add_dialog(self, cast, message, x = CENTER_X, y = CENTER_Y):
        text = Text(message, FONT_FILE, FONT_SMALL, ALIGN_CENTER)
        position = Point(x, y)
        label = Label(text, position)
        cast.add_actor(DIALOG_GROUP, label)

    def _add_lives(self, cast):
        cast.clear_actors(LIVES_GROUP)
        text = Text(LIVES_FORMAT, FONT_FILE, FONT_SMALL, ALIGN_RIGHT)
        position = Point(SCREEN_WIDTH - HUD_MARGIN, HUD_MARGIN)
        label = Label(text, position)
        cast.add_actor(LIVES_GROUP, label)

    def _add_score(self, cast):
        cast.clear_actors(SCORE_GROUP)
        text = Text(SCORE_FORMAT, FONT_FILE, FONT_SMALL, ALIGN_CENTER)
        position = Point(CENTER_X, HUD_MARGIN)
        label = Label(text, position)
        cast.add_actor(SCORE_GROUP, label)

    def _add_stats(self, cast):
        cast.clear_actors(STATS_GROUP)
        stats = Stats()
        cast.add_actor(STATS_GROUP, stats)

    def _add_player(self, cast):
        cast.clear_actors(PLAYER_GROUP)
        x = CENTER_X - PLAYER_WIDTH / 2
        y = SCREEN_HEIGHT - PLAYER_HEIGHT
        position = Point(x, y)
        size = Point(PLAYER_WIDTH, PLAYER_HEIGHT)
        velocity = Point(0, 0)
        body = Body(position, size, velocity)
        # bullet = Bullet(body, self.BULLET_FILEPATH)
        #animation = Animation(PLAYER_IMAGES, PLAYER_RATE)
        image = Image(self.PLAYER_FILEPATH)
        player = Player(body, image)
        cast.add_actor(PLAYER_GROUP, player)
        # cast.add_actor(PLAYER_GROUP, bullet)

    # ----------------------------------------------------------------------------------------------
    # scripting methods
    # ----------------------------------------------------------------------------------------------
    def _add_initialize_script(self, script):
        script.clear_actions(INITIALIZE)
        script.add_action(INITIALIZE, self.INITIALIZE_DEVICES_ACTION)

    def _add_load_script(self, script):
        script.clear_actions(LOAD)
        script.add_action(LOAD, self.LOAD_ASSETS_ACTION)
    
    def _add_output_script(self, script):
        script.clear_actions(OUTPUT)
        script.add_action(OUTPUT, self.START_DRAWING_ACTION)
        script.add_action(OUTPUT, self.DRAW_DIALOG_ACTION)
        script.add_action(OUTPUT, self.END_DRAWING_ACTION)

    def _add_release_script(self, script):
        script.clear_actions(RELEASE)
        script.add_action(RELEASE, self.RELEASE_DEVICES_ACTION)
    
    def _add_unload_script(self, script):
        script.clear_actions(UNLOAD)
        script.add_action(UNLOAD, self.UNLOAD_ASSETS_ACTION)
        
    def _add_update_script(self, script):
        script.clear_actions(UPDATE)
        script.add_action(UPDATE, self.MOVE_BULLET_ACTION)
        script.add_action(UPDATE, self.CONTROL_PLAYER_ACTION)
        script.add_action(UPDATE, self.COLLIDE_BORDERS_ACTION)
        script.add_action(UPDATE, self.COLLIDE_ZOMBIE_ACTION)
        script.add_action(UPDATE, self.COLLIDE_BULLET_ACTION)
        script.add_action(UPDATE, self.DRAW_BULLET_ACTION)