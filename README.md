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
The read_all function runs a script which grabs the most recent hundred (or more by changing the parameter),
while the read_one function takes a url and gets its patch notes (e.g. for large
updates which don't get recognized as patch notes due to not having a date in the title).
By default it merges beta and main patch notes (as wiki policy is to merge non-current betas in with main),
but it can separate them out by setting the separate_beta parameter to True.
Output goes in Outputs/qud_patch_notes.

glimmerstats.py is a script which generates a wiki table for the probability of different numbers of esper hunters appearing
at different levels of psychic glimmer.
Output goes in Outputs/glimmer_stats.txt.