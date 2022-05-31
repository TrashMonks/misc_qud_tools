import xml.etree.ElementTree as ET
import regex, random, os, luadata

def int_with_default(element, default=0):
    if element:
        return int(element)
    else:
        return default

def namedump(filename='Naming.xml'):
    tree = ET.parse(filename)
    root = tree.getroot()
    naming = {}
    for namestyle in root.find('namestyles').findall('namestyle'):
        style = namestyle.get('Name').lower() 
        naming[style] = {}
        naming[style]['HyphenationChance'] = int_with_default(namestyle.get('HyphenationChance'))
        naming[style]['TwoNameChance'] = int_with_default(namestyle.get('TwoNameChance'))
        for type in ['pre', 'in', 'post']:
            capType = type.capitalize()
            fixes = namestyle.find(type + 'fixes')
            if fixes:
                fix_count = fixes.get('Amount')
                match = regex.match(r'(\d+)(-(\d+))?', fix_count)
                min = int_with_default(match.group(1), 0)
                max = int_with_default(match.group(3), min)
                naming[style][capType + 'fixes'] = [f.get('Name') for f in fixes.findall(type + 'fix')]
                naming[style][f'Min{capType}fixAmount'] = min
                naming[style][f'Max{capType}fixAmount'] = max
            else:
                naming[style][f'Min{capType}fixAmount'] = 0
                naming[style][f'Max{capType}fixAmount'] = 0
                print(f'No {type}fixes found for {style}')
    lua_string = luadata.serialize(naming, encoding="utf-8", 
                                   indent="  ")
    lua_string = "local naming = " + lua_string + """
naming.get_keys = function()
    local keyset = {}
    for key, value in pairs(naming) do
        if type(value) == 'table' then
            table.insert(keyset, key)
        end
    end
	table.sort(keyset)
    local keys = ''
    for i, key in ipairs(keyset) do
        keys = keys .. ',' .. key:gsub("^%l", string.upper)
    end
    keys = keys:gsub("^,", "")
    return keys
end
return naming
"""    
    with open(os.path.join('Outputs', 'naming.lua'), 'w') as file:
        file.write(lua_string)


def generate_name(style='Qudish', filename='Naming.xml'):
    tree = ET.parse(filename)
    root = tree.getroot()
    for namestyle in root.find('namestyles').findall('namestyle'):
        if namestyle.get('Name') == style:
            two_name_chance = namestyle.get('TwoNameChance')
            if two_name_chance and random.randint(0, 100) < int(two_name_chance):
                name_count = 2
            else:
                name_count = 1
            full_name = ''
            for i in range(name_count):
                name = getafix(namestyle, 'pre') + getafix(namestyle, 'in') + getafix(namestyle, 'post')
                name = name.strip('-')
                name = name[0].upper() + name[1:]
                full_name += name + ' '
            return full_name[:-1]
    print(f'Name style {style} not found')

def getafix(namestyle, type='pre'):
    fixes = namestyle.find(type + 'fixes')
    if fixes is not None:
        fix_list = fixes.findall(type + 'fix')
        name_list = [f.get('Name') for f in fix_list]
        weight_list = [int(f.get('Weight')) if f.get('Weight') else 1 for f in fix_list]
        fix_count = fixes.get('Amount')
        match = regex.match(r'(\d+)(-(\d+))?', fix_count)
        min = int(match.group(1))
        max_str = match.group(3)
        if max_str:
            max = int(max_str)
            amount = random.randint(min, max)
        else:
            amount = min
        result_fixes = random.choices(name_list, weights=weight_list, k=amount)
        result = ''
        hyphenation_chance = namestyle.get('HyphenationChance')
        for fix in result_fixes:
            result += fix
            check = random.randint(0, 100) 
            if hyphenation_chance and check < int(hyphenation_chance):
                result += '-'
        return result
    else:
        return ''

if __name__ == '__main__':
    qud_install_location = 'C:\Program Files (x86)\Steam\steamapps\common\Caves of Qud\CoQ_Data\StreamingAssets\Base'
    naming_path = os.path.join(qud_install_location, 'Naming.xml')
    dump = True
    if dump:
       namedump(naming_path) 
    else:
        command = ''
        prev_name = 'Qudish'
        while (command.strip("'").lower() != 'stop'):
            command = input("Enter a name style ('stop' to quit): ")
            if not command:
                command = prev_name
            else:
                prev_name = command
            print(generate_name(style=command, filename=naming_path))
