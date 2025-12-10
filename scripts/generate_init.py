# Utility script for development
# Parse a module and generate the content of the __init__.py
# Only outputs to stdout for now, to avoid erroneous generation
# or erasing the documentation.

if __name__ == "__main__":

	import re
	from pathlib import Path
	import sys
	msg = """    This file is part of daccadevo.

	daccadevo is free software: you can redistribute it and/or modify
	it under the terms of the GNU Lesser General Public License as
	published by the Free Software Foundation, either version 3 of
	the License, or (at your option) any later version.
 
	daccadevo is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
	GNU Lesser General Public License for more details.
 
	You should have received a copy of the GNU Lesser General Public
	License along with qdpy. If not, see <http://www.gnu.org/licenses/>."""

	for line in msg.split("\n"):
		print("#", line)

	print()
	# module to parse
	target = Path(sys.argv[1])
	file_list = list(target.glob("*.py")) # No submodules?
	# for f in file_list:
	# 	mname = f.stem
	# 	if "__" in mname:
	# 		continue
	# 	print("from . import", mname)

	# print()

	all_names = []
	for f in file_list:
		# find all classes and functions in there
		f_names = []
		with open(f,"r") as opened:
			for line in opened.readlines():
				m = re.search(r'(?<=^def )\w+|(?<=^class )\w+', line)
				if m is not None:
					f_names.append(m.group(0))
		length = len(f_names)
		if length > 0:
			print(f"from .{f.stem} import",', '.join(f_names) if length < 3 else "(")
			if length > 2:
				for i in range(length-1):
					print("    "+f_names[i]+",")
				print("    "+f_names[-1]+")")

			all_names += ['"'+n+'"' for n in f_names]

	print()
	print("__all__ = [",",".join(all_names)+"]" if len(all_names) < 3 else "")
	if len(all_names) > 2:
		for val in all_names[:-1]:
			print("    "+val+",")
		print("    "+all_names[-1]+"]")





