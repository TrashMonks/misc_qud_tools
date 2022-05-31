import xml.etree.ElementTree as ET
import regex, random, os, luadata, copy

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
        base_style = namestyle.get('Base')
        if base_style:
            if base_style == '*':
                continue
            elif base_style.lower() not in naming:
                print(f'{base_style} not found in usable name lists')
                continue
            else:
                naming[style] = copy.deepcopy(naming[base_style.lower()])
        else:
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
        title_templates_blob = namestyle.find('titletemplates')
        if title_templates_blob:
            naming[style]['TitleTemplates'] = [tt.get('Name') for tt in title_templates_blob.findall('titletemplate')]
        template_vars_blob = namestyle.find('templatevars') 
        if template_vars_blob:
            naming[style]['TemplateVars'] = {}
            template_vars = template_vars_blob.findall('templatevar')
            for var in template_vars:
                naming[style]['TemplateVars'][f"%*{var.get('Name')}%*"] = [val.get('Name') for val in var.findall('value')]
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
            base_style = namestyle.get('Base')
            if base_style and base_style != '*':
                full_name = generate_name(style=base_style, filename=filename)
            else:
                two_name_chance = int_with_default(namestyle.get('TwoNameChance'), 0)
                if random.randint(0, 100) < two_name_chance:
                    name_count = 2
                else:
                    name_count = 1
                full_name = ''
                for i in range(name_count):
                    name = getafix(namestyle, 'pre') + getafix(namestyle, 'in') + getafix(namestyle, 'post')
                    name = name.strip('-')
                    name = name[0].upper() + name[1:]
                    full_name += name + ' '
                full_name = full_name.strip()
            templates = namestyle.find('titletemplates')
            if templates:
                title_templates = templates.findall('titletemplate')
                template_weights = [int_with_default(tt.get('Weight'), 1) for tt in title_templates]
                template_names = [tt.get('Name') for tt in title_templates]
                template = random.choices(template_names, weights=template_weights)[0]
                vars = namestyle.find('templatevars')
                if vars:
                    template_vars = vars.findall('templatevar')
                else:
                    template_vars = []
                vars_parsed = {'Name': ([full_name], [1])}
                for var in template_vars:
                    values = var.findall('value')
                    vars_parsed[var.get('Name')] = (
                        [val.get('Name') for val in values],
                        [int_with_default(val.get('Weight'), 1) for val in values]
                    )
                for var, (var_values, weights) in vars_parsed.items():
                    if f'*{var}*' in template:
                        value = random.choices(var_values, weights=weights)[0]
                        template = template.replace(f'*{var}*', value, 1) 
                return template
            else:
                return full_name
    print(f'Name style {style} not found')

def getafix(namestyle, type='pre'):
    fixes = namestyle.find(type + 'fixes')
    if fixes is not None:
        fix_list = fixes.findall(type + 'fix')
        name_list = [f.get('Name') for f in fix_list]
        weight_list = [int_with_default(f.get('Weight'), 1) for f in fix_list]
        fix_count = fixes.get('Amount')
        match = regex.match(r'(\d+)(-(\d+))?', fix_count)
        min = int_with_default(match.group(1), 0)
        max = int_with_default(match.group(3), min)
        amount = random.randint(min, max)
        result_fixes = random.choices(name_list, weights=weight_list, k=amount)
        result = ''
        hyphenation_chance = int_with_default(namestyle.get('HyphenationChance'), 0)
        for fix in result_fixes:
            result += fix
            check = random.randint(0, 100) 
            if check < hyphenation_chance:
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
