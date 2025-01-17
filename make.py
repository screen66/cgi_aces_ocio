#!/usr/bin/env python
"""OCIO configuration make script"""
from __future__ import print_function
import PyOpenColorIO as OCIO

__version__ = "0.3.4"


def make_config(config_filename="config.ocio", scene_linear_role="ACES - ACEScg"):
    """Generate OCIO config"""
    config = OCIO.Config()
    config.setSearchPath(":".join(["luts", "matrices"]))
    config.addColorSpace(aces_2065_1_colorspace())
    config.addColorSpace(acescg_colorspace())
    config.addColorSpace(acesproxy_colorspace())
    config.addColorSpace(acescc_colorspace())
    config.addColorSpace(acescct_colorspace())
    config.addColorSpace(linear_srgb_colorspace())
    config.addColorSpace(srgb_colorspace())
    config.addColorSpace(rec709_colorspace())
    config.addColorSpace(raw_colorspace())
    config.addColorSpace(aces_rec709_output())
    config.addColorSpace(aces_srgb_output())

    display_spaces = [["ACES Rec. 709", "Output - ACES Rec. 709"],
                      ["ACES sRGB", "Output - ACES sRGB"],
                      ["Raw", "Utility - Raw"]]
    for name, colorspace in display_spaces:
        config.addDisplay("default", name, colorspace)

    config.setActiveViews(','.join(["ACES Rec. 709",
                                    "ACES sRGB",
                                    "Raw"]))
    config.setActiveDisplays(','.join(["default"]))

    config.setRole(OCIO.Constants.ROLE_SCENE_LINEAR, scene_linear_role)
    config.setRole(OCIO.Constants.ROLE_REFERENCE, "ACES - ACES2065-1")
    config.setRole(OCIO.Constants.ROLE_COLOR_TIMING, "ACES - ACEScct")
    config.setRole(OCIO.Constants.ROLE_COMPOSITING_LOG, "ACES - ACEScct")
    config.setRole(OCIO.Constants.ROLE_DATA, "Utility - Raw")
    config.setRole(OCIO.Constants.ROLE_DEFAULT, "Utility - Raw")
    config.setRole(OCIO.Constants.ROLE_COLOR_PICKING, "Utility - Raw")
    config.setRole(OCIO.Constants.ROLE_MATTE_PAINT, "Utility - Raw")
    config.setRole(OCIO.Constants.ROLE_TEXTURE_PAINT, "Utility - Raw")
    config.setRole("rendering", scene_linear_role)
    config.setRole("compositing_linear", scene_linear_role)

    config.sanityCheck()

    with open(config_filename, "w") as fhandle:
        fhandle.write(config.serialize())
    print("Wrote {0} successfully".format(config_filename))
    return


def aces_2065_1_colorspace():
    """ACES 2065-1"""
    col_space = OCIO.ColorSpace(name="ACES - ACES2065-1", family="ACES")
    col_space.setDescription("Scene-linear, high dynamic range, AP0 primaries")
    col_space.setBitDepth(OCIO.Constants.BIT_DEPTH_F32)
    col_space.setAllocationVars([-8.0, 5.0, 0.00390625])
    col_space.setAllocation(OCIO.Constants.ALLOCATION_LG2)
    return col_space


def acescg_colorspace():
    """ACEScg"""
    col_space = OCIO.ColorSpace(name="ACES - ACEScg", family="ACES")
    col_space.setDescription("Scene-linear, high dynamic range, AP1 primaries")
    col_space.setBitDepth(OCIO.Constants.BIT_DEPTH_F32)
    col_space.setAllocationVars([-8.0, 5.0, 0.00390625])
    col_space.setAllocation(OCIO.Constants.ALLOCATION_LG2)
    group_xform = OCIO.GroupTransform()
    group_xform.push_back(OCIO.FileTransform("AP1_to_AP0.spimtx",
                                             direction=OCIO.Constants.TRANSFORM_DIR_FORWARD))
    col_space.setTransform(group_xform,
                           OCIO.Constants.COLORSPACE_DIR_TO_REFERENCE)
    return col_space


def acesproxy_colorspace():
    """ACESproxy"""
    col_space = OCIO.ColorSpace(name="ACES - ACESproxy", family="ACES")
    col_space.setDescription("ACESproxy colorspace, gamma and primaries")
    col_space.setBitDepth(OCIO.Constants.BIT_DEPTH_F32)
    col_space.setAllocationVars([0, 1])
    col_space.setAllocation(OCIO.Constants.ALLOCATION_UNIFORM)
    group_xform = OCIO.GroupTransform()
    group_xform.push_back(OCIO.FileTransform("ACESproxy_to_linear.spi1d",
                                             interpolation=OCIO.Constants.INTERP_LINEAR,
                                             direction=OCIO.Constants.TRANSFORM_DIR_FORWARD))
    group_xform.push_back(OCIO.FileTransform("AP1_to_AP0.spimtx",
                                             direction=OCIO.Constants.TRANSFORM_DIR_FORWARD))
    col_space.setTransform(group_xform,
                           OCIO.Constants.COLORSPACE_DIR_TO_REFERENCE)
    return col_space


