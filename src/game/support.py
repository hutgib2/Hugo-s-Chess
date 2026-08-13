def get_direction_between(start, end):
    drow = end[0] - start[0]
    dcol = end[1] - start[1]
    if drow != 0:
        drow = drow / abs(drow)

    if dcol != 0:
        dcol = dcol / abs(dcol)

    return (int(drow), int(dcol))
