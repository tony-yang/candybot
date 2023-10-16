from playsound import playsound
import random
import RPi.GPIO as GPIO
import time

enable = 12 # (GPIO 18)
in1 = 37 # Motor input 1 (GPIO 26)
in2 = 36 # Motor input 2 (GPIO 16)
trigger = 31 # Ultrasonic trigger (GPIO 6)
echo = 29 # Ultrasonic echo (GPIO 5)

SOUNDS = {
  1: '01_happy_halloween.mp3',
  2: '02_happy_halloween2.mp3',
  3: '03_magic_words.mp3',
  4: '04_trick_treat.mp3',
  5: '05_candy.mp3',
  6: '06_candy2.mp3',
}

def init_hardware():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(enable, GPIO.OUT)
  GPIO.setup(in1, GPIO.OUT)
  GPIO.setup(in2, GPIO.OUT)
  GPIO.setup(trigger, GPIO.OUT)
  GPIO.setup(echo, GPIO.IN)

def enable_motor():
  GPIO.output(enable, GPIO.HIGH)

def disable_motor():
  GPIO.output(enable, GPIO.LOW)

def forward():
  enable_motor()
  GPIO.output(in1, GPIO.HIGH)
  GPIO.output(in2, GPIO.LOW)
  time.sleep(3)
  disable_motor()

def measured_distance():
  GPIO.output(trigger, False)
  print(f'Waiting for sensor to settle')
  time.sleep(2)

  GPIO.output(trigger, GPIO.HIGH)
  time.sleep(0.00001)
  GPIO.output(trigger, GPIO.LOW)

  start_time = time.time()
  stop_time = time.time()

  while GPIO.input(echo) == 0:
    start_time = time.time()

  while GPIO.input(echo) == 1:
    stop_time = time.time()

  time_delta = stop_time - start_time
  return round(time_delta * 34300 / 2, 2)

def person_detected():
  dist = measured_distance()
  # Distance in cm
  if dist > 10 and dist < 160:
    print(f'Person detected at {dist} cm')
    return True
  return False

def choose_sound_track():
  return random.randint(1,len(SOUNDS))

def play_sound():
  pass

def send_candy():
  sound_num = choose_sound_track()
  print(f'Send Candy')
  if sound_num == 1:
    play_sound()
    forward()
  elif sound_num == 2:
    play_sound()
    forward()
  elif sound_num == 3:
    play_sound()
    forward()
  elif sound_num == 4:
    play_sound()
    forward()
  elif sound_num == 5:
    play_sound()
    forward()
  elif sound_num == 6:
    play_sound()
    forward()

def main():
  init_hardware()
  while True:
    time.sleep(8)
    print(f'\n\n####################################')
    while not person_detected():
      time.sleep(1)

    try:
      send_candy()
    except Exception as e:
      print(f'No more fall back, error: {e}')

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print(f'Stopped by userr')
  finally:
    GPIO.cleanup()