def acescc_colorspace():
    """ACEScc"""
    col_space = OCIO.ColorSpace(name="ACES - ACEScc", family="ACES")
    col_space.setDescription("ACEScc colorspace, gamma and primaries")
    col_space.setBitDepth(OCIO.Constants.BIT_DEPTH_F32)
    col_space.setAllocationVars([-0.3584, 1.468])
    col_space.setAllocation(OCIO.Constants.ALLOCATION_UNIFORM)
    group_xform = OCIO.GroupTransform()
    group_xform.push_back(OCIO.FileTransform("ACEScc_to_linear.spi1d",
                                             interpolation=OCIO.Constants.INTERP_LINEAR,
                                             direction=OCIO.Constants.TRANSFORM_DIR_FORWARD))
    group_xform.push_back(OCIO.FileTransform("AP1_to_AP0.spimtx",
                                             direction=OCIO.Constants.TRANSFORM_DIR_FORWARD))
    col_space.setTransform(group_xform,
                           OCIO.Constants.COLORSPACE_DIR_TO_REFERENCE)
    return col_space


def acescct_colorspace():
    """ACEScct"""
    col_space = OCIO.ColorSpace(name="ACES - ACEScct", family="ACES")
    col_space.setDescription("ACEScct colorspace, gamma and primaries")
    col_space.setBitDepth(OCIO.Constants.BIT_DEPTH_F32)
    col_space.setAllocationVars([-0.249136, 1.468])
    col_space.setAllocation(OCIO.Constants.ALLOCATION_UNIFORM)
    group_xform = OCIO.GroupTransform()
    group_xform.push_back(OCIO.FileTransform("ACEScct_to_linear.spi1d",
                                             interpolation=OCIO.Constants.INTERP_LINEAR,
                                             direction=OCIO.Constants.TRANSFORM_DIR_FORWARD))
    group_xform.push_back(OCIO.FileTransform("AP1_to_AP0.spimtx",
                                             direction=OCIO.Constants.TRANSFORM_DIR_FORWARD))
    col_space.setTransform(group_xform,
                           OCIO.Constants.COLORSPACE_DIR_TO_REFERENCE)
    return col_space


def linear_srgb_colorspace():
    """Linear sRGB"""
    col_space = OCIO.ColorSpace(name="Input - Linear (sRGB)", family="Input")
    col_space.setDescription(
        "Scene-linear, high dynamic range, sRGB/Rec.709 primaries")
    col_space.setBitDepth(OCIO.Constants.BIT_DEPTH_F32)
    col_space.setAllocationVars([-8.0, 5.0, 0.00390625])
    col_space.setAllocation(OCIO.Constants.ALLOCATION_LG2)
    group_xform = OCIO.GroupTransform()
    group_xform.push_back(OCIO.FileTransform("sRGB_to_AP0.spimtx",
                                             direction=OCIO.Constants.TRANSFORM_DIR_FORWARD))
    col_space.setTransform(group_xform,
                           OCIO.Constants.COLORSPACE_DIR_TO_REFERENCE)
    return col_space


def srgb_colorspace():
    """sRGB"""
    col_space = OCIO.ColorSpace(name="Input - sRGB", family="Input")
    col_space.setDescription("sRGB colorspace, gamma and primaries")
    col_space.setBitDepth(OCIO.Constants.BIT_DEPTH_F32)
    col_space.setAllocationVars([0, 1])
    col_space.setAllocation(OCIO.Constants.ALLOCATION_UNIFORM)
    group_xform = OCIO.GroupTransform()
    group_xform.push_back(OCIO.FileTransform("sRGB_to_linear.spi1d",
                                             interpolation=OCIO.Constants.INTERP_LINEAR,
                                             direction=OCIO.Constants.TRANSFORM_DIR_FORWARD))
    group_xform.push_back(OCIO.FileTransform("sRGB_to_AP0.spimtx",
                                             direction=OCIO.Constants.TRANSFORM_DIR_FORWARD))
    col_space.setTransform(group_xform,
                           OCIO.Constants.COLORSPACE_DIR_TO_REFERENCE)
    return col_space


