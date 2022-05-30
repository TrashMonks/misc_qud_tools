This is a tool to generate Caves of Qud names in arbitrary styles. 
It does not currently support names containing titles, but all base name styles can be generated.
The generate_name function takes a path to Qud's Naming.xml file and a style in which to generate the name.
Running the name_gen.py file from a folder containing a copy of Naming.xml will provide a basic REPL
which prompts the user for a name style and generates a name in that style. If no style is provided,
it will use the last used style (Qudish by default).
