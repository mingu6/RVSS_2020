import numpy as np
import os
import sys
sys.path.insert(0, "{}/integration".format(os.getcwd()))
sys.path.insert(0, "../integration")
import penguinPi as ppi

import pickle

def calibrateWheelRadius():
    # Compute the robot scale parameter using a range of wheel velocities.
    # For each wheel velocity, the robot scale parameter can be computed
    # by comparing the time and distance driven to the input wheel velocities.

    wheel_velocities_range = np.arange(15, 60, 5)
    delta_times = []

    for wheel_vel in wheel_velocities_range:
        print("Driving at {} ticks/s.".format(wheel_vel))

        # Repeat the test until the correct time is found.
        while True:
            delta_time = input("Input the time to drive in seconds: ")
            try:
                delta_time = float(delta_time)
            except ValueError:
                print("Time must be a number.")
                continue

            # Drive the robot at the given speed for the given time
            ppi.set_velocity(wheel_vel, wheel_vel, delta_time)

            uInput = input("Did the robot travel 1m?[y/N]")
            if uInput == 'y':
                delta_times.append(delta_time)
                print("Recording that the robot drove 1m in {:.2f} seconds at wheel speed {}.\n".format(delta_time, wheel_vel))
                break
    
    # Once finished driving, compute the scale parameter by averaging
    num = len(wheel_velocities_range)
    scales = 1 / (delta_times * wheel_velocities_range)
    print(scales)
    print("The scale parameter is estimated as {:.4f} (mean) {:.4f} (median), {:.6f} (std err) {:.4f} (robust err) m/ticks.".format(np.average(scales), np.median(scales), 
                    np.std(scales) / len(scales), np.median(np.abs(scales - np.median(scales)))))
    return scales

def calibrateBaseline(scale):
    # Compute the robot basline parameter using a range of wheel velocities.
    # For each wheel velocity, the robot scale parameter can be computed by
    # comparing the time elapsed and rotation completed to the input wheel
    # velocities.

    wheel_velocities_range = range(15, 60, 5)
    delta_times = []

    for wheel_vel in wheel_velocities_range:
        print("Driving at {} ticks/s.".format(wheel_vel))

        # Repeat the test until the correct time is found.
        while True:
            delta_time = input("Input the time to drive in seconds: ")
            try:
                delta_time = float(delta_time)
            except ValueError:
                print("Time must be a number.")
                continue

            # Spin the robot at the given speed for the given time
            ppi.set_velocity(-wheel_vel, wheel_vel, delta_time)

            uInput = input("Did the robot spin 360deg?[y/N]")
            if uInput == 'y':
                delta_times.append(delta_time)
                print("Recording that the robot spun 360deg in {:.2f} seconds at wheel speed {}.\n".format(delta_time, wheel_vel))
                break
    
    # Once finished driving, compute the basline parameter by averaging
    num = len(wheel_velocities_range)
<<<<<<< HEAD
    baselines = 2 * scale * wheel_velocities_range * delta_times / (2 * np.pi)
    print("The baseline parameter is estimated as {:.4f} (mean) {:.4f} (median), {:.6f} (std err) {:.4f} (robust err)m/ticks.".format(np.average(baselines), np.median(baselines), 
                    np.std(baselines) / len(baselines), np.median(np.abs(baselines - np.median(baselines)))))
=======
    baseline = 0
    for delta_time, wheel_vel in zip(delta_times, wheel_velocities_range):
        baseline += 1/num * (2 * scale * wheel_vel * delta_time) / (2 * np.pi)
    print("The baseline parameter is estimated as {:.2f} m.".format(baseline))
>>>>>>> 9adcef12e8c801bae2c41300b0db0e5141c6cc52
    
    return baselines


if __name__ == "__main__":
    # calibrate pibot scale and baseline
<<<<<<< HEAD
    dataDir = "{}/results".format(os.getcwd())

    print('Calibrating PiBot scale...\n')
    scale = calibrateWheelRadius()
    fileNameS = "{}/scale.txt".format(dataDir)
    np.savetxt(fileNameS, scale, delimiter=',')

    print('Calibrating PiBot baseline...\n')
    baseline = calibrateBaseline(scale)
    fileNameB = "{}/baseline.txt".format(dataDir)
    np.savetxt(fileNameB, baseline, delimiter=',')
=======
    dataDir = "wheel_calibration/".format()
    if not os.path.exists(dataDir):
        os.makedirs(dataDir)

    print('Calibrating PiBot scale...\n')
    scale = calibrateWheelRadius()
    fileNameS = "{}scale.txt".format(dataDir)
    np.savetxt(fileNameS, np.array([scale]), delimiter=',')

    print('Calibrating PiBot baseline...\n')
    baseline = calibrateBaseline(scale)
    fileNameB = "{}baseline.txt".format(dataDir)
    np.savetxt(fileNameB, np.array([baseline]), delimiter=',')
>>>>>>> 9adcef12e8c801bae2c41300b0db0e5141c6cc52
    
    print('Finished calibration')