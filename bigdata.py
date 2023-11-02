#!/usr/bin/env python3
# stene.xyz BigData
# Quick n' easy data parser

import os, sys, json, shlex, csv
global current_dataset_path, current_dataset, strict_matching
strict_matching = False
current_dataset_path = ""
current_dataset = []

def save_dataset():
	try:
		with open(current_dataset_path, "w") as outfile:
			outfile.write(json.dumps(current_dataset))
	except Exception as e:
		print("Error: Couldn't write to file \"" + current_dataset_path + "\"")
		print(e)

def command():
	global current_dataset, current_dataset_path, strict_matching
	raw_command = input(current_dataset_path + "> ")
	command = raw_command.split(" ")[0]
	args = shlex.split(raw_command.replace(command + " ", ""))

	# Command handlers
	if(command == "about"):
		print("stene.xyz BigData")
		print("Version beta-0")
		print("Written by Johnny Stene <johnny@stene.xyz>")
	elif(command == "help"):
		print("about - About BigData")
		print("help - Displays this menu")
		print("")
		print("FILE OPERATIONS")
		print("create <file> - Create a new dataset.")
		print("open <file> - Load a dataset.")
		print("save - Save the current dataset.")
		print("copy <file> - Save a copy of the current dataset.")
		print("import <file> - Import a .csv file.")
		print("export_dataset <file> - Exports the whole dataset.")
		print("export_field <field> <file> - Exports a list of all points in the given field as a plain text file.")
		print("info - Print database information.")
		print("item <item number> - Gets the nth item in the database.")

		print("DATA MANIPULATION")
		print("strict_matching - Toggle strict matching")
		print("list_fields - List all fields in the current dataset.")
		print("search <field> <value> - Searches for all entries that contain given value in the given field.")
		print("filter [include/exclude] <field> <value> - Filters all data points")

	elif(command == "create"):
		current_dataset_path = args[0] + ".bdata"
		current_dataset = []
		save_dataset()
	elif(command == "open"):
		try:
			current_dataset_path = args[0] + ".bdata"
			with open(current_dataset_path) as jsonfile:
				current_dataset = json.load(jsonfile)
		except Exception as e:
			print("Error opening.")
			print(e)
	elif(command == "save"):
		save_dataset()
	elif(command == "copy"):
		current_dataset_path = args[0] + ".bdata"
		save_dataset()
	elif(command == "import"):
		try:
			with open(args[0]) as infile:
				# get ready to parse the file
				content = infile.read()
				header = content.split("\n")[0]
				parser = csv.reader(content.split("\n")[1:])

				# build template
				# this gets used to turn csv lines into dictionaries
				template = []
				for item in header.split(","):
					template.append(item)

					# sanity check, make sure imported file doesn't contain weird entries
					if(len(current_dataset) > 0):
						if not(item in current_dataset[0]):
							if(item == "[IGNORE]"):
								continue
							print("ERROR: Input file and dataset not alike! Dataset does not contain \"" + item + "\" field.")
							return

				# sanity check, warn user if importing file without some entries
				if(len(current_dataset) > 0):
					for item in current_dataset[0]:
						if not(item in template):
							print("WARN: Input file and dataset not alike! Input file does not contain \"" + item + "\" field.")
				
				# go through and convert everything into dictionaries
				item_count = 0
				for row in parser:
					# some rows are blank
					if(len(row) == 0):
						continue

					# build item
					current_item = {}
					for i in range(0, len(row)):
						current_item[template[i]] = row[i]
					current_dataset.append(current_item)

					# used for friendly message at end
					item_count += 1
				print(str(item_count) + " items imported.")
		except Exception as e:
			print("Error while importing.")
			print(e)
	elif(command == "export_dataset"):
		# obv. don't want to write blank file
		if(len(current_dataset) == 0):
			print("Error: Current dataset empty.")
		else:
			try:
				# open file for overwriting 
				with open(args[0], "w") as outfile:
					# get field information
					header = ""
					fields = []
					for item in current_dataset[0]:
						header += item + ","
						fields.append(item)
					header = header[:-1]
					
					# write header to the file
					outfile.write(header + "\n")

					# write contents of everything to file
					for item in current_dataset:
						# item_text stores the contents of each line so we can replace the last comma with a newline
						item_text = ""
						for i in range(0, len(fields)):
							field = item[fields[i]]

							# this is needed to avoid writing a garbage csv
							if("," in field):
								field = "\"" + field + "\""
							item_text += field + ","
						item_text = item_text[:-1] + "\n"
						outfile.write(item_text)
				print("Done. Wrote " + str(len(current_dataset)) + " items.")
			except Exception as e:
				print("Failed to write.")
				print(e)
	elif(command == "export_field"):
		# once again, don't want a blank file
		if(len(current_dataset) == 0):
			print("Error: Current dataset empty.")
		else:
			try:
				# sanity check because user (me) is a moron
				if not(args[0] in current_dataset[0]):
					print("Field does not exist")

				# literally just write every field as a line
				with open(args[1]) as outfile:
					for item in current_dataset:
						outfile.write(item[args[0]] + "\n")
				print("Done.")
			except Exception as e:
				print("Failed to write.")
				print(e)
	elif(command == "info"):
		print("DATASET INFO:")
		if(len(current_dataset) > 0):
			# item count
			print(str(len(current_dataset)) + " items in dataset")

			# field list
			print("Dataset has the following fields:")
			fields = ""
			for item in current_dataset[0]:
				fields += item + ", "
			fields = fields[:-1]
			print(fields)
		else:
			print("Dataset is empty")
	elif(command == "item"):
		# legit just print every field in the nth item it's not that hard
		args[0] = int(args[0])
		if(len(current_dataset) < args[0]):
			print("Item number too high!")
		args[0] -= 1
		for item in current_dataset[args[0]]:
			print(item + ": " + current_dataset[args[0]][item])

	elif(command == "strict_matching"):
		# toggle strict matching (require complete match for search/filter) on/off
		if(strict_matching):
			print("Strict matching disabled.")
			strict_matching = False
		else:
			print("Strict matching enabled.")
			strict_matching = True
	elif(command == "list_fields"):
		# write out all the fields
		if(len(current_dataset) == 0):
			print("No fields.")
		else:
			for item in current_dataset[0]:
				print(item)
	elif(command == "search"):
		if(len(current_dataset) == 0):
			print("No items to search!")
		else:
			results = 0
			fields = []
			field_text = ""
			for item in current_dataset[0]:
				fields.append(item)
				field_text += item + " | "
			print(field_text)
			for item in current_dataset:
				if not(args[0] in item):
					print("ERROR: Item missing data point!")
					print("Item looks like this: ")
					print(item)
					return
				match = True
				if(strict_matching):
					match = (args[1] == item[args[0]])
				else:
					match = (args[1] in item[args[0]])
				if(match):
					results += 0
					item_text = ""
					for field in fields:
						item_text += item[field] + " | "
					print(item_text)
	elif(command == "filter"):
		if not(args[0] in ["exclude", "include"]):
			print("Error: first argument must be \"exclude\" or \"include\".")
			return
		
		dropped = 0
		if(len(current_dataset) > 0):
			updated_dataset = []
			for item in current_dataset:
				match = True
				if(strict_matching):
					match = (args[2] == item[args[1]])
				else:
					match = (args[2] in item[args[1]])
				if (not(match) and args[0] == "exclude") or (match and args[0] == "include"):
					updated_dataset.append(item)
				else:
					dropped += 1
			current_dataset = updated_dataset
		print("Done. Dropped " + str(dropped) + " items.")

	else:
		print("Invalid command: " + command)
if(__name__ == "__main__"):
	print(" ____ ____ ____ ____ ____ ____ ____ ____ ____ ")
	print("||s |||t |||e |||n |||e |||. |||x |||y |||z ||")
	print("||__|||__|||__|||__|||__|||__|||__|||__|||__||")
	print("|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|")
	print("BigData Beta Version 0")
	print("Written by Johnny Stene <johnny@stene.xyz>")
	print("This software is provided as-is. For more information, see LICENSE.txt.")
	print("")
	print("Type \"help\" for command list.")
	while True:
		command()
