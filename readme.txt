#####################
# stene.xyz BigData #
#####################

== About ==
stene.xyz BigData is a script to handle manual analysis of .CSV files.
It is intended for use with smaller (<1M entries) datasets, to allow quick manipulations.

== Building ==
To build, install pyinstaller and run `pyinstaller bigdata.py`

== License ==
stene.xyz BigData is released under the MIT license. See `LICENSE.txt`.

== Changelog ==
beta-0:
    - Add welcome message 
    - Relicense as MIT
    - Filter now takes include/exclude argument.
    - Added invalid command message.
0.3-a:
    - Fixed command parser.
    - Fixed .csv parser.
    - Added "item" command.
    - Removed empty "merge" function.
0.2-a:
    - Fixed crashing bug when importing file.
    - Better error messages.
    - Added "info" command.
    - Added "strict_matching" command.
0.1-a:
    - Initial release.

== Known bugs ==
- Strict matching doesn't work