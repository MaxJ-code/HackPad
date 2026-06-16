import board
import busio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.mouse_keys import MouseKeys
from kmk.extensions.display import Display
from kmk.extensions.display.ssd1306 import SSD1306
from kmk.handlers.sequences import simple_key_sequence


# Pin and Modules Definition
keyboard = KMKKeyboard()
keyboard.col_pins = (board.D10, board.D9, board.D8, board.D7)
keyboard.row_pins = (board.D0, board.D1, board.D2)
keyboard.diode_orientation = DiodeOrientation.COL2ROW
Encoder_handler = EncoderHandler()
Encoder_handler.pins = ((board.D3,board.D6,NONE),)
i2c_bus = busio.I2C(board.D5, board.D4)
driver = SSD1306(i2c=i2c_bus, device_address=0x3C)
display = Display(display_driver=driver, width=128, height=32, flip=False)
keyboard.modules.append(Layers())
keyboard.modules.append(Encoder_handler)
keyboard.modules.append(MediaKeys)
keyboard.modules.append(MouseKeys)
keyboard.extensions.append(display)


#Layer definitions
BASE = 0
NAV_LAYER = 1
LIGHTROOM = 2
LR_SELECT = 3
LR_RATING = 4
DAVINCIRESOLVE = 5
DR_ZOOM = 6

PROGRAMS = [BASE, LIGHTROOM, DAVINCIRESOLVE]


#Button definitions
class MoveProgram(Key):
    def __init__(self, direction):
        super().__init__()
        self.direction = direction
    
    def on_press(self, keyboard, *args, **kwargs):
        global current_prog_idx

        current_prog_idx = (current_prog_idx + self.direction) % len(PROGRAMS)
        next_layer = PROGRAMS[current_prog_idx]
        if keyboard.active_layers:
            keyboard.active_layers[0] = next_layer
        else:
            keyboard.active_layers.append(next_layer)

        return keyboard
    


TRANS = KC.TRNS

#BASE
PREV_TRACK = KC.MPRV
PLAY_PAUSE = KC.MPLY
NEXT_TRACK = KC.MNXT
NAV_BUTTON = KC.MO(NAV_LAYER)
CHROME = KC.F13                     #F-keys need to be set in shortcut settings
EXPLORER = simple_key_sequence(
    (
        KC.LGUI(KC.E)
    )
)
SPOTIFY = KC.F14
DISCORD = KC.F15

#NAVIGATION
PREV_PROG = MoveProgram(-1)
NEXT_PROG = MoveProgram(1)

#LIGHTROOM
SELECT = KC.MO(LR_SELECT)
RATING = KC.MO(LR_RATING)
GRID = KC.G
LOUPE = KC.E
DEVELOP = KC.D
COMPARE = KC.C
PICK = KC.P
UNPICK = KC.U
REJECT = KC.X
CROP = KC.R
MASK = simple_key_sequence(
    (
        KC.LSFT(KC.W)
    )
)


#DAVINCI RESOLVE
ZOOM = KC.MO(DR_ZOOM)
DR_ZOOM_IN = simple_key_sequence(
    (
        KC.LCTRL(KC.EQUAL)
    )
)
DR_ZOOM_OUT = simple_key_sequence(
    (
        KC.LCTRL(KC.MINUS)
    )
)


#Display Layer Map
keyboard.layer_names = ['Normal', 'Lightroom', 'LR-Select']


#Keymap
keyboard.keymap = [
    [#BASE 
     PREV_TRACK,    PLAY_PAUSE,     NEXT_TRACK,     NAV_BUTTON, 
     CHROME,        EXPLORER,       SPOTIFY,        DISCORD,
     ,              ,               ,               ], 
    [#NAV_LAYER
     TRANS,         TRANS,          TRANS,          TRANS, 
     TRANS,         TRANS,          TRANS,          TRANS,
     TRANS,         TRANS,          TRANS,          TRANS],
    [#LIGHTROOM
     GRID,          RATING,         SELECT,         NAV_BUTTON, 
     LOUPE,         PICK,           UNPICK,         REJECT,
     DEVELOP,       COMPARE,        CROP,           MASK],
    [#LR_SELECT
     TRANS,         TRANS,          TRANS,          TRANS, 
     TRANS,         TRANS,          TRANS,          TRANS,
     TRANS,         TRANS,          TRANS,          TRANS],
    [#LR_RATING
     TRANS,         TRANS,          TRANS,          TRANS, 
     KC.N5,         TRANS,          TRANS,          TRANS,
     KC.N1,         KC.N2,          KC.N3,          KC.N4],
    [#DAVINCI RESOLVE
     ,              ,               ZOOM,         NAV_BUTTON, 
     ,              ,               ,               ,
     ,              ,               ,               ],
    [#DR_ZOOM
     TRANS,         TRANS,          TRANS,          TRANS, 
     TRANS,         TRANS,          TRANS,          TRANS,
     TRANS,         TRANS,          TRANS,          TRANS]
]


#Rotary Encoder Map
Encoder_handler.map =   [
                            ((KC.VOLD, KC.VOLU),),
                            ((KC.PREV_PROG, KC.NEXT_PROG),),
                            ((KC.MW_UP, KC.MW_DN),),
                            ((KC.COMMA, KC.DOT),),
                            ((),), 
                            ((),),
                            ((DR_ZOOM_OUT, DR_ZOOM_IN),)
                        ]


#Initialisation
if __name__ == "__main__":
    keyboard.go()