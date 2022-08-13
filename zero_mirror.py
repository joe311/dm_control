import TLDFMX_wrapper

with TLDFMX_wrapper.DM_Context(0) as dm:
    mirror_pattern = [100, ]*40
    dm.set_segment_voltages(mirror_pattern)
    dm.set_segment_voltage_setpoints(mirror_pattern)
