from pulp import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image


def all_children(window):
    _list = window.winfo_children()
    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())

    return _list


def get_entries(window):
    _list = all_children(window)
    entries_list = []
    for item in _list:
        if item.winfo_class() == "Entry":
            entries_list.append(item)

    return entries_list


def clear_window(window):
    widget_list = all_children(window)
    for item in widget_list:
        item.pack_forget()
    return


def is_int(str):
    try:
        int(str)
        return True
    except ValueError:
        return False


def is_float(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


def is_fraction(str):
    values = str.split("/")
    return len(values) == 2 and all(is_int(i) for i in values)


def value(str):
    if is_float(str):
        return float(str)
    if is_fraction(str):
        values = str.split("/")
        return float(values[0]) / float(values[1])


def check_valid(window):
    flag = 1
    if window == input_1:
        entries = get_entries(input_1)
        for entry in entries:
            if not entry.get().isdigit() or entry.get() == "0":
                entry.config(
                    highlightthickness=1,
                    highlightbackground="red",
                    highlightcolor="red",
                )
                flag = 0
            else:
                entry.config(
                    highlightthickness=0,
                    highlightbackground="black",
                    highlightcolor="black",
                )
    elif window == input_2:
        entries = get_entries(input_2)
        for entry in entries:
            if is_float(entry.get()) == False and is_fraction(entry.get()) == False:
                entry.config(
                    highlightthickness=1,
                    highlightbackground="red",
                    highlightcolor="red",
                )
                flag = 0
            else:
                entry.config(
                    highlightthickness=0,
                    highlightbackground="black",
                    highlightcolor="black",
                )

    return flag


def back_input_1():
    input_2.destroy()
    input_1.deiconify()
    input_1.state("zoomed")
    return


def back_input_2():
    result_window.destroy()
    input_2.deiconify()
    input_2.state("zoomed")
    return


def on_closing():
    if messagebox.askokcancel("Thoát", "Bạn muốn thoát khỏi chương trình?"):
        input_1.destroy()
    return


def close():
    on_closing()
    return


def enter_input_2():
    if check_valid(input_1) == 0:
        messagebox.showerror("Lỗi!", "Tất cả các ô phải được nhập!!!")
    else:
        input_1.withdraw()

        global input_2
        input_2 = Toplevel()
        input_2.protocol("WM_DELETE_WINDOW", on_closing)
        input_2.title("Linear programming app")
        input_2.state("zoomed")
        input_2["bg"] = "White"

        global so_bien
        so_bien = int(var_entry.get())
        global so_rang_buoc_bien
        so_rang_buoc_bien = int(cons_entry.get())

        main_label = Label(
            input_2,
            text="Ứng dụng giải bài toán Quy hoạch tuyến tính",
            font=("Small Fonts", 20, "bold"),
            pady=40,
        )
        main_label.pack()
        main_label["bg"] = "White"

        obj_frame = Frame(input_2)
        obj_frame["bg"] = "White"
        obj_frame.pack(pady=1)

        obj_label = Label(
            obj_frame, text="Mục tiêu của bài toán: ", font=("Small Fonts", 14)
        )
        obj_label["bg"] = "White"
        obj_label.grid(row=0, column=0)

        global obj_combobox
        obj_combobox = ttk.Combobox(
            obj_frame,
            values=("Min", "Max"),
            state="readonly",
            font=("Small Fonts", 14),
            width=5,
        )
        obj_combobox.set("Min")

        obj_combobox.grid(row=0, column=1, padx=10)

        obj_func_frame = Frame(input_2)
        obj_func_frame["bg"] = "White"
        obj_func_frame.pack(pady=10)

        obj_func_label = Label(obj_func_frame, text="Hàm: ", font=("Small Fonts", 14))
        obj_func_label.grid(row=0, column=0)
        obj_func_label["bg"] = "White"

        global he_so_ham_muc_tieu_entry
        he_so_ham_muc_tieu_entry = []
        for i in range(so_bien):
            x_i_frame = Frame(obj_func_frame)
            x_i_frame.grid(row=0, column=i + 1, pady=10)
            x_i_frame["bg"] = "White"

            x_i_entry = Entry(
                x_i_frame, justify="right", font=("Small Fonts", 14), width=5
            )
            x_i_entry.grid(row=0, column=0, padx=10)
            x_i_entry["bg"] = "White"

            he_so_ham_muc_tieu_entry.append(x_i_entry)

            if i < so_bien - 1:
                x_i_label = Label(
                    x_i_frame,
                    text=("X%d +" % (i + 1)).translate(SUB),
                    font=("Small Fonts", 14),
                )
                x_i_label["bg"] = "White"
                x_i_label.grid(row=0, column=1)

            else:
                x_i_label = Label(
                    x_i_frame,
                    text=("X%d" % (i + 1)).translate(SUB),
                    font=("Small Fonts", 14),
                )
                x_i_label["bg"] = "White"
                x_i_label.grid(row=0, column=1)

        cons_frame = Frame(input_2)
        cons_frame.pack(pady=10)
        cons_frame["bg"] = "White"

        global he_so_rang_buoc_entry, dieu_kien_rang_buoc_combobox, b_entry
        he_so_rang_buoc_entry = [[] for i in range(so_rang_buoc_bien)]
        dieu_kien_rang_buoc_combobox = []
        b_entry = []
        for i in range(so_rang_buoc_bien):
            for j in range(so_bien):
                x_i_j_frame = Frame(cons_frame)
                x_i_j_frame.grid(row=i, column=j, pady=8)
                x_i_j_frame["bg"] = "White"

                x_i_j_entry = Entry(
                    x_i_j_frame, justify="right", font=("Small Fonts", 14), width=5
                )
                x_i_j_entry.grid(row=0, column=0, padx=8)
                x_i_j_entry["bg"] = "White"

                he_so_rang_buoc_entry[i].append(x_i_j_entry)

                if j < so_bien - 1:
                    x_i_j_label = Label(
                        x_i_j_frame,
                        text=("X%d +" % (j + 1)).translate(SUB),
                        font=("Small Fonts", 14),
                    )
                    x_i_j_label.grid(row=0, column=1)
                    x_i_j_label["bg"] = "White"
                else:
                    x_i_j_label = Label(
                        x_i_j_frame,
                        text=("X%d" % (j + 1)).translate(SUB),
                        font=("Small Fonts", 14),
                    )
                    x_i_j_label.grid(row=0, column=1)
                    x_i_j_label["bg"] = "White"

            cond_frame = Frame(cons_frame)
            cond_frame.grid(row=i, column=so_bien)
            cond_frame["bg"] = "White"

            cond_i = ttk.Combobox(
                cond_frame,
                values=("≥", "≤", "="),
                state="readonly",
                font=("Small Fonts", 14),
                width=2,
            )
            cond_i.set("≤")
            cond_i.grid(row=0, column=0, padx=10)

            dieu_kien_rang_buoc_combobox.append(cond_i)

            b_i = Entry(cond_frame, justify="right", font=("Small Fonts", 14), width=5)
            b_i.grid(row=0, column=1, padx=10)
            b_i["bg"] = "White"

            b_entry.append(b_i)

        var_cons_frame = Frame(input_2)
        var_cons_frame.pack(pady=10)
        var_cons_frame["bg"] = "White"

        global rang_buoc_dau_combobox
        rang_buoc_dau_combobox = []
        for i in range(so_bien):
            cond_x_i_frame = Frame(var_cons_frame)
            cond_x_i_frame.grid(row=0, column=i, padx=30, pady=10)
            cond_x_i_frame["bg"] = "White"

            x_i_label = Label(
                cond_x_i_frame,
                text=("X%d" % (i + 1)).translate(SUB),
                font=("Small Fonts", 14),
            )
            x_i_label.grid(row=0, column=0)
            x_i_label["bg"] = "White"

            cond_x_i = ttk.Combobox(
                cond_x_i_frame,
                values=("≥ 0", "≤ 0", "tự do"),
                state="readonly",
                font=("Small Fonts", 14),
                width=5,
            )
            cond_x_i.set("≥ 0")
            cond_x_i.grid(row=0, column=1, padx=10)

            rang_buoc_dau_combobox.append(cond_x_i)

        button_frame = Frame(input_2)
        button_frame.pack(pady=10)
        button_frame["bg"] = "White"

        back_button = Button(
            button_frame,
            text="Quay lại",
            font=("Small Fonts", 15),
            command=back_input_1,
        )
        back_button.grid(row=0, column=0, padx=15)
        back_button["bg"] = "White"

        continue_button = Button(
            button_frame,
            text="Tiếp tục",
            font=("Small Fonts", 15),
            command=enter_result_window,
        )
        continue_button.grid(row=0, column=1, padx=15)
        continue_button["bg"] = "White"

        quit_button = Button(
            button_frame, text="Thoát", font=("Small Fonts", 15), command=close
        )
        quit_button.grid(row=0, column=2, padx=15)
        quit_button["bg"] = "White"

        input_2.mainloop()
    return


def enter_result_window():
    if check_valid(input_2) == 0:
        messagebox.showerror("Lỗi!", "Bạn phải nhập đầy đủ các ô!!!")
    else:
        input_2.withdraw()

        global result_window
        result_window = Toplevel()
        result_window.protocol("WM_DELETE_WINDOW", on_closing)
        result_window.title("Linear programming app")
        result_window.state("zoomed")

        global he_so_rang_buoc
        he_so_rang_buoc = [[] for i in range(so_rang_buoc_bien)]
        for i in range(so_rang_buoc_bien):
            for j in range(so_bien):
                he_so_rang_buoc[i].append(value(he_so_rang_buoc_entry[i][j].get()))

        global he_so_ham_muc_tieu, rang_buoc_dau
        he_so_ham_muc_tieu = []
        rang_buoc_dau = []
        for i in range(so_bien):
            he_so_ham_muc_tieu.append(value(he_so_ham_muc_tieu_entry[i].get()))
            rang_buoc_dau.append(rang_buoc_dau_combobox[i].get())

        global dieu_kien_rang_buoc, b
        dieu_kien_rang_buoc = []
        b = []
        for i in range(so_rang_buoc_bien):
            dieu_kien_rang_buoc.append(dieu_kien_rang_buoc_combobox[i].get())
            b.append(value(b_entry[i].get()))

        x = []
        for i in range(so_bien):
            if rang_buoc_dau[i] == "≥ 0":
                x.append(LpVariable(name=("X%d" % (i + 1)).translate(SUB), lowBound=0))
            elif rang_buoc_dau[i] == "≤ 0":
                x.append(LpVariable(name=("X%d" % (i + 1)).translate(SUB), upBound=0))
            else:
                x.append(LpVariable(name=("X%d" % (i + 1)).translate(SUB)))

        global dang_ham_muc_tieu
        dang_ham_muc_tieu = obj_combobox.get()
        if dang_ham_muc_tieu == "Min":
            model = LpProblem(name="QHTT", sense=LpMinimize)
        else:
            model = LpProblem(name="QHTT", sense=LpMaximize)

        ham_muc_tieu = he_so_ham_muc_tieu[0] * x[0]
        for i in range(1, so_bien):
            ham_muc_tieu += he_so_ham_muc_tieu[i] * x[i]

        model += ham_muc_tieu
        for i in range(so_rang_buoc_bien):
            cons = he_so_rang_buoc[i][0] * x[0]
            for j in range(1, so_bien):
                cons += he_so_rang_buoc[i][j] * x[j]

            if dieu_kien_rang_buoc[i] == "≥":
                model += cons >= b[i]
            elif dieu_kien_rang_buoc[i] == "≤":
                model += cons <= b[i]
            else:
                model += cons == b[i]

        main_label = Label(
            result_window,
            text="Ứng dụng giải bài toán Quy hoạch tuyến tính",
            font=("Small Fonts", 20, "bold"),
            pady=40,
        )
        main_label.pack()

        status = model.solve()
        result = ""
        if status == 1:
            result += "Nghiệm tối ưu:\n"
            for var in model.variables():
                result += "%s = %g\n" % (var.name, var.value())
            result += "\nGiá trị tối ưu z = %g" % model.objective.value()
        elif status == -1:
            result += "Bài toán vô nghiệm"
        elif status == -2:
            result += "Bài toán không giới nội\n\nGiá trị tối ưu z = {}".format(
                "-∞" if dang_ham_muc_tieu == "Min" else "+∞"
            )

        result_label = Label(
            result_window, text=result, justify="left", font=("Small Fonts", 20)
        )
        result_label.pack(pady=20)

        button_frame = Frame(result_window)
        button_frame.pack(pady=20)

        back_button = Button(
            button_frame,
            text="Quay lại",
            font=("Small Fonts", 15),
            command=back_input_2,
        )
        back_button.grid(row=0, column=0, padx=15)

        quit_button = Button(
            button_frame, text="Thoát", font=("Small Fonts", 15), command=close
        )
        quit_button.grid(row=0, column=1, padx=15)

        result_window.mainloop()
    return


if __name__ == "__main__":
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

    global input_1
    input_1 = Tk()
    input_1.title("Linear programming app")
    input_1.protocol("WM_DELETE_WINDOW", on_closing)
    input_1.state("zoomed")

    img = Image.open(r"logo2.png")
    resize = img.resize((250, 220), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(resize)
    panel = Label(input_1, image=img)
    panel.pack(side="top", fill="both", expand="yes")
    panel["bg"] = "White"

    main_label = Label(
        input_1,
        text="Ứng dụng giải bài toán Quy hoạch tuyến tính",
        font=("Small Fonts", 20, "bold"),
        pady=40,
    )
    main_label["bg"] = "White"
    input_1["bg"] = "White"
    main_label.pack()

    main_frame = Frame(input_1)
    main_frame.pack(pady=10)
    main_frame["bg"] = "White"

    var_label = Label(main_frame, text="Nhập số biến: ", font=("Small Fonts", 15))
    var_label["bg"] = "White"
    var_label.grid(row=0, column=0)

    var_entry = Entry(main_frame, justify="right", font=("Small Fonts", 15), width=5)
    var_entry.grid(row=0, column=1, padx=10, pady=15)

    cons_label = Label(main_frame, text="Nhập số ràng buộc: ", font=("Small Fonts", 15))
    cons_label["bg"] = "White"
    cons_label.grid(row=1, column=0)

    cons_entry = Entry(main_frame, justify="right", font=("Small Fonts", 15), width=5)
    cons_entry.grid(row=1, column=1, padx=10, pady=15)

    button_frame = Frame(input_1)
    button_frame["bg"] = "White"
    button_frame.pack(pady=50)

    continue_button = Button(
        button_frame, text="Tiếp tục", font=("Small Fonts", 15), command=enter_input_2
    )
    continue_button["bg"] = "White"
    continue_button.grid(row=0, column=0, padx=15)

    quit_button = Button(
        button_frame, text="Thoát", font=("Small Fonts", 15), command=close
    )
    quit_button["bg"] = "White"
    quit_button.grid(row=0, column=1, padx=15)

    input_1.mainloop()
