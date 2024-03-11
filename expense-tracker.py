import sqlite3

# Establishing connection and cursor
with sqlite3.connect('personal_finance.db') as conn:
    c = conn.cursor()

    # Creating the table if it doesn't exist
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS finances (
        id INTEGER PRIMARY KEY,
        finance_type STRING,
        amount FLOAT,
        category STRING
    );
    """
    c.execute(create_table_sql)
    conn.commit()

    while True:
        print("Please choose an option:")
        print("1. Enter income")
        print("2. Enter expenses")
        print("3. View balance")
        print("4. View income")
        print("5. View expenses")
        print("6. Delete expense/income")
        print("7. Update expense/income")
        print("8. Exit")
        option = int(input("Select your option: "))

        if option == 1:
            finance_type = "Income"
            amount = float(input("Enter the income amount: "))
            category = str(input("Enter income category: "))
            insert_data_sql = "INSERT INTO finances (finance_type, amount, category) VALUES (?,?,?)"
            c.execute(insert_data_sql, (finance_type, amount, category))

        elif option == 2:
            finance_type = "Expenses"
            amount = float(input("Enter the expense amount: "))
            category = str(input("Enter expense category: "))
            insert_data_sql = "INSERT INTO finances (finance_type, amount, category) VALUES (?,?,?)"
            c.execute(insert_data_sql, (finance_type, amount, category))

        elif option == 3:
            select_balance_sql = """
                SELECT
                    SUM(CASE WHEN finance_type = 'Income' THEN amount ELSE 0 END) - SUM(CASE WHEN finance_type = 'Expenses' THEN amount ELSE 0 END) AS balance
                FROM finances
            """
            c.execute(select_balance_sql)
            balance = c.fetchone()
            print(f"Your balance: {balance}")

        elif option == 4:
            select_income_sql = """
                 SELECT id, finance_type, amount, category
                 FROM finances
                 WHERE finance_type = 'Income'
            """
            c.execute(select_income_sql)
            income_report = c.fetchall()

            for income in income_report:
                print("ID:", income[0])
                print("finance_type:", income[1])
                print("amount:", income[2])
                print("category:", income[3])

        elif option == 5:
            select_expenses_sql = """
                 SELECT id, finance_type, amount, category
                 FROM finances
                 WHERE finance_type = 'Expenses'
            """
            c.execute(select_expenses_sql)
            expense_report = c.fetchall()

            for expense in expense_report:
                print("ID:", expense[0])
                print("finance_type:", expense[1])
                print("amount:", expense[2])
                print("category:", expense[3])

        elif option == 6:
            delete_input = int(input("Enter the row ID: "))
            delete_input_sql = """
                 DELETE FROM finances
                 WHERE id = ?
            """
            c.execute(delete_input_sql, (delete_input,))

        elif option == 7:
            update_row = int(input("Enter the row ID: "))
            update_column = str(input("Enter the column you wish to update (finance_type, amount, category): "))

            if update_column in ['finance_type', 'amount', 'category']:
                updated_value = input("Enter the new value: ")
                update_data_sql = f"""
                        UPDATE finances
                        SET {update_column} = ?
                        WHERE id = ?
                    """
                c.execute(update_data_sql, (updated_value, update_row))
            else:
                print("Invalid column name")

        elif option == 8:
            print("Thank you for using the finance tracker")
            exit()

        else:
            print("The selected option does not exist")
