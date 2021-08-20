"""
#######################################################################################
Universal Song Barn (USB) Manager - Tkinter App (powered by PySimpleGUI)
(c) Stanley Solutions - 2020

By: Joe Stanley
#######################################################################################
"""

FILTER_STRING = "{FFMPEG_EXE} -i {IN_PATH} {FILTER} {OUT_PATH}"

BUILTIN_FILTERS = {
    "Dirty Compand": """ -filter_complex "compand=attacks=0:points=-80/-900|-45/-15|-27/-9|0/-7|20/-7:gain=5" """,
    "Light Compand": """ -filter:a "compand=.3|.3:1|1:-90/-60|-60/-40|-40/-30|-20/-20:6:0:-90:0.2" """,
    "Heavy Compand": """ -filter:a "compand=0|0:1|1:-90/-900|-70/-70|-30/-9|0/-3:6:0:0:0" """,
    "Dynamic Normalization": """ -filter:a "dynaudnorm" """,
}

# Define Function to Format Command
def format_ffmpeg_command(in_path: str, out_path: str, filter: str,
                          ffmpeg_binary: str = "ffmpeg"):
    """Format the FFMPEG Filter Command."""
    def sanitize_input(param_string, wrap=True):
        # Only accept the first portion of any multi-command string
        param_string = param_string.split('&&')[0]
        param_string = param_string.split(';')[0]
        if wrap:
            # Wrap with Quotes
            if not param_string.startswith('"'):
                param_string = '"{}'.format(param_string)
            if not param_string.endswith('"'):
                param_string = '{}"'.format(param_string)
        return param_string

    # Sanitize Each of the Parameters
    in_path = sanitize_input(in_path)
    out_path = sanitize_input(out_path)
    filter = sanitize_input(filter, wrap=False)
    ffmpeg_binary = sanitize_input(ffmpeg_binary)

    # Format the Full Command String
    return FILTER_STRING.format(
        FFMPEG_BIN = ffmpeg_binary,
        IN_PATH = in_path,
        FILTER = filter,
        OUT_PATH = out_path,
    )

