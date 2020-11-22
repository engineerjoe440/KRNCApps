# Standard Audio Filter for Cars
# Written by Joe Stanley
#
# API INTERFACE:
# The `main()` function defined here shall be the standard interface
# which the KRNC Universal Song Barn Manager will expect and interpret
# for adjusting audio as necessary.

# Any required imports necessary to support this operation
import os
import subprocess

def main(source_file, destination_file, progress_ind=None):
    """
    *standard audio filter*

    Parameters
    ----------
    source_file:        str
                        Fully-qualified file path to the source
                        file which should be modified and stored
                        as the `destination_file` by this filter.
    destination_file:   str
                        Fully-qualified file path to the destination
                        file which will be generated from this
                        filtering operation. Generated from the
                        `source_file`.
    progress_ind:       list of int, optional
                        A mutable list containing a single integer
                        which can inform the calling system what
                        percentage complete the filtering operation
                        is. Must be an integer between 0 and 100.
    
    Returns
    -------
    None
    """
    pass # this operation still has not been fully defined.