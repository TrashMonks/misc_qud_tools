from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import os, regex
from datetime import datetime


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

class PatchNoteGrabber:

    def __init__(self, separate_beta=True):
        self.output_folder = 'Outputs/qud_patch_notes'
        if not os.path.exists(self.output_folder):
            os.mkdir(self.output_folder)
        self.driver = webdriver.Firefox()
        self.url = 'https://freeholdgames.itch.io/cavesofqud/devlog'
        self.output_file = open(os.path.join(self.output_folder, 'qud_wiki_content.txt'), 'w')
        if separate_beta:
            self.beta_file = open(os.path.join(self.output_folder, 'qud_beta_content.txt'), 'w')
        else:
            self.beta_file = None
        self.date_format = '%B %d, %Y'
        with open('last_date.txt', 'r') as date_file:
            self.last_date = datetime.strptime(date_file.read(), self.date_format)

    def output_selector(self, patch_type):
        if self.beta_file is not None:
            return patch_type
        else:
            return 'main'

    def read_patch_notes(self, skip_headerless=True):
        header_text = self.driver.find_element(by=By.XPATH, value='//section/h1').text
        if 'beta' in header_text:
            notes_type = 'beta'
        else:
            notes_type = 'main' 
        header_pattern = regex.compile(r'[^\n]+ - (?P<date>[^\n]+)')
        match = header_pattern.match(header_text)
        if match:
            date = match.groupdict()['date']
            try:
                original_date = datetime.strptime(date, self.date_format)
            except ValueError:
                print('Could not parse', date, 'as date')
                original_date = None
            print(date)
        elif skip_headerless:
            return None, None
        else:
            date = 'TODO FILL IN DATE'
            original_date = None
        post_body = self.driver.find_element(by=By.XPATH, value="//section[contains(@class, 'post_body')]")
        body_html = post_body.get_attribute('outerHTML')
        soup = BeautifulSoup(body_html, features='lxml')
        section = soup.body.section
        output_strings = {
            'main': '',
            'beta': ''
        } 
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
                            notes_type = 'beta'
                        if 'beta' not in line and notes_type == 'beta':
                            line += " - 'beta' branch" 
                        output_strings[self.output_selector(notes_type)] += f'=== {line} ===\n'
                        output_strings[self.output_selector(notes_type)] += f'[{self.driver.current_url} Released {date}.]\n'
                        added_section = True
            if child.name == 'ul':
                output_strings[self.output_selector(notes_type)] += make_wiki_list(dictify(child))
        if not added_section:
            if notes_type == 'beta' and 'beta' not in date:
                date += " (beta)"
            header = f'=== {date} ===\n[{self.driver.current_url} Original patch notes]\n'
            output_strings[self.output_selector(notes_type)] = header + output_strings[self.output_selector(notes_type)]
        return original_date, output_strings
        
    def read_most_recent(self, max=100, date_limit=True):
        most_recent_date = None
        self.driver.get(self.url)  # could maybe be Steam
        for i in range(max):
            update_links = self.driver.find_elements(
                by=By.CLASS_NAME, value='read_all_link')
            update_links[i].click()
            original_date, output_strings = self.read_patch_notes()
            if most_recent_date is None:
                most_recent_date = original_date
            print('Date:', original_date)
            if not date_limit or original_date is None or original_date > self.last_date:
                if output_strings:
                    self.output_file.write(output_strings['main'])
                    if self.beta_file is not None:
                        self.beta_file.write(output_strings['beta'])
                self.driver.back()
            else:
                print('Reached last date')
                break
        if most_recent_date is not None:
            with open('last_date.txt', 'w') as date_file:
                date_file.write(most_recent_date.strftime(self.date_format))



if __name__ == '__main__':
    # url = 'https://freeholdgames.itch.io/cavesofqud/devlog/348340/the-deep-jungle-feature-arc-is-here'
    # read_one(url)
    grab = PatchNoteGrabber()
    grab.read_most_recent()
    print('Done')
