import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.mouse_keys import MouseKeys


keyboard = KMKKeyboard()

# Define your matrix pins (adjust to match your wiring)
keyboard.col_pins = (board.D10, board.D9, board.D8, board.D7)
keyboard.row_pins = (board.D0, board.D1, board.D2)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

Encoder_handler = EncoderHandler()

keyboard.modules.append(Layers())
keyboard.modules.append(Encoder_handler)
keyboard.modules.append(MediaKeys)
keyboard.modules.append(MouseKeys)

Encoder_handler.pins = ((board.D3,board.D6,NONE),)


TRANS = KC.TRNS
SHIFT = KC.MO(1)    #like shift for capital letters
SWITCH = KC.DF(1)   #switches between layers (caps)
RAISE = KC.LT(1, KC.A) #switches if held but types if tapped

keyboard.keymap = [
    [#LAYER 0: A-L
     RAISE, KC.B, KC.C, KC.D, 
     KC.E, KC.F, KC.G, KC.H,
     KC.I, KC.J, KC.K, KC.L], 
    [#LAYER 1: M-X
     KC.M, KC.N, KC.O, KC.P, 
     KC.Q, KC.R, KC.S, KC.T,
     KC.U, KC.V, KC.W, KC.X]
]

Encoder_handler.map =   [
                            ((KC.VOLD, KC.VOLU),),
                            ((KC.MW_UP, KC.MW_DN),),
                        ]


if __name__ == "__main__":
    keyboard.go()