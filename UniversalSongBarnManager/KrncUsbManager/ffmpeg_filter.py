

FILTER_STRING = "{FFMPEG_EXE} -i {IN_PATH} {FILTER} {OUT_PATH}"

# Define Function to Format Command
def format_ffmpeg_command(in_path: str, out_path: str, filter: str,
                          ffmpeg_binary: str = "ffmpeg"):
    """Format the FFMPEG Filter Command."""
    def sanitize_input(param_string):
        # Only accept the first portion of any multi-command string
        param_string = param_string.split('&&')[0]
        param_string = param_string.split(';')[0]
        # Wrap with Quotes
        if not param_string.startswith('"'):
            param_string = '"{}'.format(param_string)
        if not param_string.endswith('"'):
            param_string = '{}"'.format(param_string)
        return param_string

    # Sanitize Each of the Parameters
    in_path = sanitize_input(in_path)
    out_path = sanitize_input(out_path)
    filter = sanitize_input(filter)
    ffmpeg_binary = sanitize_input(ffmpeg_binary)

    # Format the Full Command String
    return FILTER_STRING.format(
        FFMPEG_BIN = ffmpeg_binary,
        IN_PATH = in_path,
        FILTER = filter,
        OUT_PATH = out_path,
    )

