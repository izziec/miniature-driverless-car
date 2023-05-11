"""
Elizabeth Cao

Main module.

Running this module connects to a Maestro controller and a joystick. The
joystick is used to control the Maestro controller. It assumes:

Channel 0: Steering, controlled by right joystick X.
Channel 1: Drive, controlled by left joystick Y.
"""

import contextlib
import sys
import time

from joystick import joystick
from maestro import maestro


# TODO: Be smarter about finding paths.
_JOYSTICK_PATH = "/dev/input/event5"
_MAESTRO_PATH = "/dev/ttyACM0"
_MAESTRO_BAUD = 9600

_CHANNEL_STEER = 0
_CHANNEL_DRIVE = 1

def main() -> int:
  with contextlib.ExitStack() as es:
    jdev = es.enter_context(joystick.make_joystick(_JOYSTICK_PATH))
    mdev = es.enter_context(maestro.make_maestro(_MAESTRO_PATH, _MAESTRO_BAUD))

    # TODO: Tune and separate out parameters.
    # Also abstract out Maestro-specific implementation details, such as 6000
    # being zero, into a separate drive module.
    mdev.set_target(_CHANNEL_STEER, 6000)
    mdev.set_speed(_CHANNEL_STEER, 100)
    mdev.set_acceleration(_CHANNEL_STEER, 100)

    mdev.set_target(_CHANNEL_DRIVE, 6000)
    mdev.set_speed(_CHANNEL_DRIVE, 100)
    mdev.set_acceleration(_CHANNEL_DRIVE, 100)

    while True:
      try:
        input_drive = jdev.get_abs(joystick.L_Y)
        input_steer = jdev.get_abs(joystick.R_X)

        normalized_drive = int(input_drive * -500 + 6000)
        normalized_steer = int(input_steer * -1000 + 6300)

        mdev.set_target(_CHANNEL_DRIVE, normalized_drive)
        mdev.set_target(_CHANNEL_STEER, normalized_steer)

        print(f"drive: {normalized_drive}, steer: {normalized_steer}")

        errors = mdev.get_errors()
        if errors != 0:
          mdev.go_home()
          raise Exception(f"Maestro controller raised errors {errors}")

        time.sleep(0.01)
      except KeyboardInterrupt:
        mdev.go_home()
        break

  return 0


if __name__ == "__main__":
  sys.exit(main())
