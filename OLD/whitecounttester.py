from constants import getWhite, setWhite, getColors, setColors, popWhite

def main():
    print(getWhite())  # Output: 0
    setWhite(getWhite()+1)
    print(f"{getWhite()} white circles coming")
    setWhite(getWhite() + 1)
    print(getWhite())  # Output: 2
    setWhite(getWhite() + 1)
    print(getWhite())  # Output: 3
    setWhite(getWhite() + 1)
    print(getWhite())  # Output: 4


    print(getColors())
    setColors("G", (255, 0, 0))
    setColors("W", (255, 255, 255))
    print(getColors())
    popWhite()
    print(getColors())



if __name__ == "__main__":
    main()