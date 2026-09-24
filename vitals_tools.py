"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """TODO: describe what this pulls out of the encounter records."""
    # TODO: collect the systolic value of every encounter into one list.
    sys_readings = []
    for encounter in encounters:
        sys_readings.append(encounter[2])
    return sys_readings

    


def mean_systolic(readings):
    """TODO: describe what this returns, including the empty-list result."""
    # returns the mean systolic BP for all readings
    # TODO: return None when there is nothing to average, then sum() / len().
    
    if not readings:
        return None

    return sum(readings) / len(readings)
    


def count_patients(encounters):
    """TODO: describe what this counts."""
    # returns number of unique patient IDs
    # TODO: collect the patient IDs and keep only the distinct ones.
    return (len({encounter[0] for encounter in encounters}))



def patients_at_or_above(encounters, cutoff):
    """TODO: describe which patient IDs come back."""
    # omits patients who systolic BP reading is below the cutoff
    # TODO: keep each patient whose systolic reading is at or above cutoff.
    return {encounter[0] for encounter in encounters if encounter[2] >= cutoff}


