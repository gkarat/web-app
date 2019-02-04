from tkinter import *


def raise_frame(frame):
    frame.tkraise()


def read_article_input():
    text = text_input.get("1.0", "end-1c")
    comment = comment_input.get("1.0", "end-1c")
    return text, comment


def insert_lines(file_lines, line, actual_ind):  # file_lines is array, not file
    file_lines.insert(actual_ind, line)
    return file_lines, actual_ind + 1


def update_html(f, file_lines):
    file_lines = "".join(file_lines)
    f.truncate(0)
    f.seek(0)
    f.write(file_lines)


def send_article():
    dir = v.get()
    text, comment = read_article_input()
    with open("C:/web/"+dir, "r+") as f:
        if text != "":
            input_lines = text.splitlines()
            file_lines = f.readlines()

            for line in file_lines:
                if line.strip() == '<div class="container">':
                    ind = file_lines.index(line) + 1
                    file_lines, ind = insert_lines(file_lines, '\t\t<div class="content">\n\t\t\t<p>\n', ind)
                    for iline in input_lines:
                        file_lines, ind = insert_lines(file_lines, "\t\t\t" + iline + "<br/>\n", ind)
                    file_lines, ind = insert_lines(file_lines, '\t\t\t</p>\n', ind)

                    if comment != "":
                        input_comment = comment.splitlines()
                        file_lines, ind = insert_lines(file_lines, '\t\t\t<div class="comment">\n', ind)

                        for iline in input_comment:
                            file_lines, ind = insert_lines(file_lines, "\t\t\t\t" + iline + "<br/>\n", ind)

                        file_lines, ind = insert_lines(file_lines, '\t\t\t</div>\n', ind)

                    file_lines, ind = insert_lines(file_lines, '\t\t</div>\n', ind)
                    break
            update_html(f, file_lines)


root = Tk()

bgc = "#C1BFB5"  # background colour
bc = "#F47600"

start = Frame(root, bd=70, background=bgc)
article = Frame(root, bd=70, background=bgc)
image = Frame(root)

for frame in (start, article, image):
    frame.grid(row=0, column=0, sticky='news')

root.resizable(False, False)
root.title("My Web management")

welcome_text = Label(start, text="Welcome back, George!", bd=10, background=bgc).pack(pady=(40, 30))
Button(start, compound=CENTER, width=40, height=4, bd=1, text="Add a new article", background=bc, fg="#FFFFFF",
       command=lambda: raise_frame(article)).pack()
Button(start, compound=CENTER, bd=1, width=40, height=4, text="Add a new image", background=bc, fg="#FFFFFF",
       command=lambda: raise_frame(image)).pack(pady=(10, 0))

Button(article, bd=1, width=10, height=1, text="Back", background=bc, fg="#FFFFFF",
       command=lambda: raise_frame(start)).grid(row=0, column=0, sticky=W)
Label(article, text="Here you can write a new post", bd=10, background=bgc).grid(row=0, column=0, columnspan=3)
text_input = Text(article, height=10)
text_input.grid(row=1, columnspan=3)
Label(article, text="comment\n(will be highlighted below the text)", bd=10, background=bgc) \
    .grid(row=2, column=1, columnspan=2)

v = StringVar()

Radiobutton(article, text="Python bookmarks", variable=v, value="python.html", indicatoron=0, width=30)\
    .grid(sticky=W, row=3, column=0)

Radiobutton(article, text="HTML/CSS bookmarks", variable=v, value="html.html", indicatoron=0, width=30)\
    .grid(sticky=W, row=4, column=0)

comment_input = Text(article, width=50, height=3)
comment_input.grid(row=3, rowspan=2, column=1, columnspan=2)
Button(article, bd=1, width=10, height=1, text="Send", background=bc, fg="#FFFFFF",
       command=lambda: send_article()).grid(row=5, columnspan=3, pady=10, sticky=E)

raise_frame(start)
root.mainloop()
