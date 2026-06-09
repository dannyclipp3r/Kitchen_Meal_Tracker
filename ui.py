import tkinter as tk
from tkinter import messagebox, ttk

from src.inventory import load_inventory
from src.meals import (
    add_ingredient_to_meal,
    add_meal,
    load_meals,
    MEAL_TYPES,
    load_meal_ingredients,
    remove_meal_ingredient,
    update_meal_ingredient,
)
from src.planner import build_meal_plan, load_weekly_plan, save_weekly_plan
from src.shopping_list import build_shopping_list, save_shopping_list


class ShoppingListApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Shopping List System")
        self.geometry("720x500")
        self.minsize(640, 420)

        self.build_layout()

    def build_layout(self):
        header = ttk.Frame(self, padding=(16, 16, 16, 8))
        header.pack(fill="x")

        title = ttk.Label(
            header,
            text="Kitchen Meal Tracker",
            font=("Segoe UI", 18, "bold")
        )
        title.pack(anchor="w")

        subtitle = ttk.Label(
            header,
            text="Manage meals, ingredients, meal plans, and shopping lists."
        )
        subtitle.pack(anchor="w", pady=(4, 0))

        self.content_frame = ttk.Frame(self, padding=16)
        self.content_frame.pack(fill="both", expand=True)

        self.status = ttk.Label(self, text="Ready", padding=(16, 0, 16, 12))
        self.status.pack(fill="x")

        self.show_menu()

    def clear_content(self):
        for child in self.content_frame.winfo_children():
            child.destroy()

    def show_menu(self):
        self.clear_content()

        menu = ttk.Frame(self.content_frame)
        menu.pack(expand=True)

        menu_title = ttk.Label(menu, text="Menu", font=("Segoe UI", 15, "bold"))
        menu_title.pack(pady=(0, 16))

        ttk.Button(
            menu,
            text="Add Meal",
            command=self.show_add_meal_task,
            width=28
        ).pack(pady=6)

        ttk.Button(
            menu,
            text="Add Ingredient",
            command=self.show_add_ingredient_task,
            width=28
        ).pack(pady=6)

        ttk.Button(
            menu,
            text="Check Meals",
            command=self.check_meals,
            width=28
        ).pack(pady=6)

        ttk.Button(
            menu,
            text="Generate Meal Plan",
            command=self.generate_meal_plan,
            width=28
        ).pack(pady=6)

        ttk.Button(
            menu,
            text="Generate Shopping List",
            command=self.generate_shopping_list,
            width=28
        ).pack(pady=6)

        self.status.config(text="Menu")

    def add_close_button(self, parent, text="Close", command=None):
        footer = ttk.Frame(parent)
        footer.pack(side="bottom", fill="x", pady=(12, 0))

        ttk.Button(
            footer,
            text=text,
            command=command or self.show_menu
        ).pack(side="left")

    def show_add_meal_task(self):
        self.clear_content()

        task = ttk.Frame(self.content_frame)
        task.pack(fill="both", expand=True)

        ttk.Label(task, text="Add Meal", font=("Segoe UI", 15, "bold")).pack(anchor="w")

        form = ttk.Frame(task)
        form.pack(fill="x", pady=(20, 0))

        ttk.Label(form, text="Meal Name").pack(anchor="w")
        meal_name = ttk.Entry(form)
        meal_name.pack(fill="x", pady=(4, 12))
        meal_name.focus()

        ttk.Label(form, text="Meal Type").pack(anchor="w")
        meal_type = ttk.Combobox(form, values=MEAL_TYPES, state="readonly")
        meal_type.pack(fill="x", pady=(4, 12))
        meal_type.set("Dinner")

        def save_meal():
            try:
                meal = add_meal(meal_name.get(), meal_type.get())
                meal_name.delete(0, tk.END)
                meal_type.set("Dinner")
                self.status.config(text=f"Added {meal['meal_type']} meal: {meal['meal_name']}")
            except Exception as error:
                messagebox.showerror("Error", str(error))

        ttk.Button(form, text="Save Meal", command=save_meal).pack(anchor="w")
        self.add_close_button(task)
        self.status.config(text="Add Meal")

    def show_add_ingredient_task(self):
        meals = load_meals()
        if not meals:
            messagebox.showerror("Error", "Add a meal before adding ingredients.")
            return

        self.clear_content()

        task = ttk.Frame(self.content_frame)
        task.pack(fill="both", expand=True)

        body = ttk.Frame(task)
        body.pack(fill="both", expand=True, pady=(0, 0))
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(1, weight=1)

        ttk.Label(body, text="Add Ingredient", font=("Segoe UI", 15, "bold")).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 12),
            pady=(0, 16)
        )
        ttk.Label(body, text="Ingredients For This Meal", font=("Segoe UI", 15, "bold")).grid(
            row=0,
            column=1,
            sticky="w",
            pady=(0, 16)
        )

        form = ttk.Frame(body)
        form.grid(row=1, column=0, sticky="nsew", padx=(0, 12))

        preview = ttk.Frame(body)
        preview.grid(row=1, column=1, sticky="nsew")
        preview.rowconfigure(0, weight=1)
        preview.columnconfigure(0, weight=1)

        meal_options = [f"{meal['meal_id']} - {meal['meal_name']}" for meal in meals]

        ttk.Label(form, text="Meal").pack(anchor="w")
        meal_choice = ttk.Combobox(form, values=meal_options, state="readonly")
        meal_choice.pack(fill="x", pady=(4, 10))
        meal_choice.current(0)

        ttk.Label(form, text="Ingredient").pack(anchor="w")
        ingredient = ttk.Entry(form)
        ingredient.pack(fill="x", pady=(4, 10))

        detail_frame = ttk.Frame(form)
        detail_frame.pack(fill="x", pady=(0, 12))

        quantity_frame = ttk.Frame(detail_frame)
        quantity_frame.pack(side="left", fill="x", expand=True)
        ttk.Label(quantity_frame, text="Quantity").pack(anchor="w")
        quantity = ttk.Entry(quantity_frame)
        quantity.pack(fill="x", pady=(4, 0))

        unit_frame = ttk.Frame(detail_frame)
        unit_frame.pack(side="left", fill="x", expand=True, padx=(8, 0))
        ttk.Label(unit_frame, text="Unit").pack(anchor="w")
        unit = ttk.Entry(unit_frame)
        unit.pack(fill="x", pady=(4, 0))

        ingredient_table = ttk.Treeview(
            preview,
            columns=("ingredient", "quantity", "unit"),
            show="headings",
            height=8
        )
        ingredient_table.heading("ingredient", text="Ingredient")
        ingredient_table.heading("quantity", text="Qty")
        ingredient_table.heading("unit", text="Unit")
        ingredient_table.column("ingredient", width=160, anchor="w", stretch=True)
        ingredient_table.column("quantity", width=70, anchor="center", stretch=False)
        ingredient_table.column("unit", width=70, anchor="center", stretch=False)

        ingredient_scrollbar = ttk.Scrollbar(preview, orient="vertical", command=ingredient_table.yview)
        ingredient_table.configure(yscrollcommand=ingredient_scrollbar.set)
        ingredient_table.grid(row=0, column=0, sticky="nsew")
        ingredient_scrollbar.grid(row=0, column=1, sticky="ns")

        def selected_meal_id():
            return meal_choice.get().split(" - ", 1)[0]

        def refresh_ingredient_table(event=None):
            for row_id in ingredient_table.get_children():
                ingredient_table.delete(row_id)

            meal_id = selected_meal_id()
            for item in load_meal_ingredients():
                if item["meal_id"] == meal_id:
                    ingredient_table.insert(
                        "",
                        "end",
                        values=(item["ingredient"], item["quantity"], item["unit"])
                    )

        def save_ingredient():
            try:
                row = add_ingredient_to_meal(
                    selected_meal_id(),
                    ingredient.get(),
                    quantity.get(),
                    unit.get()
                )
                ingredient.delete(0, tk.END)
                quantity.delete(0, tk.END)
                unit.delete(0, tk.END)
                refresh_ingredient_table()
                self.status.config(text=f"Added ingredient: {row['ingredient']}")
            except Exception as error:
                messagebox.showerror("Error", str(error))

        meal_choice.bind("<<ComboboxSelected>>", refresh_ingredient_table)
        refresh_ingredient_table()

        ttk.Button(form, text="Save Ingredient", command=save_ingredient).pack(anchor="w")
        self.add_close_button(task)
        self.status.config(text="Add Ingredient")

    def show_table_task(self, title, columns, headings, widths, anchors, rows, values_for_row, status_text, show_vertical_scroll=True, show_horizontal_scroll=True, on_row_open=None, hover_text_for_row=None, on_cell_open=None, hover_text_for_cell=None, close_text="Close", close_command=None):
        self.clear_content()

        task = ttk.Frame(self.content_frame)
        task.pack(fill="both", expand=True)

        ttk.Label(task, text=title, font=("Segoe UI", 15, "bold")).pack(anchor="w")

        table_frame = ttk.Frame(task)
        table_frame.pack(fill="both", expand=True, pady=(12, 0))
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        table = ttk.Treeview(table_frame, columns=columns, show="headings")
        vertical_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
        horizontal_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=table.xview)
        if show_vertical_scroll:
            table.configure(yscrollcommand=vertical_scrollbar.set)
        if show_horizontal_scroll:
            table.configure(xscrollcommand=horizontal_scrollbar.set)

        for column, heading, width, anchor in zip(columns, headings, widths, anchors):
            table.heading(column, text=heading)
            table.column(column, width=width, anchor=anchor, stretch=False)

        table.grid(row=0, column=0, sticky="nsew")
        if show_vertical_scroll:
            vertical_scrollbar.grid(row=0, column=1, sticky="ns")
        if show_horizontal_scroll:
            horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

        def scroll_vertical(event):
            table.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"

        def scroll_horizontal(event):
            table.xview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"

        def start_grab_scroll(event):
            table._grab_scroll_start = {
                "x": event.x,
                "y": event.y,
                "xview": table.xview()[0],
                "yview": table.yview()[0],
            }
            table.configure(cursor="fleur")
            return "break"

        def grab_scroll(event):
            start = getattr(table, "_grab_scroll_start", None)
            if not start:
                return "break"

            width = max(table.winfo_width(), 1)
            height = max(table.winfo_height(), 1)
            delta_x = event.x - start["x"]
            delta_y = event.y - start["y"]

            if show_horizontal_scroll:
                table.xview_moveto(max(0, min(1, start["xview"] - (delta_x / width))))
            if show_vertical_scroll:
                table.yview_moveto(max(0, min(1, start["yview"] - (delta_y / height))))
            return "break"

        def stop_grab_scroll(event):
            start = getattr(table, "_grab_scroll_start", None)
            table.configure(cursor="")

            if start:
                delta_x = abs(event.x - start["x"])
                delta_y = abs(event.y - start["y"])
                if delta_x < 6 and delta_y < 6:
                    row_id = table.identify_row(event.y)
                    column_id = table.identify_column(event.x)
                    if row_id and on_cell_open:
                        on_cell_open(table.item(row_id, "values"), column_id)
                    elif row_id and on_row_open:
                        on_row_open(table.item(row_id, "values"))

            return "break"

        def handle_hover(event):
            row_id = table.identify_row(event.y)
            column_id = table.identify_column(event.x)

            if row_id and hover_text_for_cell:
                hover_text = hover_text_for_cell(table.item(row_id, "values"), column_id)
                if hover_text:
                    table.configure(cursor="hand2")
                    self.status.config(text=hover_text)
                    return

            if row_id and hover_text_for_row:
                table.configure(cursor="hand2")
                self.status.config(text=hover_text_for_row(table.item(row_id, "values")))
            else:
                table.configure(cursor="")
                self.status.config(text=status_text)

        def clear_hover(event):
            if hover_text_for_row or hover_text_for_cell:
                table.configure(cursor="")
                self.status.config(text=status_text)

        if show_vertical_scroll:
            table.bind("<MouseWheel>", scroll_vertical)
        if show_horizontal_scroll:
            table.bind("<Shift-MouseWheel>", scroll_horizontal)
        table.bind("<ButtonPress-1>", start_grab_scroll)
        table.bind("<B1-Motion>", grab_scroll)
        table.bind("<ButtonRelease-1>", stop_grab_scroll)
        table.bind("<Motion>", handle_hover)
        table.bind("<Leave>", clear_hover)

        for row in rows:
            table.insert("", "end", values=values_for_row(row))

        self.add_close_button(task, text=close_text, command=close_command)
        self.status.config(text=status_text)

    def check_meals(self):
        try:
            meals = load_meals()
            self.show_table_task(
                title="Meals",
                columns=("meal_id", "meal_name"),
                headings=("Meal ID", "Meal Name"),
                widths=(120, 520),
                anchors=("center", "w"),
                rows=meals,
                values_for_row=lambda meal: (
                    meal["meal_id"],
                    meal["meal_name"]
                ),
                status_text=f"Loaded {len(meals)} meal(s). Click a meal to view ingredients.",
                on_row_open=lambda values: self.show_meal_ingredients(values[0], values[1], self.check_meals),
                hover_text_for_row=lambda values: f"Click to view ingredients for {values[1]}."
            )
        except Exception as error:
            messagebox.showerror("Error", str(error))
            self.status.config(text="Failed to load meals.")
    def show_meal_ingredients(self, meal_id, meal_name, previous_command=None):
        self.clear_content()

        task = ttk.Frame(self.content_frame)
        task.pack(fill="both", expand=True)

        ttk.Label(task, text=f"{meal_name} Ingredients", font=("Segoe UI", 15, "bold")).pack(anchor="w")

        body = ttk.Frame(task)
        body.pack(fill="both", expand=True, pady=(12, 0))
        body.columnconfigure(0, weight=2)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        table_frame = ttk.Frame(body)
        table_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        table = ttk.Treeview(
            table_frame,
            columns=("row_index", "ingredient", "quantity", "unit"),
            show="headings"
        )
        table.heading("row_index", text="#")
        table.heading("ingredient", text="Ingredient")
        table.heading("quantity", text="Quantity")
        table.heading("unit", text="Unit")
        table.column("row_index", width=45, anchor="center", stretch=False)
        table.column("ingredient", width=240, anchor="w", stretch=True)
        table.column("quantity", width=100, anchor="center", stretch=False)
        table.column("unit", width=100, anchor="center", stretch=False)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)
        table.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        editor = ttk.Frame(body)
        editor.grid(row=0, column=1, sticky="nsew")

        ttk.Label(editor, text="Add Or Edit Ingredient", font=("Segoe UI", 11, "bold")).pack(anchor="w")

        ttk.Label(editor, text="Ingredient").pack(anchor="w", pady=(12, 0))
        ingredient_entry = ttk.Entry(editor)
        ingredient_entry.pack(fill="x", pady=(4, 8))

        ttk.Label(editor, text="Quantity").pack(anchor="w")
        quantity_entry = ttk.Entry(editor)
        quantity_entry.pack(fill="x", pady=(4, 8))

        ttk.Label(editor, text="Unit").pack(anchor="w")
        unit_entry = ttk.Entry(editor)
        unit_entry.pack(fill="x", pady=(4, 12))

        selected_row_index = {"value": None}

        def clear_editor():
            selected_row_index["value"] = None
            ingredient_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)
            unit_entry.delete(0, tk.END)

        def load_table():
            for row_id in table.get_children():
                table.delete(row_id)

            meal_ingredients = [
                item for item in load_meal_ingredients()
                if item["meal_id"] == str(meal_id)
            ]
            for index, item in enumerate(meal_ingredients):
                table.insert(
                    "",
                    "end",
                    values=(index, item["ingredient"], item["quantity"], item["unit"])
                )

            self.status.config(text=f"Loaded {len(meal_ingredients)} ingredient(s) for {meal_name}.")

        def select_ingredient(event=None):
            selection = table.selection()
            if not selection:
                return

            values = table.item(selection[0], "values")
            selected_row_index["value"] = values[0]
            ingredient_entry.delete(0, tk.END)
            ingredient_entry.insert(0, values[1])
            quantity_entry.delete(0, tk.END)
            quantity_entry.insert(0, values[2])
            unit_entry.delete(0, tk.END)
            unit_entry.insert(0, values[3])
            self.status.config(text=f"Selected ingredient: {values[1]}.")

        def add_new_ingredient():
            try:
                added = add_ingredient_to_meal(
                    meal_id,
                    ingredient_entry.get(),
                    quantity_entry.get(),
                    unit_entry.get()
                )
                load_table()
                clear_editor()
                self.status.config(text=f"Added ingredient: {added['ingredient']}.")
            except Exception as error:
                messagebox.showerror("Error", str(error))

        def save_selected_ingredient():
            try:
                if selected_row_index["value"] is None:
                    raise ValueError("Select an ingredient to edit.")

                updated = update_meal_ingredient(
                    meal_id,
                    selected_row_index["value"],
                    ingredient_entry.get(),
                    quantity_entry.get(),
                    unit_entry.get()
                )
                load_table()
                clear_editor()
                self.status.config(text=f"Updated ingredient: {updated['ingredient']}.")
            except Exception as error:
                messagebox.showerror("Error", str(error))

        def remove_selected_ingredient():
            try:
                if selected_row_index["value"] is None:
                    raise ValueError("Select an ingredient to remove.")

                removed = remove_meal_ingredient(meal_id, selected_row_index["value"])
                load_table()
                clear_editor()
                self.status.config(text=f"Removed ingredient: {removed['ingredient']}.")
            except Exception as error:
                messagebox.showerror("Error", str(error))

        ttk.Button(editor, text="Add New Ingredient", command=add_new_ingredient).pack(anchor="w", pady=(0, 8))
        ttk.Button(editor, text="Save Changes", command=save_selected_ingredient).pack(anchor="w", pady=(0, 8))
        ttk.Button(editor, text="Remove Ingredient", command=remove_selected_ingredient).pack(anchor="w", pady=(0, 8))
        ttk.Button(editor, text="Clear Fields", command=clear_editor).pack(anchor="w")

        table.bind("<<TreeviewSelect>>", select_ingredient)
        load_table()

        self.add_close_button(
            task,
            text="Back",
            command=previous_command or self.show_menu,
            extra_buttons=[("Close", self.show_menu)]
        )

    def format_meal_plan_by_day(self, meal_plan):
        days = []
        meal_types = []
        grouped_plan = {}

        for meal in meal_plan:
            day = meal["day"]
            meal_type = meal["meal_type"]

            if day not in grouped_plan:
                grouped_plan[day] = {"day": day}
                days.append(day)

            if meal_type not in meal_types:
                meal_types.append(meal_type)

            grouped_plan[day][meal_type] = meal["meal_name"]

        rows = [grouped_plan[day] for day in days]
        return meal_types, rows

    def generate_meal_plan(self):
        try:
            meals = load_meals()
            meal_plan = build_meal_plan(meals)
            save_weekly_plan(meal_plan)

            meal_types, grouped_rows = self.format_meal_plan_by_day(meal_plan)
            meal_lookup = {
                (meal["day"], meal["meal_type"]): (meal["meal_id"], meal["meal_name"])
                for meal in meal_plan
            }
            columns = tuple(["day"] + meal_types)
            headings = tuple(["Day"] + meal_types)
            widths = tuple([130] + [220 for _ in meal_types])
            anchors = tuple(["w"] + ["w" for _ in meal_types])

            def meal_from_cell(values, column_id):
                if not column_id.startswith("#"):
                    return None

                column_index = int(column_id.replace("#", "")) - 1
                if column_index <= 0 or column_index > len(meal_types):
                    return None

                day = values[0]
                meal_type = meal_types[column_index - 1]
                return meal_lookup.get((day, meal_type))

            self.show_table_task(
                title="Meal Plan",
                columns=columns,
                headings=headings,
                widths=widths,
                anchors=anchors,
                rows=grouped_rows,
                values_for_row=lambda day_plan: tuple(
                    [day_plan["day"]] + [day_plan.get(meal_type, "") for meal_type in meal_types]
                ),
                status_text=f"Generated meal plan for {len(grouped_rows)} day(s). Click a meal to view ingredients.",
                show_vertical_scroll=False,
                show_horizontal_scroll=True,
                on_cell_open=lambda values, column_id: (
                    self.show_meal_ingredients(*meal_from_cell(values, column_id), self.generate_meal_plan)
                    if meal_from_cell(values, column_id) else None
                ),
                hover_text_for_cell=lambda values, column_id: (
                    f"Click to view ingredients for {meal_from_cell(values, column_id)[1]}."
                    if meal_from_cell(values, column_id) else None
                )
            )
        except Exception as error:
            messagebox.showerror("Error", str(error))
            self.status.config(text="Failed to generate meal plan.")

    def generate_shopping_list(self):
        try:
            inventory = load_inventory()
            meals = load_meals()
            meal_ingredients = load_meal_ingredients()
            weekly_plan = load_weekly_plan()

            shopping_list = build_shopping_list(
                inventory,
                meals,
                meal_ingredients,
                weekly_plan
            )
            save_shopping_list(shopping_list)

            self.show_table_task(
                title="Shopping List",
                columns=("ingredient", "quantity", "unit"),
                headings=("Ingredient", "Quantity", "Unit"),
                widths=(340, 140, 140),
                anchors=("w", "center", "center"),
                rows=shopping_list,
                values_for_row=lambda item: (
                    item["ingredient"],
                    item["quantity"],
                    item["unit"]
                ),
                status_text=f"Generated {len(shopping_list)} shopping list item(s).",
                show_vertical_scroll=True,
                show_horizontal_scroll=False
            )
        except Exception as error:
            messagebox.showerror("Error", str(error))
            self.status.config(text="Failed to generate shopping list.")


if __name__ == "__main__":
    app = ShoppingListApp()
    app.mainloop()



























