# Lateral Maneuvers Testing Tool

> [!WARNING]
> Use caution when using this tool.

Test your vehicle's lateral control tuning with this tool. The tool will test the vehicle's ability to follow a few lateral maneuvers and includes a tool to generate a report from the route.

## Instructions

1. Check out a development branch such as `master` on your comma device.
2. The full maneuver suite runs at 20 and 30 mph.
3. Enable "Lateral Maneuver Mode" in Galaxy or set the parameter manually:

   ```sh
   echo -n 1 > /data/params/d/LateralManeuverMode
   ```

4. Turn your vehicle back on. You will see "Lateral Maneuver Mode".

5. Ensure the area ahead is clear, as openpilot will command lateral acceleration steps in this mode. Once you are ready, set ACC manually to the target speed shown on screen and let openpilot stabilize lateral. After 2 seconds of steady straight driving, the maneuver will begin automatically. openpilot lateral control stays engaged between maneuvers while waiting for the next maneuver's readiness conditions. The maneuver will be aborted and repeated if speed is out of range, steering is touched or openpilot disengages.

6. When the testing is complete, you'll see an alert that says "Maneuvers Finished." Complete the route by pulling over and turning off the vehicle.

7. Locate the route and ensure all logs are uploaded.

8. Gather the route ID and then run the report generator:

   ```sh
   python tools/lateral_maneuvers/generate_report.py 98395b7c5b27882e/000001cc--5a73bde686
   ```
