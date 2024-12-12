import re
from models.cell import Cell
from modules.calculator import Calculator

ADDRESS_ERROR_MESSAGE = 'REF'

class ExpressionEvaluator:
    def __init__(self, cell_address):
        self.cell_address = cell_address

    def evaluate(self, expr):
        if expr.startswith("="):
            expr = expr[1:]
        if expr == None:
            return ''
        if self.cell_address in expr:
            return ADDRESS_ERROR_MESSAGE

        addresses = self.__find_cell_addresses(expr)
        if len(addresses) > 0:
            cells = Cell.where(addresses)
            if len(cells) > 0:
                if len(set(addresses)) != len(cells):
                    return ADDRESS_ERROR_MESSAGE
                cell_values = {cell['address']: cell['text'] for cell in cells}
                print(cell_values)
                expr = self.__find_cell_and_replace(expr, cell_values)

        return Calculator().evaluate(expr)


    def __find_cell_addresses(self, expr):
        pattern = r'\b[A-Z]+\d+\b'
        matches = re.findall(pattern, expr)
        return matches

    def __find_cell_and_replace(self, expr, cell_values):
        pattern = r'\b[A-Z]+\d+\b'

        def replace_with_value(match):
            cell_address = match.group(0)
            return str(cell_values.get(cell_address, cell_address))

        modified_text = re.sub(pattern, replace_with_value, expr)
        return modified_text
