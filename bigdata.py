#!/usr/bin/env python3
# stene.xyz BigData
# Quick n' easy data parser

import os, sys, json
global current_dataset_path, current_dataset
current_dataset_path = ""
current_dataset = []

def save_dataset():
	try:
		with open(current_dataset_path, "w") as outfile:
			outfile.write(current_dataset)
	except:
		print("Error: Couldn't write to file \"" + current_dataset_path + "\"")

def command():
	global current_dataset, current_dataset_path
	raw_command = input(current_dataset_path + "> ")
	command = raw_command.split(" ")[0]
	args = raw_command.split(" ")[1:]

	if(command == "about"):
		print("stene.xyz BigData")
		print("Version 0.1-a")
		print("Written by Johnny Stene <johnny@stene.xyz>")
	elif(command == "help"):
		print("about - About BigData");
		print("help - Displays this menu")
		print("")
		print("FILE OPERATIONS")
		print("create <file> - Create a new dataset.")
		print("save - Save the current dataset.")
		print("copy <file> - Save a copy of the current dataset.")
		print("merge <file> - Merge this dataset with another.")
		print("import <file> - Import a .csv file.")
		print("export_dataset <file> - Exports the whole dataset.")
		print("export_field <field> <file> - Exports a list of all points in the given field as a plain text file.")

		print("DATA MANIPULATION")
		print("list_fields - List all fields in the current dataset.")
		print("search <field> <value> - Searches for all entries that contain given value in the given field.")
		print("search_strict <field> <value> - Searches for all entries that 100% match the given value in the given field.")
		print("filter_include <field> <value> - Filters all data points (retain all data points where the given value is stored in the field)")
		print("filter_exclude <field> <value> - Filters all data points (retain all data points where the given value isn't stored in the field)")

	elif(command == "create"):
		current_dataset_path = args[0] + ".bdata"
		current_dataset = []
		save_dataset()
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
						current_item[template[current_position]] = point
					current_position += 1
					if(current_position == len(template)):
						current_position = 0
						dataset.append(current_item)
						current_item = {}
						item_count += 1
				print(str(item_count) + " items imported.")
		except:
			print("Error while importing.")
	elif(command == "export_dataset"):
		if(len(current_dataset) == 0):
			print("Error: Current dataset empty.")
		else:
			try:
				with open(args[0]) as outfile:
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
			except:
				print("Failed to write.")
	elif(command == "export_field"):
		if(len(current_dataset) == 0):
			print("Error: Current dataset empty.")
		else:
			try:
				with open(args[1]) as outfile:
					for item in current_dataset:
						outfile.write(item[args[0]] + "\n")
				print("Done.")
			except:
				print("Failed to write.")

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
				if(args[1] in item[args[0]]):
					results += 0
					item_text = ""
					for field in fields:
						item_text += item[field] + " | "
					print(item_text)
	elif(command == "search_strict"):
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
				if(args[1] == item[args[0]]):
					results += 0
					item_text = ""
					for field in fields:
						item_text += item[field] + " | "
					print(item_text)
	elif(command == "filter_include"):
		if(len(current_dataset) > 0):
			updated_dataset = []
			for item in current_dataset:
				if(args[1] == item[args[0]]):
					updated_dataset.append(item)
			current_dataset = updated_dataset
		print("Done.")
	elif(command == "filter_exclude"):
		if(len(current_dataset) > 0):
			updated_dataset = []
			for item in current_dataset:
				if not(args[1] == item[args[0]]):
					updated_dataset.append(item)
			current_dataset = updated_dataset
		print("Done.")
if(__name__ == "__main__"):
	while True:
		command()
