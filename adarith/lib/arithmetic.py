from .number import Number
from .operation import OperationType
from .scale import ScaleType
import random

class TwoDigitArithmetic(object):
    def __init__(self, leftNumber=Number(), operation=OperationType(), rightNumber=Number()):
        self.leftNumber = leftNumber
        self.operation = operation
        self.rightNumber = rightNumber
        self.answer = self.answer()
        super().__init__()

    def __repr__(self):
        r = f'{self.leftNumber} {self.operation} {self.rightNumber} = '
        return r

    def answer(self):
        left = self.leftNumber.floatValue
        right = self.rightNumber.floatValue
        answer = 0
        if self.operation.type == OperationType.ADD:
            answer = left + right
        elif self.operation.type == OperationType.SUB:
            answer = left - right
        elif self.operation.type == OperationType.MUL:
            answer = left * right
        elif self.operation.type == OperationType.DIV:
            answer = left / right
        self.answer = answer
        return self.answer
        


class ArithmeticFactory(object):
    def __init__(self, scale=ScaleType, floor=0, ceil=10, radix=0):
        self.scale = scale
        self.floor = Number(scale=scale, absValue=floor, radix=radix)
        self.ceil = Number(scale=scale, absValue=ceil, radix=radix)
        self.radix = radix        
        super().__init__()

    def buildAritmetic(self, operation=OperationType()):
        operation = operation
        left = random.random() * (self.ceil.floatValue - self.floor.floatValue) + self.floor.floatValue
        right = random.random() * (self.ceil.floatValue - self.floor.floatValue) + self.floor.floatValue

        # Int
        if self.radix == 0: 
            left = random.randint(self.floor.decValue, self.ceil.decValue)
            right = random.randint(self.floor.decValue, self.ceil.decValue) 
            right =  right + left - 10 if right + left > 10  else right
        
        if operation.type == OperationType.SUB:
            if left < right:
                left, right = right, left
        
        twoDigitArithmetic = TwoDigitArithmetic(leftNumber=Number.of(left), operation=operation, rightNumber=Number.of(right))
        return twoDigitArithmetic



if __name__ == '__main__':
    addOperation = OperationType()
    subOperation = OperationType(OperationType.SUB)
    mulOperation = OperationType(OperationType.MUL)
    divOperation = OperationType(OperationType.DIV)

    arithmeticFactory = ArithmeticFactory()
    for i in range(0, 10):
        arithmetic = arithmeticFactory.buildAritmetic(addOperation)
        print(f'No.{i}: {arithmetic}')    

    for i in range(0, 10):
        arithmetic = arithmeticFactory.buildAritmetic(subOperation)
        print(f'No.{i}: {arithmetic}')
    
    
        
