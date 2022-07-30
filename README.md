This repository hosts a few little tools and scripts relating to Caves of Qud.

name_gen.py is a tool to generate Caves of Qud names in arbitrary styles. 
It does not currently support names containing titles, but all base name styles can be generated.
* The generate_name function takes a path to Qud's Naming.xml file and a style in which it generates a name.
* The namedump function takes a path to Naming.xml and dumps relevant features into Outputs/naming.lua for wiki purposes.
* Running name_gen.py will provide a basic REPL
which prompts the user for a name style and generates a name in that style. If no style is provided,
it will use the last used style (Qudish by default).
* If CoQ is installed somewhere other than the usual Windows Steam location, edit qud_install_location.

qud_grab.py reads the Caves of Qud patch notes from Itch and converts them into a wiki format.
It mainly contains the PatchNoteGrabber class.
* The read_most_recent method reads the most recent updates (up to a maximum which defaults to 100 but 
can be overridden), stopping when it reaches the date in last_date.txt. last_date.txt will be updated 
when it is run, but should be checked against the actual contents of the wiki's Version History page.
* The read_specific method will take a specific patch note URL and read its contents. This is useful
for major updates as their header does not follow the usual patch note format so they will usually be
skipped by read_most_recent.
* By default the PatchNoteGrabber will separate out beta from main patch notes, but wiki policy is to
keep them together for non-current betas. If the patch notes you are grabbing include non-current betas,
set separate_beta=False when creating the PatchNoteGrabber.
* Output goes in Outputs/qud_patch_notes.

glimmerstats.py is a script which generates a wiki table for the probability of different numbers of esper hunters appearing
at different levels of psychic glimmer. 
* This is based on a manual conversion to Python of XRL.PsychicHunterSystem's GetNumPsychicHunters.
* Output goes in Outputs/glimmer_stats.txt.