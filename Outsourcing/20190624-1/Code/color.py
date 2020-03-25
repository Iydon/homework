# -*- encode: utf-8 -*-
def color(string:str, fore="紫", back="黑", disp="默认"):
    """Coloring text.

    Parameters
    ==========
        string: String, text to be colored.
        fore:   String, foreground color.
        back:   String, background color.
        disp:   String, display effect.

    Return
    ======
        Text with color information.

    Examples
    ========
    >>> _color("Hello world", "蓝", "黑", "默认")
    """
    colormap = {"黑":["30","40"],
                "红":["31","41"],
                "绿":["32","42"],
                "黄":["33","43"],
                "蓝":["34","44"],
                "紫":["35","45"],
                "青":["36","46"],
                "白":["37","47"],}
    disp_map = {"默认":"0",
                "高亮":"1",
                "下划":"4",
                "闪烁":"5",
                "反白":"7",
                "隐藏":"8",}
    return "\033[%s;%s;%sm%s\033[0m"% \
                (disp_map[disp], colormap[fore][0], \
                 colormap[back][-1], string)
