class Calculator {

    // Initializes the previous and current Operands
    constructor(previousOperandTextElement, currentOperandTextElement) {

        // Sets elements as objects within Calc class
        this.previousOperandTextElement = previousOperandTextElement
        this.currentOperandTextElement = currentOperandTextElement
        // A call to clear function once calculator is initialized, clear operands and opperator
        this.clear()
    }

    clear() {
        this.currentOperand = ''
        this.previousOperand = ''
        this.opperation = undefined
    }

    delete() {
        // Slice will copy the first to 'second to last' element, essentially deleting the last character
        this.currentOperand = this.currentOperand.toString().slice(0, -1)
    }

    // Function to append a number to the current operand
    appendNumber(number) {
        // Ensures operand will not have more than 1 decimal
        if (number === '.' && this.currentOperand.includes('.')) return
        // Appends the number from the button to the original
        this.currentOperand = this.currentOperand.toString() + number.toString()

    }

    // Function to choose operation once button is pressed
    chooseOperation(operation) {
        // Ensures current operand exists
        if (this.currentOperand === '') return
        // If there is a previous operand, use the selected operation on it and compute
        if (this.previousOperand !== '') {
            this.compute()
        }
        // Initializes operation as an object
        this.operation = operation
        // Sets the previous operation to what was current (preparing for calculation)
        this.previousOperand = this.currentOperand
        // Sets current to an empty string
        this.currentOperand = ''
    }

    // Function to computer both operands using the given operation
    compute() {
        let computation
        // Convert operands to floats and store in vars
        const prev = parseFloat(this.previousOperand)
        const current = parseFloat(this.currentOperand)
        // Ensure both are numbers, otherwise stop executing this function
        if (isNaN(prev) || isNaN(current)) return
        // Switch statement to caculate based on operation
        switch (this.operation) {
            case '+':
                computation = prev + current
                break
            case '-':
                computation = prev - current
                break
            case '*':
                computation = prev * current
                break
            case '÷':
                computation = prev / current
                break
            default:
                return
        }
        // Set current operand to display result
        this.currentOperand = computation
        // Set operation as undefined for next use
        this.operation = undefined
        // Clear previous op for next use
        this.previousOperand = ''
    }

    getDisplayNumber(number) {
        // Convert number to string
        const stringNumber = number.toString()
        // Getting to integer, ignoring the numbers after the decimal
        // Creates an array, splits it at the decimal, gets the first part of the array, and makes it a float
        const integerDigits = parseFloat(stringNumber.split('.')[0])
        // Gets the decimal part of the number only
        const decimalDigits = stringNumber.split('.')[1]
        let integerDisplay
        // If integer is not a number, make display an empty string
        if (isNaN(integerDigits)) {
            integerDisplay = ''
        // If it is a number, use Locale String fuct to add commas just to the digits and update display
        } else {
            integerDisplay = integerDigits.toLocaleString('en', {
                // Ensures there are no fraction digits (numbers after a decimal)
                maximumFractionDigits: 0
            })
        }
        // If decimal digits exist, return the newly formatted number with decimal digits
        if (decimalDigits != null) {
            return `${integerDisplay}.${decimalDigits}`
        // Or just return the newly formatted integer
        } else {
            return integerDisplay
        }
    }

    updateDisplay() {
        // Set the inner text in the HTML to the formated number from above funct
        this.currentOperandTextElement.innerText = this.getDisplayNumber(this.currentOperand)

        // If there is an operation, set prev op with operation after
        if (this.operation != null) {
            this.previousOperandTextElement.innerText = `${this.getDisplayNumber(this.previousOperand)} ${this.operation}`
        } else {
            this.previousOperandTextElement.innerText = ''
        }
    }
}

// Setting constants for all the buttons on calculator 
const numberButtons = document.querySelectorAll('[data-number]')
const operationButtons = document.querySelectorAll('[data-operation]')
const equalsButton = document.querySelector('[data-equals]')
const deleteButton = document.querySelector('[data-delete]')
const allClearButton = document.querySelector('[data-all-clear]')
const previousOperandTextElement = document.querySelector('[data-previous-operand]')
const currentOperandTextElement = document.querySelector('[data-current-operand]')

// Initializing calc object
const calculator = new Calculator(previousOperandTextElement, currentOperandTextElement)

// Adding event listeners for buttons and calling proper functions

numberButtons.forEach(button => {
    button.addEventListener('click', () => {
        calculator.appendNumber(button.innerText)
        calculator.updateDisplay()
    })
})

operationButtons.forEach(button => {
    button.addEventListener('click', () => {
        calculator.chooseOperation(button.innerText)
        calculator.updateDisplay()
    })
})

equalsButton.addEventListener('click', button => {
    calculator.compute()
    calculator.updateDisplay()
})

allClearButton.addEventListener('click', button => {
    calculator.clear()
    calculator.updateDisplay()
})

deleteButton.addEventListener('click', button => {
    calculator.delete()
    calculator.updateDisplay()
})
