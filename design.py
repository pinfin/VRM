from math import pi


class Geometry:

    def __init__(self):
        # design radius
        self.r_inner = None
        self.r_outer = None
        self.r_nozzle = None
        self.r_valve = None

        # design thickness
        self.thickness = None
        self.inner_thickness = None
        self.outer_thickness = None

        # design angle
        self.angle_slot = None
        self.angle_nozzle = None

        # design high
        self.high = None
        self.high_slot = None
        self.high_nozzle = None

        # design count slot
        self.count_slot = None
        self.count_nozzle = None


def get_init_volume(chamber: Geometry):
    r1 = chamber.r_inner + chamber.inner_thickness
    r2 = chamber.r_outer
    v1 = pi * (r2 ** 2 - r1 ** 2) * chamber.high
    v2 = 2 * (chamber.angle_slot * pi / 180) * (r1 ** 2 - chamber.r_inner ** 2)
    return v1 + v2


def get_init_volume_chamber(rot: Geometry, st: Geometry):
    v1 = get_init_volume(rot)
    v2 = (rot.angle_nozzle * pi / 180) * (st.r_inner ** 2 - rot.r_outer ** 2) * rot.high_nozzle
    return v1 + v2 * 2


def get_expansion_volume(rot: Geometry, st: Geometry, expand_angle: float):
    r1 = rot.r_outer + rot.outer_thickness
    r2 = st.r_inner
    return 2 * expand_angle * (r2 ** 2 - r1 ** 2) * rot.high_nozzle


def get_working_angle(st: Geometry, val: Geometry):
    from math import asin
    return pi - 2 * asin(val.r_valve / st.r_inner) - (st.angle_slot * pi / 180)


def get_nozzle_area(rot: Geometry):
    return (rot.angle_nozzle * pi) / 180 * rot.r_nozzle * rot.high_nozzle


def get_partition_area(rot: Geometry, st: Geometry):
    return (st.r_inner - rot.r_inner) * rot.high_nozzle
