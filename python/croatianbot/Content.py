import re
import random

title_matcher = re.compile("^([^=]+)(=.*)$")
escaped_new_line = re.compile("\\\\n")
h3_search = re.compile(r"===(Adjective|Adverb|Interjection|Phrase|Pronoun|Noun|Verb)=[^#]+# ([^=]+)", re.DOTALL)
curly_link_search = re.compile(r"\{\{[^}]*[|=]([^|}=]+)\}\}")
square_link_search_1 = re.compile(r"\[\[[^|]*\|([^|\]]*)\]\]")
square_link_search_2 = re.compile(r"\[\[([^|\]]*)\]\]")
split_definitions = re.compile(r"#")

def _parse(line: str) -> tuple:
    title_match = title_matcher.match(line).groups()
    title = title_match[0]
    definition = title_match[1]
    definition = escaped_new_line.sub("\n", definition)
    print(definition)
    (grammatical_class, definition) = h3_search.search(definition).groups()
    print(grammatical_class)
    print(definition)
    definition = curly_link_search.sub(r"(\1)", definition)
    definition = square_link_search_1.sub(r"\1", definition)    
    definition = square_link_search_2.sub(r"\1", definition)
    definitions = split_definitions.split(definition)
    return (title, definitions, grammatical_class)

def get() -> str:
    target_line = random.randint(0, 19000)
    with open("sh.csv", "r") as f:
        line_count = 0
        line = f.readline()
        while line:
            if line_count > target_line:
                (title, definitions, grammatical_class) = _parse(line)
                if title and len(definitions) > 0 and grammatical_class:
                    result = f"Croatian {grammatical_class} of the hour:\n\"{title}\"\nDefinition:\n"
                    for i in range(len(definitions)):
                        result += f"{i+1}. {definitions[i]}"
                    return result
            line_count += 1
            line = f.readline()
    return None