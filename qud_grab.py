from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import os, regex

output_folder = 'Outputs/qud_patch_notes'

def dictify(ul):
    result = {}
    for li in ul.find_all("li", recursive=False):
        key = next(li.stripped_strings)
        ul = li.find("ul")
        if ul:
            result[key] = dictify(ul)
        else:
            result[key] = None
    return result


def make_wiki_list(data, level=0): # TODO this should parse out the html somehow
    if isinstance(data, str):
        return f"{level * '*'} {data}\n"
    else:
        output = ""
        if isinstance(data, set):
            for item in data:
                output += make_wiki_list(item, level+1)
        elif isinstance(data, dict):
            for item, children in data.items():
                output += make_wiki_list(item, level+1)
                output += make_wiki_list(children, level+1)
        return output.replace(u'\xa0', ' ')  # turn non-breaking space to space 

def read_patch_notes(driver, output_file, beta_file=None, skip_headerless=True):
    if beta_file is not None:
        separate_beta = True
    else:
        separate_beta = False
    header_text = driver.find_element(by=By.XPATH, value='//section/h1').text
    if 'beta' in header_text:
        notes_type = 'beta'
    else:
        notes_type = 'main' 
    header_pattern = regex.compile(r'[^\n]+ - (?P<date>[^\n]+)')
    match = header_pattern.match(header_text)
    if match:
        date = match.groupdict()['date']
        print(date)
    elif skip_headerless:
        return
    else:
        date = 'TODO FILL IN DATE'
    post_body = driver.find_element(by=By.XPATH, value="//section[contains(@class, 'post_body')]")
    body_html = post_body.get_attribute('outerHTML')
    soup = BeautifulSoup(body_html, features='lxml')
    section = soup.body.section
    output_strings = {
        'main': '',
        'beta': ''
    }

    def output_selector(patch_type):
        if separate_beta:
            return patch_type
        else:
            return 'main'
        
    added_section = False
    for child in section.children:
        if child.name == 'p':
            for line in child.stripped_strings:
                match = regex.match(r"[\d./]+( - '?beta'? branch)?", line)
                if match:
                    if 'beta' in line:
                        notes_type = 'beta'
                    elif notes_type == 'beta':
                        print("GOT UNEXPECTED NEW ITEM DURING BETA?")
                    elif output_strings['main'] != '':
                        print('Got beta with an existing main!')
                        notes_type = 'beta'
                    if 'beta' not in line and notes_type == 'beta':
                        line += " - 'beta' branch" 
                    output_strings[output_selector(notes_type)] += f'=== {line} ===\n'
                    output_strings[output_selector(notes_type)] += f'[{driver.current_url} Released {date}.]\n'
                    added_section = True
        if child.name == 'ul':
            output_strings[output_selector(notes_type)] += make_wiki_list(dictify(child))
    if not added_section:
        if notes_type == 'beta' and 'beta' not in date:
            date += " (beta)"
        header = f'=== {date} ===\n[{driver.current_url} Original patch notes]\n'
        output_strings[output_selector(notes_type)] = header + output_strings[output_selector(notes_type)]
    output_file.write(output_strings['main'])
    if beta_file is not None:
        beta_file.write(output_strings['beta'])

def read_bulk(n=100, separate_beta=False):
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    driver = webdriver.Firefox()
    url = 'https://freeholdgames.itch.io/cavesofqud/devlog'
    output_file = open(os.path.join(output_folder, 'qud_wiki_content.txt'), 'w')
    if separate_beta:
        beta_file = open(os.path.join(output_folder, 'qud_beta_content.txt'), 'w')
    else:
        beta_file = None
    driver.get(url)  # could maybe be Steam
    for i in range(100):  # adjust to as far back as you want to go
        update_links = driver.find_elements(
            by=By.CLASS_NAME, value='read_all_link')
        update_links[i].click()
        if beta_file:
            read_patch_notes(driver, output_file, beta_file)
        else:
            read_patch_notes(driver, output_file)
        driver.back()
    output_file.close()
    if beta_file is not None:
        beta_file.close()

def read_one(url, separate_beta=False):
    driver = webdriver.Firefox()
    driver.get(url)
    with open(os.path.join(output_folder, 'qud_wiki_content.txt'), 'w') as output_file:
        read_patch_notes(driver, output_file, skip_headerless=False)

if __name__ == '__main__':
    # url = 'https://freeholdgames.itch.io/cavesofqud/devlog/348340/the-deep-jungle-feature-arc-is-here'
    # read_one(url)
    read_bulk(100)
    print('Done')
