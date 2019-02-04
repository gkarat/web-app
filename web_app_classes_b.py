import tkinter as tk
from tkinter import font as tkfont

#  import os

bgc = "#C1BFB5"  # background colour
bc = "#F47600"  # button colour


def raise_frame(frame):
    frame.tkraise()


def insert_lines(file_lines, line, actual_ind):  # file_lines is array, not file
    file_lines.insert(actual_ind, line)
    return file_lines, actual_ind + 1


def update_html(f, file_lines):
    file_lines = "".join(file_lines)
    f.truncate(0)
    f.seek(0)
    f.write(file_lines)


def send_article(input_value, text_input, comment_input):
    direction = input_value.get()
    if direction != "":
        print("check", direction)
        direction = "C:/web/" + direction
        text, comment = (text_input.get("1.0", "end-1c"), comment_input.get("1.0", "end-1c"))
        with open(direction, "r+") as f:
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


def send_article_pressed(status, input_value, text_input, comment_input):
    if text_input.get("1.0", "end-1c") != "":
        if input_value.get() != "":
            send_article(input_value, text_input, comment_input)
            status.config(text="Successfully sent", fg="green")
        else:
            status.config(text="Choose where to post", fg="red")
    else:
        status.config(text="Write some text before", fg="red")


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=10, weight="bold")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageArticle, PageImage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.raise_frame("StartPage")

    def raise_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        welcome_text = tk.Label(self, text="Welcome back, George!", bd=10, background=bgc)
        welcome_text.pack(side="top", fill="x", pady=(60, 10))

        button1 = tk.Button(self, width=40, height=4, text="Add a new article", background=bc, fg="white",
                            command=lambda: controller.raise_frame("PageArticle"))
        button2 = tk.Button(self, width=40, height=4, text="Add a new image", background=bc, fg="white",
                            command=lambda: controller.raise_frame("PageImage"))

        button1.pack()
        button2.pack()


class PageArticle(tk.Frame):

    def status_reload(self, status):
        status.grid_forget()
        status.config(text="")
        status.grid(row=0, columnspan=3, sticky=tk.E, padx=(0, 10))
        status.after(3000, lambda: self.status_reload(status))

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        back_button = tk.Button(self, width=10, height=1, text="Back", background=bc, fg="white",
                                command=lambda: controller.raise_frame("StartPage"))

        label1 = tk.Label(self, text="Here you can write a new post", bd=10)

        text_input = tk.Text(self, height=10)

        label2 = tk.Label(self, text="comment\n(will be highlighted below the text)", bd=10)

        input_value = tk.StringVar()

        button1 = tk.Radiobutton(self, text="Python bookmarks", variable=input_value, value="python.html",
                                 indicatoron=0, width=30, selectcolor=bc)

        button2 = tk.Radiobutton(self, text="HTML/CSS bookmarks", variable=input_value, value="html.html",
                                 indicatoron=0, width=30, selectcolor=bc)

        comment_input = tk.Text(self, width=50, height=3)

        status = tk.Label(self, text="")

        send_button = tk.Button(self, bd=1, width=10, height=1, text="Send an article", background=bc, fg="white",
                                command=lambda: send_pressed(status, input_value, text_input, comment_input))

        back_button.grid(row=0, column=0, sticky=tk.W, padx=(10, 0), pady=(10, 10))
        label1.grid(row=0, column=0, columnspan=3)
        text_input.grid(row=1, columnspan=3, padx=(10, 10))
        label2.grid(row=2, column=1, columnspan=2)
        button1.grid(sticky=tk.W, row=3, column=0, padx=(10, 0))
        button2.grid(sticky=tk.W, row=4, column=0, padx=(10, 0))
        comment_input.grid(row=3, rowspan=2, column=1, columnspan=2, padx=(10, 10))
        send_button.grid(row=5, columnspan=3, pady=10, sticky=tk.E, padx=(0, 10))
        status.grid(row=0, columnspan=3, sticky=tk.E, padx=(0, 10))
        status.after(3000, lambda: self.status_reload(status))


def send_image_pressed(path, page):
    if path != "":

    pass

class PageImage(tk.Frame):

    def __init__(self, parent, controller):
        """"
        def clear_url(evt):
            url.delete(0, tk.END)
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        back_button = tk.Button(self, width=10, height=1, text="Back", background=bc, fg="white",
                                command=lambda: controller.raise_frame("StartPage"))
        label = tk.Label(self, text="Here you can post a new image")
        direction = tk.Label(self, text="(here must be a file direction)")
        label2 = tk.Label(self, text="print URL:")
        label3 = tk.Label(self, text="or upload from computer")

        url = tk.Entry(self, width=50)
        # url.insert(0, "enter an image's URL")
        upload_button = tk.Button(self, width=42, height=1, text="Upload")

        send_button = tk.Button(self, bd=1, width=10, height=1, text="Send", background=bc, fg="white",
                                command=lambda: pass)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=3)
        label.grid(row=0, column=0, columnspan=2, pady=(10, 0), padx=(10, 0))
        back_button.grid(row=0, column=0, sticky=tk.W, pady=(10, 0), padx=(10, 0))
        url.grid(row=1, column=0, columnspan=2, sticky=tk.S, padx=(130, 0))
        label2.grid(row=1, column=0, sticky=tk.S+tk.W, columnspan=2, padx=(175, 0))
        # url.bind("<Button-1>", clear_url)
        upload_button.grid(row=2, column=0, columnspan=2, sticky=tk.N, pady=(10, 0), padx=(130, 0))
        label3.grid(row=2, column=0, sticky=tk.N+tk.W, columnspan=2, padx=(90, 0),pady=(10, 0))
        direction.grid(row=2, column=0, columnspan=2, sticky=tk.N, pady=(50,0), padx=(130, 0))


if __name__ == "__main__":
    app = App()
    app.resizable(False, False)
    app.title("My Web management")
    app.mainloop()
