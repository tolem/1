import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    print(_,filenames)
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None





def converts_md_to_html(content):

    """ This is a basic markdown to html file converter. It supports  
     heading, boldface text, unordered lists, links, and paragraphs
    """


    content = str(content)
    # global regex patterns I used for this challenge 
    heading_pattern = re.compile(r"\s*(#{1,6}\s+\w*.\w+.?\w*)", re.M) 
    bold_pattern = re.compile(r"([**].*[^\s{2,}][**][\s.;,])", re.M)
    para_pattern =  re.compile(r"(?s)(^[\w+|<strong>](?:[^+$\n\r\t][\n\r\r\D\W]?)+)", re.M)
    list_pattern = re.compile(r"(^[*-].+)", re.M)
    uli_pattern = re.compile(r"(^<li>.*</li>$)", re.M) 
    uli_first = re.compile(r"(\s\s^<li>.*</li>$)", re.M)
    uli_last = re.compile(r"(^<li>.*</li>$\s\s)", re.M)
    link_pattern = re.compile(r"\[([\w\s.]+)\]\(([^ ]+?)( '(.+)')?\)", re.M)

    # **** regex ****
    # ***************
    # ***************


    try:

        # helper func 
        def save_to(r, t):
            t = (r + '.')[:-1]  # it copies and modifies the str   # trick from stackoverflow https://stackoverflow.com/questions/24804453/how-can-i-copy-a-python-string
            return t


        # this handles headings logic
        heading_list = heading_pattern.findall(content)
        if heading_list is not None:
            for boldface in heading_list:
                boldface = boldface.rstrip("\r\n")
                prefix = boldface.split()  # strips Markdown from heading 
                boldfont = " ".join(prefix[1:])  # converts list to str
                cnt = len(prefix[0])
        
                if cnt in range(1,7):
                    cnt = len(prefix[0])
                    pattern = re.compile(r"%s" %boldface, )
                    x = pattern.search(content)
                    # print(pattern,x)
                    if pattern.search(content):
                        bold = x.group()
                        print(bold)
                        temp = pattern.sub(f" <h{cnt}> { boldfont } </h{cnt}>",  content,  1) # replaces Markdown with HTML syntax
                        content = (temp + '.')[:-1]
                    else:
                        print("Something Erred")


        # Handles bold logic
        bold_list = bold_pattern.findall(content) # contains a list of bold pattern or returns none 
        print(content,bold_list)
        if bold_list is not None:
            copy_list = bold_list[:]
            for idx,bold in enumerate(copy_list):
                copy_list[idx] = "".join([s for s in bold if s != "*"]) # removes non alphanumeric chars like '*' from str isalpha removes spaces

                b = copy_list[idx] 
                c = bold_pattern.search(content)
                
                print(c)
                if c: # evals expression
                    box = bold_pattern.sub(f"<strong>{b}</strong>", content, 1) # converts pattern to HTML syntax for bold text 
                    content = save_to(box,content)



        # Handles paragraph regex
        para_list = para_pattern.findall(content)
        if para_list is not None:
            # print(len(para_list))
            para_copy = para_list[:]
            for para in para_copy:
                paragraph = content.replace(para,f"<p> {para} </p>",  1) # HTML Syntax for paragraph
                content = save_to(paragraph, content)
            print(paragraph)


        # Handles the logic to convert unordered list into HTML list 
        unordered_list = list_pattern.findall(content)
        if unordered_list is not None:
            
            for li in unordered_list:
                li = li.lstrip("-*")  # removes trailing Markdown
            
                if list_pattern.search(content): # validates a sub strings exists
                                                     
                    l = list_pattern.sub(f"<li>{li}</li>",content,1)  #applies HTML list syntax
                    content = save_to(l,content) 
                    
        
            # uli_tag = uli_pattern.findall(content)  
            # first, last = 0, len(uli_tag)-1  # gets indices 
            # for idx, uli in enumerate(uli_tag):
            #     if idx == first:  # checks position is first
            #         f_uli = content.replace(uli,f"<ul>\n{uli}",1)
            #         content = save_to(f_uli, content)
            #     elif idx == last: # checks position is last
            #         b_uli = content.replace(uli,f"{uli}\n</ul>",1)
            #         content = save_to(b_uli, content)
                    
            #     else:
            #         pass # else skips positions

        # This pattern finds the first and last link position 
        ul_first = uli_first.findall(content)
        ul_last = uli_last.findall(content)
        for i in ul_first:
            a = re.compile(i)
            f_uli = a.sub(f"\n<ul> {i}",content, 1) # adds opening ul tag (HTML syntax) to first link
            content = save_to(f_uli, content)
        for j in ul_last:
            print(j)
            b = re.compile(j)
            f_uli = b.sub(f"{j}</ul>",content, 1) # adds bottom ul tag (HTML syntax) to bottom link
            content = save_to(f_uli, content)


              
    # Handles link pattern 
        link_list = link_pattern.findall(content)
        # print(link_pattern.search(content))
        # for lnks in link_list:
        #     link_items = lnks
        #     click_text, url, *_ = link_items # unpacks tupples and gets items
        #     q_lnks = link_pattern.sub(f"<a href={url} target=_top >{click_text}</a>", content, 1) # converts Markdowns to  link HTML syntx
        #     content = save_to(q_lnks,content)

        for count in range(len(link_list)):
            print(count)
            g = link_pattern.search(content)
            click_text, url = g.group(1, 2) # unpacks  and gets regex items
            print(click_text, url)
            q_lnks = link_pattern.sub(f"<a href={url} target=_top >{click_text}</a>", content, 1)
            content = save_to(q_lnks,content)
            
                                
    except Exception as err:
        print("The error is", err)

    finally:
        print(content)


    return content