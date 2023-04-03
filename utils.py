# -*- coding: utf-8 -*-

import os, sys
import numpy as np
import itertools, struct
import xml.etree.ElementTree as ET


def numpy2tiff(image, path):
    """
    Save a numpy array as a TIFF image file.

    Parameters:
    image (ndarray): The input image as a numpy array.
    path (str): The output file path.

    Returns:
    None
    """
    def tiff_tag(tag_code, datatype, values):
        datatype_code = np.dtype(datatype).num
        number = 1 if isinstance(values, int) else len(values)
        tag_bytes = bytearray(12 + number * np.dtype(datatype).itemsize)
        struct.pack_into('<H', tag_bytes, 0, tag_code)
        struct.pack_into('<H', tag_bytes, 2, datatype_code)
        struct.pack_into('<L', tag_bytes, 4, number)
        if number == 1:
            struct.pack_into(datatype, tag_bytes, 8, values)
        else:
            struct.pack_into('<' + (datatype[-1:] * number), tag_bytes, 8, *values)
        return tag_bytes

    image_bytes = image.shape[0] * image.shape[1] * image.shape[2]
    with open(path, 'wb+') as f:
        image.reshape((image_bytes,))
        f.write(b'II')
        f.write(struct.pack('<H', 43))  # Version number
        f.write(struct.pack('<H', 8))  # Bytesize of offsets
        f.write(struct.pack('<H', 0))  # always zero
        f.write(struct.pack('<Q', 16 + image_bytes))  # Offset to IFD
        for offset in range(0, image_bytes, 2 ** 20):
            f.write(image[offset:offset + 2 ** 20].tobytes())
        f.write(struct.pack('<Q', 8))  # Number of tags in IFD
        f.write(tiff_tag(256, '<L', image.shape[1]))  # ImageWidth tag
        f.write(tiff_tag(257, '<L', image.shape[0]))  # ImageLength tag
        f.write(tiff_tag(258, '<H', (8, 8, 8)))  # BitsPerSample tag
        f.write(tiff_tag(262, '<H', 2))  # PhotometricInterpretation tag
        f.write(tiff_tag(273, '<H', 16))  # StripOffsets tag
        f.write(tiff_tag(277, '<H', 3))  # SamplesPerPixel
        f.write(tiff_tag(278, '<Q', image_bytes // 8192))  # RowsPerStrip
        f.write(tiff_tag(279, '<Q', image_bytes))  # StripByteCounts
        f.write(struct.pack('<Q', 0))  # Offset to next IFD
