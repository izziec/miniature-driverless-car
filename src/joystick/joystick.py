"""Module for reading inputs from a joystick."""

import contextlib
from typing import Iterator

import evdev


L_X = evdev.ecodes.ABS_X
L_Y = evdev.ecodes.ABS_Y
R_X = evdev.ecodes.ABS_RX
R_Y = evdev.ecodes.ABS_RY


class Joystick:

  def __init__(self, path: str):
    """Initializes a new joystick controller.

    Args:
      path: The device path for the joystick (e.g. /dev/input/event1).
    """
    self._device = evdev.InputDevice(path)
    self._abs_values = {
      L_X: 0,
      L_Y: 0,
      R_X: 0,
      R_Y: 0,
    }
    self._abs_limits = { c: self._device.absinfo(c) for c in self._abs_values }

  def _update(self) -> None:
    """Reads all pending input events and updates the internal state."""
    while True:
      evt = self._device.read_one()
      if evt is None:
        break

      if evt.type == evdev.ecodes.EV_ABS and evt.code in self._abs_values:
        info = self._abs_limits[evt.code]
        normalized = (evt.value - info.min) / (info.max - info.min)
        normalized = normalized * 2.0 - 1.0
        self._abs_values[evt.code] = normalized

  def close(self) -> None:
    """Closes the connection to the joystick."""
    self._device.close()

  def get_abs(self, axis: int) -> float:
    """Returns the current value for the given axis between [-1, 1]."""
    self._update()
    return self._abs_values[axis]


@contextlib.contextmanager
def make_joystick(*args, **kwargs) -> Iterator[Joystick]:
  """Yields a new joystick controller."""
  j = Joystick(*args, **kwargs)
  try:
    yield j
  finally:
    j.close()
