


def smooth_command(des, cur, t, T=1):
    if t < T/2:
        return C1(des, cur, t, T)
    elif t < T:
        return C2(des, cur, t, T)
    else:
        return des


def C1(des, cur, t, T):
    out = (2/T**2) * (des - cur) * t**2 + cur

    return out


def C2(des, cur, t, T):
    out = (2/T**2) * (cur - des) * (t-T)**2 + des

    return out