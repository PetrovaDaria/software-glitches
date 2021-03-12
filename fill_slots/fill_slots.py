def empty_func(text):
    return []


def fill_slots(
        text,
        glitch_type_func=empty_func,
        victim_func=empty_func,
        manufacturer_func=empty_func,
        duration_func=empty_func,
        severity_func=empty_func,
        money_func=empty_func,
        other_loss_func=empty_func,
        reason_func=empty_func
):
    glitch_type = glitch_type_func(text)
    victims = victim_func(text)
    manufacturer = manufacturer_func(text)
    duration = duration_func(text)
    severity = severity_func(text)
    money = money_func(text)
    other_loss = other_loss_func(text)
    reason = reason_func(text)

    return {
        # hardware/software/network
        'glitch_type': glitch_type,
        # company-victim
        'victim': victims,
        # company-maker of glitched software
        'manufacturer': manufacturer,
        # duration of glitch
        'duration': duration,
        'severity_scale': severity,
        'money_loss': money,
        'other_loss': other_loss,
        'reason': reason
    }
