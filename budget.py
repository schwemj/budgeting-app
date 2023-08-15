
class Category:
    category = ''
    balance = 0.0
    result = ''

    def __init__(self, cat):
        self.category = cat  # category name
        self.ledger = []  # ledger for each cat collecting history

    def check_funds(self, amount):
        if amount > self.balance:  # check if funds are sufficient
            return False
        else:
            return True

    def deposit(self, amount, description=''):
        self.ledger.append({"amount": amount, "description": description})  # append history to ledger
        self.balance += amount  # update amount

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):  # only execute if funds are sufficient
            self.ledger.append({"amount": -amount, "description": description})  # append history to ledger
            self.balance -= amount  # update amount
            return True
        else:
            return False

    def transfer(self, amount, destination):  # apply withdraw and deposit methods
        if self.check_funds(amount):  # only execute if funds are sufficient
            self.withdraw(amount, description='Transfer to ' + destination.category)
            destination.deposit(amount, description='Transfer from ' + self.category)
            return True
        else:
            return False

    def get_balance(self):  # return current balance
        return self.balance

    def __str__(self):  # print budget history

        left_stars = '*' * (15 - len(self.category) // 2)
        right_stars = '*' * (15 - len(self.category) // 2)
        title = left_stars + self.category + right_stars

        self.result += title + '\n'  # adding category title to result str

        for item in self.ledger:
            num_str = '{:.2f}'.format(item['amount'])
            if len(num_str) > 7:  # enforcing 7-char max
                num_str = num_str[:4] + '...'  # visual hint implying longer number
            if len(item['description']) > 23:  # shortens description str
                self.result += item['description'][:23] + ' ' + num_str + '\n'  # append result str
            else:
                str_len = len(num_str) + len(item['description'])
                self.result += item['description'] + ' ' * (30 - (str_len)) + num_str + ('\n')  # append result str

        self.result += 'Total: ' + '{:.2f}'.format(self.balance)  # display total

        return self.result


def create_spend_chart(categories):
    lines = ['Percentage spent by category',
             '100|',
             ' 90|',
             ' 80|',
             ' 70|',
             ' 60|',
             ' 50|',
             ' 40|',
             ' 30|',
             ' 20|',
             ' 10|',
             '  0|',
             '    -']  # for printing

    all_withdrawals = []  # will collect name, withdrawn total, percentage for each cat
    total_spent = 0

    for cat in categories:
        withdrawals = []  # separate list for each cat
        for item in cat.ledger:
            if item['amount'] < 0:  # if amount negative (=withdrawn)
                withdrawals.append(item['amount'])
                total_spent += item['amount']  # add to total
        all_withdrawals.append([cat.category, round(sum(withdrawals), 2)])  # add name and total for each cat

    total_spent = round(total_spent, 2)  # round total

    max_str = 0

    for a in all_withdrawals:
        # a.append(int(round((a[1] / total_spent)*100,-1))) # appends percentage for each cat
        a.append(int((a[1] / total_spent * 100)))
        if len(a[0]) > max_str:  # finds longest str
            max_str = len(a[0])

    str_count = ['' for a in range(max_str)]  # collects characters in one column per cat

    o = []  # collecting o's for percentage bars

    for a in all_withdrawals:  # appends str_count for vertical printing
        lines[12] += '---'  # 3 dashes for each column
        string = a[0]
        perc = int(a[2] / 10)
        spaces = ' ' * (max_str - len(string))
        string += spaces  # adds spaces to strings shorter than max_str to make them even
        for i in range(len(str_count)):
            str_count[i] += string[i] + '  '  # add chars to columns + spacing

        o.append('o' * perc + 'o')  # append o

    for bar in o:  # insert o's into each line
        idx = 11  # start at line 12 (0) and crawl up to line 1 (100)
        for b in bar:
            lines[idx] += ' ' + b + ' '
            idx -= 1

    for st in str_count:
        lines.append(' ' * 5 + st)  # append chars + add spacing in front of columns

    target_len = len(lines[-1])

    for line in lines[1:]:
        len_dif = target_len - len(line)
        if len_dif != 0:
            line += ' ' * len_dif

    chart = ''  # what will print

    for line in lines:
        chart += line + '\n'

    return chart
