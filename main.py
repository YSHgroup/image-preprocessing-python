# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
txt = "I love apples/, apple ar\e my favo/rite \fruit"

x = txt.count("/") + txt.count('\f')
i = txt.rindex('/')
i_1 = txt.rindex('\\')
print(x, i, i_1)
print(max(i, i_1))