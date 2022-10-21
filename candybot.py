import RPi.GPIO as GPIO
import speech_recognition as sr
import time

enable = 12 # (GPIO 18)
in1 = 37 # Motor input 1 (GPIO 26)
in2 = 36 # Motor input 2 (GPIO 16)
r = sr.Recognizer()

def init_hardware():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(enable, GPIO.OUT)
  GPIO.setup(in1, GPIO.OUT)
  GPIO.setup(in2, GPIO.OUT)

def enable_motor():
  GPIO.output(enable, GPIO.HIGH)

def disable_motor():
  GPIO.output(enable, GPIO.LOW)

def backward():
  GPIO.output(in1, GPIO.HIGH)
  GPIO.output(in2, GPIO.LOW)
  time.sleep(10)

def forward():
  GPIO.output(in1, GPIO.LOW)
  GPIO.output(in2, GPIO.HIGH)
  time.sleep(10)

def person_detected():
  print(f'Person detected')
  return True

def send_candy(text: str):
  if 'trick' in text or 'treat' in text or len(text) > 8:
    print(f'Send Candy')
    enable_motor()
    forward()
    backward()
    disable_motor()
  else:
    print(f'False Detection, no candy')

def main():
  init_hardware()
  while True:
    time.sleep(10)
    print(f'\n\n####################################')
    while not person_detected():
      time.sleep(1)

    with sr.Microphone() as source:
      r.adjust_for_ambient_noise(source)
      print('Halloween greeting')
      audio = r.listen(source)

    try:
      text = r.recognize_google(audio)
      print(f'Google: {text}')
      send_candy(text)
    except Exception as e:
      print(f'Google failed: {e}')
      print(f'Fall back to Sphinx')
      try:
        text = r.recognize_sphinx(audio)
        print(f'Sphinx: {text}')
        send_candy(text)
      except Exception as e:
        print(f'No more fall back, error: {e}')