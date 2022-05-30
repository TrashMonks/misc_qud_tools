import regex, os
from qud_grab import output_folder

print(sorted(os.listdir(output_folder), key=lambda fn: int(fn.split('.')[0])))

with open(os.path.join('Outputs', 'qud_wiki_content.txt'), 'w') as output_file:
    for filename in sorted(os.listdir(output_folder), key=lambda fn: int(fn.split('.')[0])):
        with open(os.path.join(output_folder, filename), 'r') as file:
            patch_notes = file.read()
        patch_notes = patch_notes.replace('{{', '{{((}}')
        patch_notes_pattern = regex.compile(r"[^\n]+ - (?P<date>[^\n]+)\n((?P<version>[\d./]+( - 'beta' branch)?)\n)?(?P<notes>.*\n)*")
        match = regex.match(pattern=patch_notes_pattern, string=patch_notes)
        if match:
            captures = match.capturesdict()
            if len(captures['version']) > 0:
                output_file.write(f'=== {captures["version"][0]} ===\n')
                output_file.write(f'Released {captures["date"][0]}.\n')
            else:
                output_file.write(f'=== {captures["date"][0]} ===\n')
            output_file.write('* ' + '* '.join(captures["notes"]))
        else:
            print(filename, len(patch_notes) > 1000, patch_notes.split('\n')[:3])
            if len(patch_notes) > 1000:
                with open(os.path.join('Outputs', 'qud_not_added.txt'), 'a') as missing_file:
                    missing_file.write(patch_notes)
