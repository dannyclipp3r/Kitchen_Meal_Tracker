import tkinter as tk
from tkinter import messagebox, ttk

import customtkinter as ctk

from src.meals import (
    MEAL_TYPES,
    add_ingredient_to_meal,
    add_meal,
    load_meal_ingredients,
    load_meals,
    remove_meal_ingredient,
    update_meal_ingredient,
    delete_meal,
)
from src.planner import build_meal_plan, load_weekly_plan, save_weekly_plan
from src.shopping_list import build_shopping_list, save_shopping_list
from src.email_service import send_shopping_list_email


class KitchenMealTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.title("Kitchen Meal Tracker")
        self.geometry("840x480")
        self.resizable(False, False)

        self.configure_grid()
        self.configure_tree_style()
        self.build_layout()

    def configure_grid(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def configure_tree_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", rowheight=26)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def build_layout(self):
        header = ctk.CTkFrame(self, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(header, text="Kitchen Meal Tracker", font=ctk.CTkFont(size=22, weight="bold"))
        title.grid(row=0, column=0, sticky="w", padx=18, pady=(16, 2))

        subtitle = ctk.CTkLabel(header, text="Manage meals, ingredients, meal plans, and shopping lists.")
        subtitle.grid(row=1, column=0, sticky="w", padx=18, pady=(0, 14))

        self.content = ctk.CTkFrame(self)
        self.content.grid(row=1, column=0, sticky="nsew", padx=18, pady=18)
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.status = ctk.CTkLabel(self, text="Ready", anchor="w")
        self.status.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 12))

        self.show_menu()

    def clear_content(self):
        for child in self.content.winfo_children():
            child.destroy()

    def set_status(self, text):
        self.status.configure(text=text)

    def show_menu(self):
        self.clear_content()
        menu = ctk.CTkFrame(self.content)
        menu.grid(row=0, column=0)

        ctk.CTkLabel(menu, text="Menu", font=ctk.CTkFont(size=18, weight="bold")).pack(padx=28, pady=(24, 14))
        ctk.CTkButton(menu, text="Add Meal", width=260, command=self.show_add_meal).pack(pady=7)
        ctk.CTkButton(menu, text="Check Meals", width=260, command=self.check_meals).pack(pady=7)
        ctk.CTkButton(menu, text="Weekly Meal Plan", width=260, command=self.generate_meal_plan).pack(pady=7)
        ctk.CTkButton(menu, text="Generate Shopping List", width=260, command=self.generate_shopping_list).pack(pady=(7, 24))
        self.set_status("Menu")

    def add_footer(self, parent, primary_text="Close", primary_command=None, extra_buttons=None):
        footer = ctk.CTkFrame(parent, fg_color="transparent")
        footer.grid(row=99, column=0, columnspan=3, sticky="ew", pady=(12, 0))
        footer.grid_columnconfigure(99, weight=1)

        ctk.CTkButton(footer, text=primary_text, width=110, command=primary_command or self.show_menu).grid(row=0, column=0, sticky="w")
        for index, (text, command) in enumerate(extra_buttons or [], start=1):
            ctk.CTkButton(footer, text=text, width=110, command=command).grid(row=0, column=index, sticky="w", padx=(8, 0))

    def show_add_meal(self):
        self.clear_content()
        page = ctk.CTkFrame(self.content, fg_color="transparent")
        page.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        page.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(page, text="Add Meal", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, sticky="w")

        form = ctk.CTkFrame(page)
        form.grid(row=1, column=0, sticky="ew", pady=(16, 0))
        form.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(form, text="Meal Name", anchor="w").grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 4))
        meal_name = ctk.CTkEntry(form)
        meal_name.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 12))
        meal_name.focus()

        ctk.CTkLabel(form, text="Meal Type", anchor="w").grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 4))
        meal_type = ctk.CTkOptionMenu(form, values=MEAL_TYPES)
        meal_type.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 16))
        meal_type.set("Dinner")

        def save_meal():
            try:
                meal = add_meal(meal_name.get(), meal_type.get())
                meal_name.delete(0, tk.END)
                meal_type.set("Dinner")
                self.set_status(f"Added {meal['meal_type']} meal: {meal['meal_name']}")
            except Exception as error:
                messagebox.showerror("Error", str(error))

        ctk.CTkButton(form, text="Save Meal", command=save_meal).grid(row=4, column=0, sticky="w", padx=16, pady=(0, 16))
        self.add_footer(page)
        self.set_status("Add Meal")

    def make_table(self, parent, columns, headings, widths, anchors, show_vertical=True, show_horizontal=True):
        table_frame = ctk.CTkFrame(parent)
        table_frame.grid(row=0, column=0, sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        table = ttk.Treeview(table_frame, columns=columns, show="headings")
        table.tag_configure("hover", background="#dceeff")

        vertical = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
        horizontal = ttk.Scrollbar(table_frame, orient="horizontal", command=table.xview)
        if show_vertical:
            table.configure(yscrollcommand=vertical.set)
        if show_horizontal:
            table.configure(xscrollcommand=horizontal.set)

        for column, heading, width, anchor in zip(columns, headings, widths, anchors):
            table.heading(column, text=heading)
            table.column(column, width=width, anchor=anchor, stretch=False)

        table.grid(row=0, column=0, sticky="nsew")
        if show_vertical:
            vertical.grid(row=0, column=1, sticky="ns")
        if show_horizontal:
            horizontal.grid(row=1, column=0, sticky="ew")
        return table

    def show_table_page(
        self,
        title,
        columns,
        headings,
        widths,
        anchors,
        rows,
        values_for_row,
        status_text,
        show_vertical=True,
        show_horizontal=True,
        on_row_open=None,
        hover_text_for_row=None,
        on_cell_open=None,
        hover_text_for_cell=None,
        close_text="Close",
        close_command=None,
        extra_buttons=None,
    ):
        self.clear_content()
        page = ctk.CTkFrame(self.content, fg_color="transparent")
        page.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        page.grid_rowconfigure(1, weight=1)
        page.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(page, text=title, font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, sticky="w")

        table_host = ctk.CTkFrame(page, fg_color="transparent")
        table_host.grid(row=1, column=0, sticky="nsew", pady=(12, 0))
        table_host.grid_rowconfigure(0, weight=1)
        table_host.grid_columnconfigure(0, weight=1)

        table = self.make_table(table_host, columns, headings, widths, anchors, show_vertical, show_horizontal)
        hovered = {"row_id": None}

        def set_hover(row_id):
            if hovered["row_id"] and table.exists(hovered["row_id"]):
                table.item(hovered["row_id"], tags=())
            hovered["row_id"] = row_id
            if row_id:
                table.item(row_id, tags=("hover",))

        def start_drag(event):
            table._drag_start = {"x": event.x, "y": event.y, "xview": table.xview()[0], "yview": table.yview()[0]}
            table.configure(cursor="fleur")
            return "break"

        def drag(event):
            start = getattr(table, "_drag_start", None)
            if not start:
                return "break"
            if show_horizontal:
                table.xview_moveto(max(0, min(1, start["xview"] - ((event.x - start["x"]) / max(table.winfo_width(), 1)))))
            if show_vertical:
                table.yview_moveto(max(0, min(1, start["yview"] - ((event.y - start["y"]) / max(table.winfo_height(), 1)))))
            return "break"

        def stop_drag(event):
            start = getattr(table, "_drag_start", None)
            table.configure(cursor="")
            if start and abs(event.x - start["x"]) < 12 and abs(event.y - start["y"]) < 12:
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
            set_hover(row_id)
            if row_id and hover_text_for_cell:
                hover_text = hover_text_for_cell(table.item(row_id, "values"), column_id)
                if hover_text:
                    table.configure(cursor="hand2")
                    self.set_status(hover_text)
                    return
            if row_id and hover_text_for_row:
                table.configure(cursor="hand2")
                self.set_status(hover_text_for_row(table.item(row_id, "values")))
            else:
                table.configure(cursor="")
                self.set_status(status_text)

        def clear_hover(event):
            set_hover(None)
            table.configure(cursor="")
            self.set_status(status_text)

        table.bind("<ButtonPress-1>", start_drag)
        table.bind("<B1-Motion>", drag)
        table.bind("<ButtonRelease-1>", stop_drag)
        table.bind("<Motion>", handle_hover)
        table.bind("<Leave>", clear_hover)
        if show_vertical:
            table.bind("<MouseWheel>", lambda event: (table.yview_scroll(int(-1 * (event.delta / 120)), "units"), "break")[-1])
        if show_horizontal:
            table.bind("<Shift-MouseWheel>", lambda event: (table.xview_scroll(int(-1 * (event.delta / 120)), "units"), "break")[-1])

        for row in rows:
            table.insert("", "end", values=values_for_row(row))

        self.add_footer(page, primary_text=close_text, primary_command=close_command, extra_buttons=extra_buttons)
        self.set_status(status_text)

    def check_meals(self):
        try:
            meals = load_meals()
            self.show_table_page(
                title="Meals",
                columns=("meal_id", "meal_type", "meal_name"),
                headings=("Meal ID", "Meal Type", "Meal Name"),
                widths=(100, 140, 480),
                anchors=("center", "center", "w"),
                rows=meals,
                values_for_row=lambda meal: (meal["meal_id"], meal["meal_type"], meal["meal_name"]),
                status_text=f"Loaded {len(meals)} meal(s). Click a meal to view ingredients.",
                on_row_open=lambda values: self.show_meal_ingredients(values[0], values[2], self.check_meals),
                hover_text_for_row=lambda values: f"Click to view ingredients for {values[2]}.",
            )
        except Exception as error:
            messagebox.showerror("Error", str(error))
            self.set_status("Failed to load meals.")

    def show_meal_ingredients(self, meal_id, meal_name, previous_command=None):
        self.clear_content()
        page = ctk.CTkFrame(self.content, fg_color="transparent")
        page.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        page.grid_rowconfigure(1, weight=1)
        page.grid_columnconfigure(0, weight=2)
        page.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(page, text=f"{meal_name} Ingredients", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, columnspan=2, sticky="w")

        table_host = ctk.CTkFrame(page, fg_color="transparent")
        table_host.grid(row=1, column=0, sticky="nsew", pady=(12, 0), padx=(0, 12))
        table_host.grid_rowconfigure(0, weight=1)
        table_host.grid_columnconfigure(0, weight=1)
        table = self.make_table(
            table_host,
            columns=("row_index", "ingredient", "quantity", "unit"),
            headings=("#", "Ingredient", "Quantity", "Unit"),
            widths=(45, 260, 100, 100),
            anchors=("center", "w", "center", "center"),
            show_vertical=True,
            show_horizontal=False,
        )

        editor = ctk.CTkScrollableFrame(page)
        editor.grid(row=1, column=1, sticky="nsew", pady=(12, 0))
        editor.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(editor, text="Add Or Edit Ingredient", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, sticky="w", padx=14, pady=(14, 6))
        ctk.CTkLabel(editor, text='Tap a table row to edit or remove it.', anchor='w').grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 10))
        ctk.CTkLabel(editor, text="Ingredient", anchor="w").grid(row=2, column=0, sticky="ew", padx=14)
        ingredient_entry = ctk.CTkEntry(editor)
        ingredient_entry.grid(row=3, column=0, sticky="ew", padx=14, pady=(4, 10))
        ctk.CTkLabel(editor, text="Quantity", anchor="w").grid(row=4, column=0, sticky="ew", padx=14)
        quantity_entry = ctk.CTkEntry(editor)
        quantity_entry.grid(row=5, column=0, sticky="ew", padx=14, pady=(4, 10))
        ctk.CTkLabel(editor, text="Unit", anchor="w").grid(row=6, column=0, sticky="ew", padx=14)
        unit_entry = ctk.CTkEntry(editor)
        unit_entry.grid(row=7, column=0, sticky="ew", padx=14, pady=(4, 12))

        selected = {"row_index": None}


        def clear_editor():
            selected["row_index"] = None
            ingredient_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)
            unit_entry.delete(0, tk.END)
            table.selection_remove(table.selection())

        def load_table():
            for row_id in table.get_children():
                table.delete(row_id)
            self.set_status(f"Loaded {len(items)} ingredient(s) for {meal_name}.")

        def select_ingredient(event=None):
            selection = table.selection()
            if not selection:
                return
            values = table.item(selection[0], "values")
            selected["row_index"] = values[0]
            ingredient_entry.delete(0, tk.END)
            ingredient_entry.insert(0, values[1])
            quantity_entry.delete(0, tk.END)
            quantity_entry.insert(0, values[2])
            unit_entry.delete(0, tk.END)
            unit_entry.insert(0, values[3])
            self.set_status(f"Selected ingredient: {values[1]}.")

        def add_new():
            try:
                added = add_ingredient_to_meal(meal_id, ingredient_entry.get(), quantity_entry.get(), unit_entry.get())
                load_table()
                clear_editor()
                self.set_status(f"Added ingredient: {added['ingredient']}.")
            except Exception as error:
                messagebox.showerror("Error", str(error))

        def save_changes():
            try:
                if selected["row_index"] is None:
                    raise ValueError("Select an ingredient to edit.")
                updated = update_meal_ingredient(meal_id, selected["row_index"], ingredient_entry.get(), quantity_entry.get(), unit_entry.get())
                load_table()
                clear_editor()
                self.set_status(f"Updated ingredient: {updated['ingredient']}.")
            except Exception as error:
                messagebox.showerror("Error", str(error))

        def remove_selected():
            try:
                if selected["row_index"] is None:
                    raise ValueError("Select an ingredient to remove.")
                removed = remove_meal_ingredient(meal_id, selected["row_index"])
                load_table()
                clear_editor()
                self.set_status(f"Removed ingredient: {removed['ingredient']}.")
            except Exception as error:
                messagebox.showerror("Error", str(error))

        def delete_current_meal():
            confirm = messagebox.askyesno(
                "Delete Meal",
                f"Are you sure you want to delete '{meal_name}'?"
            )

            if not confirm:
                return

            try:
                removed = delete_meal(meal_id)
                self.set_status(f"Deleted meal: {removed['meal_name']}")
                (previous_command or self.show_menu)()

            except Exception as error:
                messagebox.showerror("Error", str(error))

        ctk.CTkButton(editor, text="Add New Ingredient", height=42, command=add_new).grid(row=8, column=0, sticky="ew", padx=14, pady=(0, 8))
        ctk.CTkButton(editor, text="Remove Ingredient", height=42, command=remove_selected).grid(row=9, column=0, sticky="ew", padx=14, pady=(0, 8))
        ctk.CTkButton(editor, text="Save Changes", height=42, command=save_changes).grid(row=10, column=0, sticky="ew", padx=14, pady=(0, 8))
        ctk.CTkButton(editor, text="Delete Meal", height=42, command=delete_current_meal).grid(row=11, column=0, sticky="ew", padx=14, pady=(0, 8))
        ctk.CTkButton(editor, text="Back", height=42, command=previous_command or self.show_menu).grid(row=12, column=0, sticky="ew", padx=14, pady=(0, 14))

        table.bind("<<TreeviewSelect>>", select_ingredient)
        load_table()
        ctk.CTkButton(
            page,
            text="Back",
            height=42,
            width=140,
            command=previous_command or self.show_menu,
        ).grid(row=2, column=0, sticky="w", pady=(12, 0))

        self.add_footer(page, primary_text="Back", primary_command=previous_command or self.show_menu, extra_buttons=[("Close", self.show_menu)])

    def format_meal_plan_by_day(self, meal_plan):
        days = []
        meal_types = []
        grouped = {}
        for meal in meal_plan:
            day = meal["day"]
            meal_type = meal["meal_type"]
            if day not in grouped:
                grouped[day] = {"day": day}
                days.append(day)
            if meal_type not in meal_types:
                meal_types.append(meal_type)
            grouped[day][meal_type] = meal["meal_name"]
        return meal_types, [grouped[day] for day in days]

    def generate_meal_plan(self):
        try:
            meal_plan = load_weekly_plan()

            if not meal_plan:
                meals = load_meals()
                meal_plan = build_meal_plan(meals)
                save_weekly_plan(meal_plan)

            self.show_meal_plan(meal_plan)

        except Exception as error:
            messagebox.showerror("Error", str(error))
            self.set_status("Failed to load meal plan.")

    def regenerate_meal_plan(self):
        try:
            confirm = messagebox.askyesno(
                "Regenerate Meal Plan",
                "Generate a new weekly meal plan? This will replace the current plan."
            )

            if not confirm:
                return

            meals = load_meals()
            meal_plan = build_meal_plan(meals)
            save_weekly_plan(meal_plan)
            self.show_meal_plan(meal_plan)

        except Exception as error:
            messagebox.showerror("Error", str(error))
            self.set_status("Failed to regenerate meal plan.")

    def show_meal_plan(self, meal_plan):
        meal_types, rows = self.format_meal_plan_by_day(meal_plan)
        lookup = {
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
            return lookup.get((values[0], meal_types[column_index - 1]))

        self.show_table_page(
            title="Meal Plan",
            columns=columns,
            headings=headings,
            widths=widths,
            anchors=anchors,
            rows=rows,
            values_for_row=lambda day_plan: tuple(
                [day_plan["day"]] + [day_plan.get(meal_type, "") for meal_type in meal_types]
            ),
            status_text=f"Loaded meal plan for {len(rows)} day(s). Click a meal to view ingredients.",
            show_vertical=False,
            show_horizontal=True,
            on_cell_open=lambda values, column_id: self.show_meal_ingredients(
                *meal_from_cell(values, column_id),
                self.generate_meal_plan
            ) if meal_from_cell(values, column_id) else None,
            hover_text_for_cell=lambda values, column_id: (
                f"Click to view ingredients for {meal_from_cell(values, column_id)[1]}."
                if meal_from_cell(values, column_id)
                else None
            ),
            close_text="Back",
            close_command=self.show_menu,
            extra_buttons=[("Regenerate", self.regenerate_meal_plan)],
        )

    def generate_shopping_list(self):
        try:
            meal_ingredients = load_meal_ingredients()
            weekly_plan = load_weekly_plan()
            shopping_list = build_shopping_list(meal_ingredients, weekly_plan)
            save_shopping_list(shopping_list)

            def email_list():
                try:
                    send_shopping_list_email(shopping_list)
                    self.set_status("Shopping list emailed.")
                except Exception as error:
                    messagebox.showerror("Email Error", str(error))
                    self.set_status("Failed to email shopping list.")

            self.show_table_page(
                title="Shopping List",
                columns=("ingredient", "quantity", "unit"),
                headings=("Ingredient", "Quantity", "Unit"),
                widths=(420, 140, 140),
                anchors=("w", "center", "center"),
                rows=shopping_list,
                values_for_row=lambda item: (item["ingredient"], item["quantity"], item["unit"]),
                status_text=f"Generated {len(shopping_list)} shopping list item(s).",
                show_vertical=True,
                show_horizontal=False,
                close_text="Back",
                close_command=self.show_menu,
                extra_buttons=[("Email List", email_list)],
            )
        except Exception as error:
            messagebox.showerror("Error", str(error))
            self.set_status("Failed to generate shopping list.")

if __name__ == "__main__":
    app = KitchenMealTrackerApp()
    app.mainloop()
