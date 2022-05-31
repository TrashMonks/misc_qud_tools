This repository hosts a few little tools and scripts relating to Caves of Qud.

name_gen.py is a tool to generate Caves of Qud names in arbitrary styles. 
It does not currently support names containing titles, but all base name styles can be generated.
The generate_name function takes a path to Qud's Naming.xml file and a style in which it generates a name.
The namedump function takes a path to Naming.xml and dumps relevant features into Outputs/naming.lua for wiki purposes.
Running name_gen.py will provide a basic REPL
which prompts the user for a name style and generates a name in that style. If no style is provided,
it will use the last used style (Qudish by default).
If CoQ is installed somewhere other than the usual Windows Steam location, edit qud_install_location.

qud_grab.py reads the Caves of Qud patch notes from Itch and converts them into a wiki format.
It can be run as a script which grabs the most recent hundred (or more by editing the code),
but the read_patch_notes function can also be called on individual pages to convert them (e.g. for large
updates which don't get recognized as patch notes due to not having a date or version number in the title).

glimmerstats.py is a script which generates a wiki table for the probability of different numbers of esper hunters appearing
at different levels of psychic glimmer.