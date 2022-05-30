This repository hosts my various little tools and scripts relating to Caves of Qud.

name_gen.py is a tool to generate Caves of Qud names in arbitrary styles. 
It does not currently support names containing titles, but all base name styles can be generated.
The generate_name function takes a path to Qud's Naming.xml file and a style in which to generate the name.
Copying Naming.xml into this folder and running name_gen.py will provide a basic REPL
which prompts the user for a name style and generates a name in that style. If no style is provided,
it will use the last used style (Qudish by default).

qud_grab.py is a script which reads the Caves of Qud patch notes from Itch and converts them into a wiki format.

glimmerstats.py is a script which generates a wiki table for the probability of different numbers of esper hunters appearing
at different levels of psychic glimmer.