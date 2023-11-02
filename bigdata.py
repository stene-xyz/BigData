#!/usr/bin/env python3
# stene.xyz BigData
# Quick n' easy data parser

import os, sys, json
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
	raw_args = raw_command.split(" ")[1:]

	# Parse arguments
	args = []
	long_arg = ""
	in_long_arg = False
	for arg in raw_args:
		if(arg.startswith("\"")):
			in_long_arg = True
			arg = arg[1:]
			long_arg = arg
		elif(in_long_arg):
			long_arg += " " + arg
			if(arg.endswith("\"")):
				long_arg = long_arg[:-1]
				args.append(long_arg)
		else:
			args.append(arg)

	# Command handlers
	if(command == "about"):
		print("stene.xyz BigData")
		print("Version 0.2-a")
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
		print("merge <file> - Merge this dataset with another.")
		print("import <file> - Import a .csv file.")
		print("export_dataset <file> - Exports the whole dataset.")
		print("export_field <field> <file> - Exports a list of all points in the given field as a plain text file.")
		print("info - Print database information.")

		print("DATA MANIPULATION")
		print("strict_matching - Toggle strict matching")
		print("list_fields - List all fields in the current dataset.")
		print("search <field> <value> - Searches for all entries that contain given value in the given field.")
		print("filter_include <field> <value> - Filters all data points (retain all data points where the given value is stored in the field)")
		print("filter_exclude <field> <value> - Filters all data points (retain all data points where the given value isn't stored in the field)")

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
	elif(command == "merge"):
		print("TODO")
	elif(command == "import"):
		try:
			with open(args[0]) as infile:
				content = infile.read()
				header = content.split("\n")[0]

				# build template
				template = []
				for item in header.split(","):
					template.append(item)
					if(len(current_dataset) > 0):
						if not(item in current_dataset[0]):
							if(item == "[IGNORE]"):
								continue
							print("ERROR: Input file and dataset not alike! Dataset does not contain \"" + item + "\" field.")
							return

				# sanity check
				if(len(current_dataset) > 0):
					for item in current_dataset[0]:
						if not(item in template):
							print("WARN: Input file and dataset not alike! Input file does not contain \"" + item + "\" field.")

				# add data
				content = content.replace(header, "")
				current_item = {}
				current_position = 0
				item_count = 0
				for point in content.split(","):
					if not(template[current_position] == "[IGNORE]"):
						current_item[template[current_position]] = point.strip()
					current_position += 1
					if(current_position == len(template)):
						current_position = 0
						current_dataset.append(current_item)
						current_item = {}
						item_count += 1
				print(str(item_count) + " items imported.")
		except Exception as e:
			print("Error while importing.")
			print(e)
	elif(command == "export_dataset"):
		if(len(current_dataset) == 0):
			print("Error: Current dataset empty.")
		else:
			try:
				with open(args[0], "w") as outfile:
					header = ""
					fields = []
					for item in current_dataset[0]:
						header += item + ","
						fields.append(item)
					header = header[:-1]
					outfile.write(header + "\n")
					for item in current_dataset:
						for i in range(0, len(fields) - 1):
							outfile.write(item[fields[i]] + ",")
						outfile.write(item[fields[-1]] + "\n")
				print("Done.")
			except Exception as e:
				print("Failed to write.")
				print(e)
	elif(command == "export_field"):
		if(len(current_dataset) == 0):
			print("Error: Current dataset empty.")
		else:
			try:
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
			print(str(len(current_dataset)) + " items in dataset")
			print("Dataset has the following fields:")
			fields = ""
			for item in current_dataset[0]:
				fields += item + ", "
			fields = fields[:-1]
			print(fields)
		else:
			print("Dataset is empty")

	elif(command == "strict_matching"):
		if(strict_matching):
			print("Strict matching disabled.")
			strict_matching = False
		else:
			print("Strict matching enabled.")
			strict_matching = True
	elif(command == "list_fields"):
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
	elif(command == "filter_include"):
		dropped = 0
		if(len(current_dataset) > 0):
			updated_dataset = []
			for item in current_dataset:
				match = True
				if(strict_matching):
					match = (args[1] == item[args[0]])
				else:
					match = (args[1] in item[args[0]])
				if(match):
					updated_dataset.append(item)
				else:
					dropped += 1
			current_dataset = updated_dataset
		print("Done. Dropped " + str(dropped) + " items.")
	elif(command == "filter_exclude"):
		dropped = 0
		if(len(current_dataset) > 0):
			updated_dataset = []
			for item in current_dataset:
				match = True
				if(strict_matching):
					match = (args[1] == item[args[0]])
				else:
					match = (args[1] in item[args[0]])
				if not(match):
					updated_dataset.append(item)
				else:
					dropped += 1
			current_dataset = updated_dataset
		print("Done. Dropped " + str(dropped) + " items.")
if(__name__ == "__main__"):
	while True:
		command()
