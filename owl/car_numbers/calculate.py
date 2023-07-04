def calc_checksum(number: str):
    if len(number) == 12:
        number = number[0:11]
    if len(number) != 11:
        raise Exception("Number should have 11 or 12 digits")

    sum = 0
    for i in range(11):
        factor = (2 - i % 2)
        mul = int(number[i]) * factor
        sum += mul // 10 + mul % 10
    check = (10 - sum % 10) % 10
    return str(check)


def check_checksum(number: str):
    if len(number) != 12:
        raise Exception("Number should have 12 digits")

    chk = calc_checksum(number)
    return chk == number[-1]


def calc_digit(number: str, pos: int):
    if len(number) != 12:
        raise Exception("Number should have 12 digits")

    if pos == 11:
        return calc_checksum(number)
    else:
        sum = 0
        for i in range(11):
            if i != pos:
                factor = (2 - i % 2)
                mul = int(number[i]) * factor
                sum += mul // 10 + mul % 10
        check = (10 - sum % 10) % 10

        subst = (check - int(number[11])) % 10
        factor = (2 - pos % 2)
        digit = (subst % factor) * 5 + subst // factor

        return digit


if __name__ == "__main__":
    # print (calc_checksum("21513846029")) # 4
    # print (check_checksum("215138460294")) # True
    # print (check_checksum("215138460292")) # False

    print (calc_digit("215138460294", 0))
    print (calc_digit("215138460294", 1))
    print (calc_digit("215138460294", 2))
    print (calc_digit("215138460294", 3))
    print (calc_digit("215138460294", 4))
    print (calc_digit("215138460294", 5))
    print (calc_digit("215138460294", 6))
    print (calc_digit("215138460294", 7))
    print (calc_digit("215138460294", 8))
    print (calc_digit("215138460294", 9))
    print (calc_digit("215138460294", 10))
    print (calc_digit("215138460294", 11))