def load_text(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return text


if __name__ == "__main__":

    text = load_text("data/scholarship_rules.txt")

    print(text[:1000])