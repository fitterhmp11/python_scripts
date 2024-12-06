# this script takes a portion of fortinet policy config, changes and text port (for example
# interface name) modifies the name, and creates a new policy with ID 0 .  It prints out only necessary
# lines in the outputfile_modified.txt


import sys
import os

# Check if the user provided an input file as an argument
if len(sys.argv) != 2:
    print("Usage: python modify_firewall_config.py <input_file>")
    sys.exit(1)

# Get the input file from the command line
input_file = sys.argv[1]

# Check if the input file exists
if not os.path.isfile(input_file):
    print(f"Error: File '{input_file}' does not exist.")
    sys.exit(1)

# Define the output file name based on the input file
output_file = os.path.splitext(input_file)[0] + "_policy_copy_modified.txt"

org_value1 =  "wan-edge" # the string to be located and replaced
new_value1 = "wan-zone1" # the string to replace the org_value1

# Open the input file and process each line
with open(input_file, "r") as file, open(output_file, "w") as outfile:
    inside_edit = False  # Track if we're inside an "edit" block
    edit_config_lines = []  # Store lines of the current "edit" block

    for line in file:
        stripped_line = line.strip()

        # Start of an "edit" block
        if stripped_line.startswith("edit"):
            inside_edit = True
            edit_config_lines = [line]  # Start a new "edit" block
            continue

        # End of an "edit" block
        if inside_edit and stripped_line.startswith("next"):
            inside_edit = False

            # Process the "edit" block
            edit_text = "".join(edit_config_lines)
            if org_value1 in edit_text:
                # Change the edit number to 0 and replace "wan-edge" with "wan-zone1"
                modified_edit = edit_text.replace(org_value1, new_value1)
                modified_edit = modified_edit.replace(edit_config_lines[0], "edit 0\n")
                outfile.write(modified_edit)  # Write the modified edit block to output
                outfile.write("next\n")  # Add the "next" keyword

            continue

        # If inside an "edit" block, collect lines
        if inside_edit:
            edit_config_lines.append(line)

# Output completion message
print(f"Modified firewall configuration saved to '{output_file}'.")