def rec709_colorspace():
    """Rec. 709"""
    col_space = OCIO.ColorSpace(name="Input - Rec. 709", family="Input")
    col_space.setDescription(
        "Rec. 709 colorspace, Rec. 1886 gamma, Rec. 709 primaries")
    col_space.setBitDepth(OCIO.Constants.BIT_DEPTH_F32)
    col_space.setAllocationVars([0, 1])
    col_space.setAllocation(OCIO.Constants.ALLOCATION_UNIFORM)
    group_xform = OCIO.GroupTransform()
    group_xform.push_back(OCIO.FileTransform("rec1886_to_linear.spi1d",
                                             interpolation=OCIO.Constants.INTERP_LINEAR,
                                             direction=OCIO.Constants.TRANSFORM_DIR_FORWARD))
    group_xform.push_back(OCIO.FileTransform("sRGB_to_AP0.spimtx",
                                             direction=OCIO.Constants.TRANSFORM_DIR_FORWARD))
    col_space.setTransform(group_xform,
                           OCIO.Constants.COLORSPACE_DIR_TO_REFERENCE)
    return col_space


def raw_colorspace():
    """Raw"""
    col_space = OCIO.ColorSpace(name="Utility - Raw", family="Utility")
    col_space.setDescription("Raw data")
    col_space.setBitDepth(OCIO.Constants.BIT_DEPTH_F32)
    col_space.setIsData(True)
    return col_space


def aces_srgb_output():
    """ACES sRGB output"""
    col_space = OCIO.ColorSpace(name="Output - ACES sRGB", family="Output")
    col_space.setDescription("ACES sRGB output transform")
    col_space.setBitDepth(OCIO.Constants.BIT_DEPTH_F32)
    group_xform = OCIO.GroupTransform()
    group_xform.push_back(OCIO.FileTransform("Log2_48_nits_Shaper_to_linear.spi1d",
                                             interpolation=OCIO.Constants.INTERP_LINEAR,
                                             direction=OCIO.Constants.TRANSFORM_DIR_INVERSE))
    group_xform.push_back(OCIO.FileTransform("Log2_48_nits_Shaper.RRT.sRGB.spi3d",
                                             interpolation=OCIO.Constants.INTERP_TETRAHEDRAL))
    col_space.setTransform(group_xform,
                           OCIO.Constants.COLORSPACE_DIR_FROM_REFERENCE)

    group_xform = OCIO.GroupTransform()
    group_xform.push_back(OCIO.FileTransform("InvRRT.sRGB.Log2_48_nits_Shaper.spi3d",
                                             interpolation=OCIO.Constants.INTERP_TETRAHEDRAL))
    group_xform.push_back(OCIO.FileTransform("Log2_48_nits_Shaper_to_linear.spi1d",
                                             interpolation=OCIO.Constants.INTERP_LINEAR,
                                             direction=OCIO.Constants.TRANSFORM_DIR_FORWARD))
    col_space.setTransform(group_xform,
                           OCIO.Constants.COLORSPACE_DIR_TO_REFERENCE)
    return col_space


def aces_rec709_output():
    """ACES Rec. 709 output"""
    col_space = OCIO.ColorSpace(name="Output - ACES Rec. 709", family="Output")
    col_space.setDescription("ACES Rec. 709 output transform")
    col_space.setBitDepth(OCIO.Constants.BIT_DEPTH_F32)
    group_xform = OCIO.GroupTransform()
    group_xform.push_back(OCIO.FileTransform("Log2_48_nits_Shaper_to_linear.spi1d",
                                             interpolation=OCIO.Constants.INTERP_LINEAR,
                                             direction=OCIO.Constants.TRANSFORM_DIR_INVERSE))
    group_xform.push_back(OCIO.FileTransform("Log2_48_nits_Shaper.RRT.Rec.709.spi3d",
                                             interpolation=OCIO.Constants.INTERP_TETRAHEDRAL))
    col_space.setTransform(group_xform,
                           OCIO.Constants.COLORSPACE_DIR_FROM_REFERENCE)

    group_xform = OCIO.GroupTransform()
    group_xform.push_back(OCIO.FileTransform("InvRRT.Rec.709.Log2_48_nits_Shaper.spi3d",
                                             interpolation=OCIO.Constants.INTERP_TETRAHEDRAL))
    group_xform.push_back(OCIO.FileTransform("Log2_48_nits_Shaper_to_linear.spi1d",
                                             interpolation=OCIO.Constants.INTERP_LINEAR,
                                             direction=OCIO.Constants.TRANSFORM_DIR_FORWARD))
    col_space.setTransform(group_xform,
                           OCIO.Constants.COLORSPACE_DIR_TO_REFERENCE)
    return col_space


if __name__ == "__main__":
    make_config(config_filename="config_acescg.ocio",
                scene_linear_role="ACES - ACEScg")
    make_config(config_filename="config_linear_srgb.ocio",
                scene_linear_role="Input - Linear (sRGB)")
