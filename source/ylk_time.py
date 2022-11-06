import adafruit_ntp
import ipaddress
import json
import rtc
import socketpool
import ssl
import time
import wifi

from ylk_led import led

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

def set_ntp_time(tz_offset = 1, attempts = 0, max_attempts = 10):
  print("Retrieving ntp, attempt #{}".format(attempts + 1))
  try:
    pool = socketpool.SocketPool(wifi.radio)
    ntp = adafruit_ntp.NTP(pool, tz_offset=tz_offset)
    now = ntp.datetime
    dst = get_europe_berlin_dst(now)

    rtc.RTC().datetime = time.struct_time((now[0], now[1], now[2], now[3] + dst, now[4], now[5], now[6], now[7], dst))
  except Exception as e:
    print(e)

    if attempts < max_attempts:
      attempts += 1
      time.sleep(attempts + 0.1)
      set_ntp_time(tz_offset, attempts)
    else:
      print("Failed to retrieve time")

def connect_wifi(attempts = 0, max_attempts = 10):
  try:
    led.value = True

    ssid = ''
    
    for network in wifi.radio.start_scanning_networks():
      if network.ssid in secrets['networks']:
        print("Found known network: {}".format(network.ssid))
        ssid = network.ssid
        wifi.radio.stop_scanning_networks()
        break

    if ssid == '':
      print("No known networks found")
      return

    print("Connecting to {}...".format(ssid))
    wifi.radio.connect(ssid, secrets['networks'][ssid])
    print("Connected to {}...".format(ssid))
    
    print("Ping 1.1.1.1", wifi.radio.ping(ipaddress.ip_address("1.1.1.1")))
  except Exception as e:
    led.value = False
    print(e)

    if attempts < max_attempts:
      attempts += 1
      time.sleep(attempts + 0.1)
      connect_wifi(attempts)
    else:
      print("Failed to connect")

def set_rtc():
  connect_wifi()
  set_ntp_time()


def last_sunday_in_month(year, month):
  """
  Return last Sunday in month
  """
  if month == 12:
    month = 0
    year += 1

  first_day_of_next_month = time.struct_time((year, month + 1, 1, 0, 0, 0, 0, 0, 0))
  first_day_of_next_month_timestamp = time.mktime(first_day_of_next_month)

  last_day_of_month = time.localtime(first_day_of_next_month_timestamp - 1)
  last_day_of_month_timestamp = time.mktime(last_day_of_month)

  last_sunday_in_month = time.localtime(last_day_of_month_timestamp - 60 * 60 * 24 * last_day_of_month.tm_wday)

  return last_sunday_in_month

def get_europe_berlin_dst(date_time):
  """
  Daylight saving time for Europe/Berlin is active from last Sunday in March to the last Sunday in October
  """
  dst = 0

  last_sunday_in_march = time.mktime(last_sunday_in_month(date_time.tm_year, 3))
  last_sunday_in_october = time.mktime(last_sunday_in_month(date_time.tm_year, 10))
  today = time.mktime(date_time)

  if today >= last_sunday_in_march and today < last_sunday_in_october:
    dst = 1

  return dst
