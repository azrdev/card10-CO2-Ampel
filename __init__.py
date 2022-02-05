import bme680
import leds
import time
import display
import vibra
import buttons


IAQ_STEP = 25  # all 11 LEDs ~= iaq 300, offset 25 (first always on), below that linear

# iaq_accuracy thresholds
# see https://firmware.card10.badge.events.ccc.de/epicardium/api.html#bsec-api
IAQ_ACCU_LOW = 1
IAQ_ACCU_MEDIUM = 2
IAQ_ACCU_HIGH = 3

# rocket constants
ROCKET_BLUE = 0  # Left
ROCKET_YELLOW = 1  # Top
ROCKET_GREEN = 2  # Right

colors = {
  'lime': [0, 255, 0],
  'green': [0, 128, 0],
  'yellow': [255, 255, 0],
  'orange': [255, 128, 0],
  'red': [255, 0, 0],
  'purple': [128, 0, 128],
  'brown': [128, 0, 0],
  'blue': [0, 0, 255]
}


def iaq_color(iaq):
    """Map color from iaq value as defined in BME680 datasheet"""
    if (iaq < 50):
        return colors['lime']
    if (iaq < 100):
        return colors['green']
    if (iaq < 150):
        return colors['yellow']
    if (iaq < 200):
        return colors['orange']
    if (iaq < 250):
        return colors['red']
    if (iaq <= 350):
        return colors['purple']
    if (iaq > 350):
        return colors['brown']


def iaq_string(iaq):
    if (iaq < 50):
        return "Excellent"
    if (iaq < 100):
        return "Good"
    if (iaq < 150):
        return "Ventilate?"
    if (iaq < 200):
        return "Ventilate."
    if (iaq < 250):
        return "Ventilate!"
    if (iaq <= 350):
        return "Danger!"
    if (iaq > 350):
        return "Leave!"


def accuracy_string(iaq_accuracy):
    if iaq_accuracy < IAQ_ACCU_LOW:
        return "Run-in"
    elif iaq_accuracy < IAQ_ACCU_MEDIUM:
        return "Low"
    elif iaq_accuracy < IAQ_ACCU_HIGH:
        return "Medium"
    else:
        return "High"


def main():

    power_saving = False  # toggled by button. True → screen off

    disp = display.open()
    disp.backlight(25)
    disp.clear().update()
    leds.clear()
    leds.set_powersave(True)
    leds.dim_top(1)
    leds.dim_bottom(1)

    # main loop
    tick = True
    with bme680.Bme680() as environment:
        while True:
            tick = not tick

            data = environment.get_data()

            # button toggle screen
            if buttons.read(buttons.TOP_RIGHT):
                power_saving = not power_saving

            # set 11 top row LEDs according to IAQ
            iaq_color_now = iaq_color(data.iaq)
            on_led_count = min(data.iaq // IAQ_STEP + 1, 11*IAQ_STEP)
            for i in range(11):
                leds.prep(i,
                          iaq_color_now if i < on_led_count
                          else [0, 0, 0])

            # set 4 bottom LEDs according to eCO2
            if data.eco2 < 600:
                co2_color = colors['green']
            elif data.eco2 < 900:
                co2_color = colors['orange']
            else:  # eco2 >= 900
                co2_color = colors['red']
            leds.prep(leds.BOTTOM_LEFT, co2_color)
            leds.prep(leds.BOTTOM_RIGHT, co2_color)
            leds.prep(leds.TOP_RIGHT, co2_color)
            leds.prep(leds.TOP_LEFT, co2_color)

            leds.set_rocket(ROCKET_BLUE, 0)
            if data.iaq_accuracy < IAQ_ACCU_MEDIUM:  # reading is bad
                # blue rocket always on
                leds.set_rocket(ROCKET_BLUE, 12)
            elif data.iaq_accuracy < IAQ_ACCU_HIGH:  # reading could be more accuate
                # blue rocket blinking
                if tick:
                    leds.set_rocket(ROCKET_BLUE, 12)
                else:
                    leds.set_rocket(ROCKET_BLUE, 0)

            leds.update()

            disp.clear()
            if(not power_saving):
                disp.backlight(25)
                # eCO2: 666          #
                # IAQ: 323           #
                #   accuracy: Medium #
                disp.print("eCO2: " + str(int(data.eco2)) + "ppm")
                disp.print("IAQ: " + str(data.iaq), posy=20)
                disp.print("accuracy: " + accuracy_string(data.iaq_accuracy),
                           fg=iaq_color_now, posy=40)
                # if iaq_accuracy < HIGH, recalibration occurs.
                # Place the badge both in open-air then in a closed box with exhaled air for around 10min each.

            else:
                disp.backlight(0)
                # TODO: dim LEDs

            disp.update()

            time.sleep(1)


if __name__ == "__main__":
    main()
