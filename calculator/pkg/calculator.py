# calculator.py

class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()
        postfix_tokens = self._infix_to_postfix(tokens)
        return self._evaluate_postfix(postfix_tokens)

    def _infix_to_postfix(self, tokens):
        output = []
        operators = []
        for token in tokens:
            if token in self.operators:
                while operators and self.precedence[token] <= self.precedence[operators[-1]]:
                    output.append(operators.pop())
                operators.append(token)
            else:
                output.append(token)
        while operators:
            output.append(operators.pop())
        return output

    def _evaluate_postfix(self, tokens):
        stack = []
        for token in tokens:
            if token in self.operators:
                operand2 = float(stack.pop())
                operand1 = float(stack.pop())
                result = self.operators[token](operand1, operand2)
                stack.append(result)
            else:
                stack.append(token)
        return float(stack[0])