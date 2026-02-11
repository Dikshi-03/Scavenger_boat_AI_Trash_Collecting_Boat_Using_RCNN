# -*- coding: utf-8 -*-
import time
from sensors_module import SensorsModule
from motors_module import MotorsModule
from gps_module import GPSModule
from battery_module import BatteryModule
from vision_module import VisionModule

# ---------------- Initialize Modules ----------------
sensors = SensorsModule(trig_pin=20, echo_pin=21)

motors = MotorsModule(
    left_motor_pins=(17, 18, 5),
    right_motor_pins=(27, 22, 6),
    belt_motor_pins=(23, 24, 25)
)

gps = GPSModule(use_dummy=True)
battery = BatteryModule()

vision = VisionModule(
    "/home/pi/boat_project/rcnn.pt",
    threshold=0.3,
    debug=True,
    show_boxes=True
)

# ---------------- Patrol Parameters ----------------
OBSTACLE_DISTANCE = 20
LOW_BATTERY_VOLTAGE = 8.0
PROP_SPEED = 70  # propeller speed

# ---------------- Return to Start ----------------
def return_to_start():
    print("Returning to start position...")
    motors.stop()
    if gps.use_dummy:
        gps.fake_position = [0.0, 0.0]
        print("[GPS Dummy] Returned to base at (0.0, 0.0).")

# ---------------- Helper: Maintain Propellers ----------------
def maintain_propellers():
    motors.forward(PROP_SPEED)  # reinforce propeller movement

# ---------------- Continuous Trash Search ----------------
def search_trash():
    print("Starting trash search...")
    maintain_propellers()  # start propellers immediately

    try:
        while True:
            # ---- Battery Check ----
            voltage = battery.get_voltage()
            if voltage < LOW_BATTERY_VOLTAGE:
                print("Battery low! Returning to base...")
                motors.stop()
                return_to_start()
                break

            # ---- Obstacle Avoidance ----
            distance = sensors.get_distance()
            if distance < OBSTACLE_DISTANCE:
                print("Obstacle detected! Avoiding...")
                motors.turn_right(PROP_SPEED)
                time.sleep(1)
                maintain_propellers()
                continue

            # ---- Trash Detection ----
            if vision.detect_trash():
                print("Trash detected! Collecting while moving...")
                motors.run_conveyor(100)  # conveyor ON
                start_time = time.time()

                # Keep propellers running during trash collection
                while time.time() - start_time < 15:
                    distance = sensors.get_distance()
                    if distance < OBSTACLE_DISTANCE:
                        print("Obstacle detected during collection! Avoiding...")
                        motors.turn_right(PROP_SPEED)
                        time.sleep(1)
                        maintain_propellers()
                    maintain_propellers()          # keep moving
                    motors.run_conveyor(100)       # ensure conveyor stays ON
                    time.sleep(0.2)                # faster loop for responsiveness

                motors.stop_conveyor()
                print("Trash collected! Continuing search...")

            # ---- GPS Update (Dummy) ----
            if gps.use_dummy:
                gps.fake_position[0] += 0.2
                print(f"[GPS Dummy] Position: {gps.read_coordinates()}")

            maintain_propellers()  # keep propellers moving
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Search aborted by user.")
        motors.stop()

    finally:
        vision.close()
        motors.cleanup()


# ---------------- Run Program ----------------
if __name__ == "__main__":
    search_trash()

