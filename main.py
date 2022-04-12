import numpy
from random import randint
import os
import json
import string
import colorama


fore, back, = colorama.Fore, colorama.Back

class MatrixPinLock:

    def __init__(self):
        self.log = []
        self.sorted_PinLock = self.pinLock()
        random = self.random_pinLock(self.pinLock())
        random[:] = self.random_pinLock(random)
        self.random = random
        self.alphabet = []

        self.text = """"""
        self.clear = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

        for c in string.printable:
            self.alphabet.append(c)
        self.alphabet.sort()

    def encoder(self, string=str, shift=int):  # translate the text into random asccii characters
        encoded_alphabet = {}  # used for shifting the values
        emptyString = ''  # empty string add the new translated text character by character
        shifted = self.alphabet[shift:] + self.alphabet[:shift]  # shift the variable "alphabet"

        for i in range(len(self.alphabet)):  # the variable "i" in the for loop is the index of the variable "alphabet"
            encoded_alphabet[shifted[i]] = self.alphabet[i]  # adds the new key-value shifted pairs to the dictionary
        for c in string:  # c contains the characters of the text (prints character by character
            emptyString = emptyString + encoded_alphabet[
                c]  # replace the characters of the text to the new shifted character
        return emptyString  # (doesn't return an empty estring lol) # return the new encoded text

    def decoder(self, string, shift=int):  # is the same proccess of encoded Object but in reverse:
        encoded_alphabet = {}
        emptyString = ''
        shifted = self.alphabet[shift:] + self.alphabet[:shift]

        for i in range(len(self.alphabet)):
            encoded_alphabet[self.alphabet[i]] = shifted[i]
        for c in string:
            emptyString = emptyString + encoded_alphabet[c]
        return emptyString

    def pinLock(self)->list:
        numberList = []
        pinlock = []

        for i in range(1, 10):
            numberList.append(i)
            pinlock.append(numberList)
        return pinlock

    def vShift(self, pinlock=list, shift=None, column=None, random=False)->list:
        randomPinLock = []
        randomPinLock_ = []
        numberList = []

        shape = numpy.shape(pinlock)

        if shape[1]:
            for numberlist in numpy.column_stack(pinlock):
                for nums in numberlist:
                    numberList.append(nums)
                randomPinLock_.append(numberList[:shape[1]:])
                del numberList[:shape[1]:]
            if random == True:

                for numberlist in randomPinLock_:
                    shift_ = randint(-8, 8)
                    numberlist = numberlist[shift_:] + numberlist[:shift_]
                    randomPinLock.append(numberlist)
            else:
                shift_ = shift
                randomPinLock_[column] = randomPinLock_[column][shift_:] + randomPinLock_[column][:shift_]
                for numberlist in randomPinLock_:
                    randomPinLock.append(numberlist)

            numberList.clear()
            randomPinLock_.clear()

            for numberlist in numpy.column_stack(randomPinLock):
                for nums in numberlist:
                    numberList.append(nums)
                randomPinLock_.append(numberList[:shape[1]:])
                del numberList[:shape[1]:]

            return randomPinLock_

    def hShift(self, pinlock=list, shift=int, row=int, random=False):

        randomPinLock = []
        pinlock[row] = pinlock[row][shift:] + pinlock[row][:shift]
        for numberlist in pinlock:
            randomPinLock.append(numberlist)

        if random == True:
            for numberlist in pinlock:
                shift += randint(-8, 8)
                numberlist = numberlist[shift:] + numberlist[:shift]
                randomPinLock.append(numberlist)

        return randomPinLock

    def random_pinLock(self, pinlock=list)->list:
        randomPinLock = []
        h_shift = 0

        for numberlist in pinlock:
            h_shift += randint(-8, 8)
            numberlist = numberlist[h_shift:] + numberlist[:h_shift]
            randomPinLock.append(numberlist)


        randomPinLock[:] = self.vShift(randomPinLock, random=True)
        return randomPinLock

    def manipulate(self, pinlock=list):
        commands = ['v', 'h', 'r', 'c', 'log', 'save', 'q', 'done', 'load', 'doc']

        solved = False

        while solved == False:

            try:
                original = self.sorted_PinLock
                user = input('type here: ')
                analyze = user.split()  # example: -ver -column 3 6
                matrixPinLock = pinlock



                if analyze[0] == 'add' and analyze[1] == 'textfile' and '.txt' in analyze[2]:
                    cwd = os.getcwd()
                    path = os.path.join(cwd, analyze[2])

                    with open(path, 'r') as f:
                        read = f.read()

                        self.text = read
                        print(fore.GREEN, '\ntext added!\n', fore.RESET)
                        continue

                if analyze[0] == 'show':
                    print(back.RED, '\n', numpy.vstack(matrixPinLock), '\n', back.RESET)
                    continue

                if analyze[0] == 'encode' and analyze[1].isdigit():
                    encode = self.encoder(self.text, int(analyze[1]))
                    self.text = encode
                    with open('message.txt', 'w') as f:
                        write = f.write(self.text)
                    print(fore.GREEN, '\nmessage have been encoded!\n', fore.RESET)
                    continue

                if analyze[0] == commands[-1]:
                    with open('doc', 'r') as f:
                        read = f'\n\n\n{f.read()}\n\n\n'
                        self.clear()
                        print(fore.BLUE, read, fore.RESET)
                        continue

                if analyze[0] == commands[4]:
                    for log in self.log:
                        print(fore.CYAN, log, '\n', fore.RESET)
                    continue

                if analyze[0] == commands[6]:
                    self.log.append(user)
                    quit()

                if analyze[0] == commands[7]:
                    if matrixPinLock == original:
                        self.log.append(user)
                        return matrixPinLock
                    else:
                        print(fore.RED, 'not solved.', fore.RESET)
                        self.log.append(user)
                        continue

                if solved == True:
                    return solved

                if analyze[0] == commands[5] and analyze[1]:
                    with open(analyze[1], 'w') as f:
                        for i in range(len(matrixPinLock)):
                            matrixPinLock[i] = [int(x) for x in matrixPinLock[i]]
                        save = json.dump(list(matrixPinLock), f)
                        print(fore.GREEN, '\tmatrix saved successfully!', fore.RESET)
                        self.log.append(user)
                        continue

                if analyze[0] == commands[8] and analyze[1]:
                    with open(analyze[1], 'r') as f:
                        load = json.load(f)
                        matrixPinLock[:] = load
                        print(fore.GREEN, '\tmatrix loaded successfully!', fore.RESET)
                        self.log.append(user)
                        continue

                if analyze[3]:

                    mode, r_c, position, shift = analyze[0], analyze[1], int(analyze[2]), int(analyze[3])


                    if commands[0] == analyze[0] and commands[3] == analyze[1]: # vertically
                        if analyze[2].isdigit() and shift:

                            shiftV = self.vShift(matrixPinLock, shift, position-1)
                            matrixPinLock[:] = shiftV
                            if matrixPinLock == original:
                                print(back.GREEN, '\n', numpy.vstack(matrixPinLock), '\n', back.RESET)
                                solved = True
                            self.clear()
                            print(back.RED, '\n', numpy.vstack(matrixPinLock), '\n', back.RESET)




                    if commands[1] == analyze[0] and commands[2] == analyze[1]: # horizontally
                        if analyze[2].isdigit() and shift:

                            shiftH = self.hShift(matrixPinLock, shift, position-1)
                            matrixPinLock[:] = shiftH
                            if matrixPinLock == original:
                                print(back.GREEN, '\n', numpy.vstack(matrixPinLock), '\n', back.RESET)
                                solved = True
                            self.clear()
                            print(back.RED, '\n', numpy.vstack(matrixPinLock), '\n', back.RESET)

                self.log.append(user)
            except Exception as e:
                self.log.append([user, f'-{e}'])
                print(back.YELLOW, f'\n\n\t{e}\n\n', back.RESET)
                continue

        return matrixPinLock



    def revealMessage(self, puzzle=list, originalMatrix=list):
        if puzzle == originalMatrix:
            while True:
                try:

                        user = int(input('decode: '))
                        with open('message.txt', 'r') as f:
                            self.text = f.read()
                        decode = self.decoder(string=self.text, shift=user)
                        return decode


                except Exception as e:
                    print(e)
                    continue








mpl = MatrixPinLock()
pinlock = mpl.pinLock()

print(back.GREEN, numpy.vstack(pinlock), '\n', back.RESET)
print(back.RED, numpy.vstack(mpl.random), '\n', back.RESET)

mPuzzle = mpl.manipulate(pinlock=mpl.random)
for i in range(len(mPuzzle)):
    mPuzzle[i] = [int(x) for x in mPuzzle[i]]

print(fore.LIGHTGREEN_EX, mpl.revealMessage(mPuzzle, mpl.sorted_PinLock), fore.RESET)
