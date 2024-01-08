import sys
import os
import re

# Define max engraving speed
LASER_PWR = 255 # 0-255 of laser intensity

if len(sys.argv) > 1:
    input_file_path = sys.argv[1].strip().replace("\"", "")
    if not os.path.isfile(input_file_path):
        print(f"Input file: \"{input_file_path}\" is not a valid file")
    else:
        f = open(input_file_path, "rt")
        input_file_content = f.readlines()
        output_file_content: list[str] = []
        if len(input_file_content) > 0:
            # Read content of file
            print(f"Read {len(input_file_content)} lines")
            pattern = re.compile(r'([Gg]\d+)\s+[Zz]\s*([-+]?\d*\.\d+)')
            for gcode_line in input_file_content:
                if "G" in gcode_line and "Z" in gcode_line:
                    # If gcode is moving the Z axis up, turn off the laser
                    # If gcode is moving the Z axis down, turn on the laser
                    match = pattern.search(gcode_line)
                    if match:
                        height = float(match.group(2))
                        if height < 0:
                            gcode_line = f"M03 S{LASER_PWR} F1000\nM8\n"
                        else:
                            gcode_line = "M09\n"
                output_file_content.append(gcode_line)
            # Write new gcode
            split_input_file_path = input_file_path.split(".")
            output_file_path = split_input_file_path[0] + "_laser." + split_input_file_path[-1]
            print(f"Writing to {output_file_path}...")
            f = open(output_file_path, "w")
            f.write("".join(str(item) for item in output_file_content))
            f.close()
        else:
            print("Input file does not contain any text")
else:
    print(f"\nNo input file is provided, syntax:\n\n\tpython {os.path.basename(__file__)} \"path/to/gcode.ngc\"\n\n")