class Nanobot:
    def __init__(self):
        self.logic = []

    def display_logic(self):
        if not self.logic:
            print("No logic lines added.")
        else:
            print("\nCurrent Logic:")
            for index, line in enumerate(self.logic, start=1):
                print(f"{index}: {line}")

    def add_logic_line(self, line):
        self.logic.append(line)
        print(f'Added logic line: "{line}"')

    def edit_logic_line(self, index, new_line):
        if 0 <= index < len(self.logic):
            old_line = self.logic[index]
            self.logic[index] = new_line
            print(f'Edited logic line {index + 1}: "{old_line}" -> "{new_line}"')
        else:
            print("Invalid index. No line edited.")

    def delete_logic_line(self, index):
        if 0 <= index < len(self.logic):
            removed_line = self.logic.pop(index)
            print(f'Removed logic line: "{removed_line}"')
        else:
            print("Invalid index. No line deleted.")

def main():
    nanobot = Nanobot()
    print("Welcome to the Nanobot Logic Editor!")

    while True:
        print("\nMenu:")
        print("1. Add Logic Line")
        print("2. Edit Logic Line")
        print("3. Delete Logic Line")
        print("4. Display Current Logic")
        print("5. Confirm Logic")
        print("6. Exit")

        choice = input("Choose an option (1-6): ")

        if choice == '1':
            line = input("Enter the logic line: ")
            nanobot.add_logic_line(line)

        elif choice == '2':
            nanobot.display_logic()
            index = int(input("Enter the line number to edit: ")) - 1
            new_line = input("Enter the new logic line: ")
            nanobot.edit_logic_line(index, new_line)

        elif choice == '3':
            nanobot.display_logic()
            index = int(input("Enter the line number to delete: ")) - 1
            nanobot.delete_logic_line(index)

        elif choice == '4':
            nanobot.display_logic()

        elif choice == '5':
            print("\nFinal Logic Confirmed:")
            print("\n".join(nanobot.logic))
            break  # Exit after confirming logic

        elif choice == '6':
            print("Exiting the editor. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
