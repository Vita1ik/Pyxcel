import re

SYNTAX_ERROR_MESSAGE = 'SYNTAX_ERROR'
NAN_ERROR_MESSAGE = 'NaN'

class Calculator:

    def __init__(self):
        self.line: str = ''
        self.current: str = ''

    def evaluate(self, expr):
        try:
            self.line = expr
            result = str(self._exp())
            if self.line != '':
                return SYNTAX_ERROR_MESSAGE
            return result
        except SyntaxError:
            return SYNTAX_ERROR_MESSAGE

    def _exp(self):
        result = self._term()
        while self._is_next('[-+]'):
            if self.current == '+':
                result += self._term()
            else:
                result -= self._term()
        return result

    def _term(self):
        result = self._factor()
        while self._is_next('[*/]'):
            if self.current == '*':
                result *= self._factor()
            else:
                try:
                    result /= self._factor()
                except ZeroDivisionError:
                    result = NAN_ERROR_MESSAGE
        return result

    def _factor(self):
        if self._is_next(r'[0-9]*\.?[0-9]+'):
            return float(self.current) if '.' in self.current else int(self.current)
        if self._is_next('-'):
            return -self._factor()
        if self._is_next('[(]'):
            result = self._exp()
            if not self._is_next('[)]'):
                raise SyntaxError()
            return result
        raise SyntaxError()

    def _is_next(self, regexp: str):
        m = re.match(r'\s*' + regexp + r'\s*', self.line)
        if m:
            self.current = m.group().strip()
            self.line = self.line[m.end():]
            return True
        return False
