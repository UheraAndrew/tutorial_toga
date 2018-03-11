import toga
from toga.style.pack import *
import random


def get_capital_list(path):
    out_dict = {}
    with open(path, "r", encoding="UTF-8", errors="ignore") as c_file:
        temp = c_file.readline()
        while temp:
            i = temp.strip().split(" @@ ")
            out_dict[i[1]] = i[0]
            temp = c_file.readline()
    return out_dict


def build(app):
    box = toga.Box()
    ask_box = toga.Box()
    capital_box = toga.Box()
    cursor_box = toga.Box()
    answer_box = toga.Box()

    country_dict = get_capital_list("country.txt")
    country_list = list(country_dict.keys())

    global start
    global data
    start = True
    data = [0, 0, []]

    def next_question(widget):
        global start
        global correct_answer
        global was_answer

        if not start:
            i = random.randint(0, len(country_list))
            correct_answer = country_list[i]
            was_answer = False

            sen_label.text = \
                    country_dict[country_list[i]] + " - is the capital ..."

            possible_answers = [i]
            while len(possible_answers) < 4:
                i = random.randint(0, len(country_list) - 1)
                if i not in possible_answers:
                    possible_answers.append(i)

            random.shuffle(possible_answers)
            result_button1.label = country_list[possible_answers[0]]
            result_button2.label = country_list[possible_answers[1]]
            result_button3.label = country_list[possible_answers[2]]
            result_button4.label = country_list[possible_answers[3]]

    def check_answer(widget):
        answer = widget.label
        global was_answer
        global data

        if not was_answer:
            was_answer = True

            if answer == correct_answer:
                print("123123")
                data[0] += 1
                sen_label.text = "You are right " + correct_answer
            else:
                data[1] += 1
                data[2].append(sen_label.text[:-3] + " of " + correct_answer)
                sen_label.text = sen_label.text[:-3] + " of " +\
                    correct_answer + "\nYour answer is:  " + answer

    def start_question(widget):
        global start
        global data

        if start:
            start = False
            inform_label.text = ""
            final_button.label = "End test"
            data = [0, 0, []]
            next_question(widget)
        else:
            start = True
            inform_label.text =\
            """
            \nYou get {} correct answer\
            \nYou get {} uncorrect answer\
            \nIn following question you get uncorrect answer:\n\
            """.format(data[0], data[1])
            for i in data[2]:
                inform_label.text += i + "\n"
            final_button.label = "Start test"

    next_button = toga.Button("Next question", on_press=next_question)
    final_button = toga.Button("Start test", on_press=start_question)
    cursor_box.add(next_button)
    cursor_box.add(final_button)

    result_button1 = toga.Button("               ", on_press=check_answer)
    result_button2 = toga.Button("               ", on_press=check_answer)
    result_button3 = toga.Button("               ", on_press=check_answer)
    result_button4 = toga.Button("               ", on_press=check_answer)
    capital_box.add(result_button1)
    capital_box.add(result_button2)
    capital_box.add(result_button3)
    capital_box.add(result_button4)

    sen_label = toga.Label("", style=Pack(text_align=CENTER))
    ask_box.add(sen_label)

    inform_label = toga.Label("", style=Pack(text_align=CENTER))
    answer_box.add(inform_label)

    box.add(ask_box)
    box.add(capital_box)
    box.add(cursor_box)
    box.add(answer_box)

    box.style.update(direction=COLUMN, padding_top=50)
    sen_label.style.update(width=400, padding_top=100, padding_left=100)
    capital_box.style.update(width=400, text_align=RIGHT, padding_left=100)
    cursor_box.style.update(text_align=CENTER, padding_left=220)
    answer_box.style.update(text_align=CENTER, padding_left=220)

    return box


def main():
    return toga.App('Country test', 'ua.in.ucu.start', startup=build)


if __name__ == '__main__':
    main().main_loop()
