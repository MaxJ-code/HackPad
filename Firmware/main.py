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


#Button definitions
NORMAL = 0              # Ebene 0: Normaler PC-Modus
LIGHTROOM = 1           # Ebene 1: Lightroom Haupt-Modus
LR_SELECT = 2           # Ebene 2: Lightroom Select-Modus
LR_RATING = 3           # Ebene 3: Lightroom Rating-Modus

TRANS = KC.TRNS
NAV_BUTTON = KC.TG(LIGHTROOM)
LR_SELECT_BUTTON = KC.LT(LR_SELECT, KC.TG(LIGHTROOM))
LR_RATING_BUTTON = KC.LT(LR_RATING, KC.TG(LIGHTROOM))
EDITOR = simple_key_sequence(
    (
        KC.LGUI(KC.E)
    )
)


#Display Layer Map
keyboard.layer_names = ['Normal', 'Lightroom', 'LR-Select']


#Keymap
keyboard.keymap = [
    [#LAYER 0: NORMAL 
     KC.MPRV, KC.MPLY, KC.MNXT, NAV_BUTTON, 
     KC., KC., KC., KC.,
     KC., KC., KC., KC.], 
    [#LAYER 1: LIGHTROOM
     KC.P, KC.U, KC.X, LR_SELECT_BUTTON, 
     KC.R, KC.C, KC., KC.V,
     KC.Q, KC.E, KC.D, LR_RATING_BUTTON],
    [#LAYER 2: LIGHTROOM_SELECT
     TRANS, TRANS, TRANS, TRANS, 
     TRANS, TRANS, TRANS, TRANS,
     TRANS, TRANS, TRANS, TRANS],
    [#LAYER 3: LIGHTROOM_RATING
     TRANS, TRANS, TRANS, TRANS, 
     KC.N5, TRANS, TRANS, TRANS,
     KC.N1, KC.N2, KC.N3, KC.N4]
]


#Rotary Encoder Map
Encoder_handler.map =   [
                            ((KC.VOLD, KC.VOLU),),
                            ((KC.MW_UP, KC.MW_DN),),
                            ((KC.COMMA, KC.DOT),),
                            (())
                        ]


#Initialisation
if __name__ == "__main__":
    keyboard.go()
