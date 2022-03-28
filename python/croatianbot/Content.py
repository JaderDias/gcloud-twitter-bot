import Storage

def get() -> str:
    pub_count = Storage.read_and_increment_pub_count()
    with open("croatian_nouns.tsv", "r") as f:
        line_count = 0
        line = f.readline()
        while line:
            if line_count == pub_count:
                words = line.rstrip("\n").split("\t")
                message = f"Croatian noun of the hour:\n\"{words[0]}\"\nDefinition:"
                for i in range(len(words) - 1):
                    number = i + 1
                    message = f"{message}\n{number}. {words[number]}"
                return message
            line_count += 1
            line = f.readline()
    return None