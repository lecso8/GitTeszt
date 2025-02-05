import gspread


def remove_accent(text):
    change_to = "aaeeiioooooouuuuuu"
    changable = "áÁéÉíÍóÓöÖőŐúÚüÜűŰ"
    correct = ""
    for changable_thing in text:
        if changable_thing in changable:
            usable = changable.index(changable_thing)
            correct += change_to[usable]
        else:
            correct += changable_thing
    return correct


def main():
    gc = gspread.service_account(filename="creds.json")
    sheet = gc.open("diakok").sheet1
    line = sheet.get_all_values()
    header = line[0]
    data = line[1:]
    if "E-mail" not in header:
        header.append("E-mail")
        sheet.update([header], "A1:Z1")
    email_line = header.index("E-mail") + 1
    for i, line in enumerate(data, start=2):
        if len(line) >= 2:
            last_name = remove_accent(line[0].lower())
            first_name = remove_accent(line[1].lower())
            email = f"{first_name}.{last_name}@gmail.com"
            sheet.update_cell(i, email_line, email)
    print("Az email címek hozzáadása sikeres volt.")


main()
