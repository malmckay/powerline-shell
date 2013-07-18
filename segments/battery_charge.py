#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from http://stevelosh.com/blog/2010/02/my-extravagant-zsh-prompt/#my-right-prompt-battery-capacity
import math, subprocess, sys

def add_battery_charge_segment():
  p = subprocess.Popen(["/usr/sbin/ioreg", "-rc", "AppleSmartBattery"], stdout=subprocess.PIPE)
  output = p.communicate()[0]

  o_max = [l for l in output.splitlines() if 'MaxCapacity' in l][0]
  o_cur = [l for l in output.splitlines() if 'CurrentCapacity' in l][0]

  b_max = float(o_max.rpartition('=')[-1].strip())
  b_cur = float(o_cur.rpartition('=')[-1].strip())

  charge = b_cur / b_max
  charge_threshold = ((10 * charge))

  # Output
  filled_char = Character.BATTERY_FILLED
  empty_char  = Character.BATTERY_EMPTY

  total_slots, slots = 4, []
  filled = int(math.ceil(charge_threshold * (total_slots / 10.0))) * filled_char
  empty = (total_slots - len(filled)) * empty_char

  out = (filled + empty)

  color_green = 34
  color_yellow = 220
  color_red = 196

  if len(filled) > 2:
    powerline.append(out, color_green, 0)
  elif len(filled) > 1:
    powerline.append(out, color_yellow, 0)
  else:
    powerline.append(out, color_red, 0)

add_battery_charge_segment()
