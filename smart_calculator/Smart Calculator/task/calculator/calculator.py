# write your code here
import re
from collections import deque

variables = {}


def operation(a, b, operand):
    if operand == "+":
        return int(a) + int(b)
    elif operand == "-":
        return int(a) - int(b)
    elif operand == "*":
        return int(a) * int(b)
    elif operand == "/":
        return int(a) // int(b)


def convert_infix_postfix(expression):
    postfix_result = ""
    operators = deque()
    for idx, i in enumerate(expression):
        if i == ' ':
            postfix_result = postfix_result + ' '
        elif i not in ['+', '-', '*', '/', '(', ')'] or (i == '-' and re.search('^\d$', expression[idx + 1])):
            postfix_result = postfix_result + i
        else:
            if not len(operators) or operators[-1] == '(':
                operators.append(i)
            elif i == '(':
                operators.append(i)
            elif i == ')' and '(' not in operators:
                return False
            elif i == ')':
                j = operators.pop()
                while j != '(':
                    postfix_result = postfix_result + ' ' + j
                    if len(operators):
                        j = operators.pop()
                    else:
                        break
            elif i in ['/', '*'] and operators[-1] in ['+', '-']:
                operators.append(i)
            else:
                j = operators.pop()
                while j != '(':
                    postfix_result = postfix_result + ' ' + j
                    if len(operators) and ((i in ['/', '*'] and operators[-1] not in ['+', '-']) or ((i in ['+', '-'] and operators[-1] not in ['/', '*']))):
                        j = operators.pop()
                    else:
                        break
                operators.append(i)
    if len(operators) and '(' not in operators:
        for _ in range(len(operators)):
            postfix_result = postfix_result + ' ' + operators.pop()
    elif '(' in operators:
        return False
    postfix_result = re.sub(' +', ' ', postfix_result)
    return postfix_result


def calculate_postfix(expression):
    expression = replace_variable_values(expression)
    if not expression:
        return False
    elements = expression.split()
    numbers = deque()
    for ele in elements:
        if ele in ['+', '-', '*', '/']:
            num2 = numbers.pop()
            num1 = numbers.pop()
            numbers.append(operation(num1, num2, ele))
        else:
            numbers.append(ele)
    return numbers.pop()


def calculate_result(expression, start=True):
    if expression and not re.search('^(-?\d* (\+|-) -?\d*)', expression):
        return expression
    result = 0
    if start:
        first_op = re.search('^(-?\d* (\+|-) -?\d*)', expression).group()
        operand = re.search(' (\+|-) ', first_op).group()
        result += operation(a=first_op[:first_op.index(operand)],
                            b=first_op[first_op.index(operand) + 3:],
                            operand=operand.strip())
        expression = expression[len(first_op) + 1:]
    while expression:
        temp_exp = re.search('^((\+|-) \d*)', expression).group()
        operand = temp_exp[0].strip()
        result = operation(a=result, b=temp_exp[2:], operand=operand)
        expression = expression[len(temp_exp) + 1:]
    return result


def pre_process_expression(expression):
    expression = re.sub('(---)+', '-', expression)
    expression = re.sub('(--)+', '+', expression)
    expression = re.sub('\++', '+', expression)
    expression = re.sub('\+-', '-', expression)
    expression = re.sub('-\+', '+', expression)
    expression = re.sub('((-|\+)?\d+)\+((-|\+)?\d+)', r'\1 + \3', expression)
    expression = re.sub('((-|\+)?\d+)-((-|\+)?\d+)', r'\1 - \3', expression)
    expression = re.sub('((-|\+)?\d+)\*((-|\+)?\d+)', r'\1 * \3', expression)
    expression = re.sub('((-|\+)?\d+)\/((-|\+)?\d+)', r'\1 / \3', expression)
    expression = re.sub('\+(\d+)', r'+ \1', expression)
    expression = re.sub('(([-\*\/\+])\()', r'\2 (', expression)
    expression = re.sub('(\)([-\*\+\/]))', r') \2', expression)
    expression = re.sub(' +', ' ', expression)
    if re.search('^(\+)*\d*$', expression):
        expression = re.sub("\+", "", expression)
    if '=' in expression:
        expression = re.sub("( *= *)", "=", expression)
    return expression


def check_input(inp_str):
    if inp_str == '/exit':
        return "exit"
    elif inp_str == "/help":
        return "help"
    elif inp_str.startswith("/"):
        return "bad command"
    elif re.search('=', inp_str):
        return "assignment" + inp_str
    elif (re.search('(-|\+\*\/)$|(\d+([^-\+\*\/])+\d+)', inp_str) and not re.search('^(-|\+)*\d*$', inp_str)) \
            or '**' in inp_str or '//' in inp_str:
        return "bad expression"
    else:
        return inp_str


def replace_variable_values(expression):
    matches = re.findall('([a-z]+)', expression)
    for match in matches:
        try:
            expression = expression.replace(match, variables.get(match))
        except TypeError:
            return False
    return expression


def assign_variables(expression):
    if "=" not in expression:
        if "+" in expression or "-" in expression:
            expression = replace_variable_values(expression)
            return calculate_result(expression)
        if re.search('[^-\+\sa-zA-Z]', expression):
            return "Invalid identifier"
        elif variables.get(expression):
            return variables.get(expression)
        else:
            return "Unknown variable"
    if expression.count("=") != 1:
        return "Invalid assignment"
    var, val = expression.split('=')
    if re.search('[^a-zA-Z]', var):
        return "Invalid identifier"
    if (re.search('[a-zA-Z]', val) and re.search('[^a-zA-Z]', val)):
        return "Invalid assignment"
    elif len(re.search('([a-zA-Z]*)', val).group()) == len(val):
        if variables.get(val):
            val = variables.get(val)
        else:
            return "Unknown variable"
    variables[var] = val
    return None


while True:
    in_str = input().strip()

    if not in_str:
        continue
    in_str = check_input(in_str)
    if in_str == 'exit':
        print('Bye!')
        break
    elif in_str == "help":
        print("""The program calculates:
         1. Sum 
         2. Subtraction
         3. Multiplication 
         4. Division """)
    elif in_str == "bad command":
        print("Unknown command")
    elif in_str == "bad expression":
        print("Invalid expression")
    elif "assignment" in in_str:
        in_str = in_str.replace("assignment", "")
        in_str = pre_process_expression(in_str)
        result = assign_variables(in_str)
        if result:
            print(result)
    else:
        in_str = pre_process_expression(in_str)
        in_str = convert_infix_postfix(in_str)
        if in_str:
            result = calculate_postfix(in_str)
            if result or str(result) == "0":
                print(result)
            else:
                print('Unknown variable')
        else:
            print('Invalid expression')
