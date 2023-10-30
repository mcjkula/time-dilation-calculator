import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

class Configuration:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = "Arial"
    matplotlib.rcParams["text.latex.preamble"] = r"\usepackage{cmbright}"
    COLOR_LINE = "#111111"
    COLOR_TEXT = "#111111"

def visualize(v):
    fig, ax = plt.subplots(figsize=(17.5, 7))
    ax.set_aspect("equal", "box")

    v = (v / 299792.458) * 10
    percentage = v / 0.1

    c_start, c_end = (0, 0), (0, -10)
    v_start, v_end = c_start, (v, 0)

    d_start = (0, 0)
    d_side = np.sqrt(abs(c_end[1]) ** 2 - v_end[0] ** 2)
    d_end = (v_end[0], -d_side)
    dd_start, dd_end = (v_end[0], 0), (v_end[0], -d_side)

    dt_start, dt_end = (-0.2, d_end[1]), (v_end[0] + 0.2, d_end[1]) if percentage != 100 else (v_start[1], d_end[1])

    t_start, t_end = (-0.2, c_end[1]), (v_end[0] + 0.2, c_end[1])

    td_start, td_end = (v_end[0], d_end[1]), (v_end[0], c_end[1])

    ax.fill_between(
        [v_start[0], v_end[0]], [dt_start[1], dt_end[1]], [t_start[1], t_end[1]], color="lightgray", alpha=0.5
    )
    # ax.plot([c_start[0], c_end[0]], [c_start[1], c_end[1]], color=color_line, lw=2, label="c")
    adjusted_c_end = (c_end[0], c_end[1] - 0.05)
    ax.add_patch(
        FancyArrowPatch(
            c_start,
            adjusted_c_end,
            mutation_scale=20,
            lw=2,
            arrowstyle="-|>",
            color=Configuration.COLOR_LINE,
            label="c",
        )
    )
    # Backup: ax.plot([v_start[0], v_end[0]], [v_start[1], v_end[1]], color=Configuration.COLOR_LINE, lw=2, label="v")
    # The endpoint of the Arrow needs to be adjusted for some reason as its shorter with an arrow than without
    adjusted_v_start = (v_start[0] - 0.05, v_start[1])
    if v_end[0] > 0:
        adjusted_v_end = (v_end[0] + 0.05, v_end[1])
        ax.add_patch(
            FancyArrowPatch(
                adjusted_v_start,
                adjusted_v_end,
                mutation_scale=20,
                lw=2,
                arrowstyle="-|>",
                color=Configuration.COLOR_LINE,
                label="v",
            )
        )
    else:
        ax.add_patch(
            FancyArrowPatch(
                v_start, v_end, mutation_scale=20, lw=2, arrowstyle="-|>", color=Configuration.COLOR_LINE, label="v"
            )
        )
    # ax.plot([d_start[0], d_end[0]], [d_start[1], d_end[1]], color=Configuration.COLOR_LINE, lw=1.5, label="d")
    ax.add_patch(
        FancyArrowPatch(
            d_start,
            d_end,
            mutation_scale=20,
            linestyle="dotted",
            lw=2,
            arrowstyle="-",
            color=Configuration.COLOR_LINE,
            label="d1",
        )
    )
    ax.add_patch(
        FancyArrowPatch(
            d_start,
            d_end,
            mutation_scale=20,
            linestyle="solid",
            lw=0,
            arrowstyle="-|>",
            color=Configuration.COLOR_LINE,
            label="d2",
        )
    )
    ax.plot([dd_start[0], dd_end[0]], [dd_start[1], dd_end[1]], color=Configuration.COLOR_LINE, lw=1.5, label="dd")
    ax.plot([dt_start[0], dt_end[0]], [dt_start[1], dt_end[1]], color=Configuration.COLOR_LINE, lw=2, label="dt")
    if v_end[0] >= (0.33 * abs(c_end[1])):
        ax.add_patch(
            FancyArrowPatch(
                td_start,
                td_end,
                mutation_scale=20,
                lw=2,
                arrowstyle="-|>",
                color=Configuration.COLOR_LINE,
                label="td1",
            )
        )
        ax.add_patch(
            FancyArrowPatch(
                td_end,
                td_start,
                mutation_scale=20,
                lw=2,
                arrowstyle="-|>",
                color=Configuration.COLOR_LINE,
                label="td2",
            )
        )
    ax.plot([t_start[0], t_end[0]], [t_start[1], t_end[1]], color=Configuration.COLOR_LINE, lw=2, label="t")
    ax.text(c_start[0] - 0.5, (c_start[1] + c_end[1]) / 2, "c", color=Configuration.COLOR_TEXT, fontsize=14)
    ax.text(
        (v_start[0] + v_end[0]) / 2,
        (v_start[1] + v_end[1]) / 2 + 0.5,
        f"v ({percentage:.5f}% of c)",
        ha="center",
        va="center",
        color=Configuration.COLOR_TEXT,
        fontsize=14,
    )
    ax.text(
        (t_start[0] + t_end[0]) / 2,
        (t_start[1] + t_end[1]) / 2 - 0.5,
        f"$\gamma$ = {abs(c_end[1]) / d_side:.10f}",
        ha="center",
        va="center",
        color=Configuration.COLOR_TEXT,
        fontsize=14,
    )
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()

visualize(149896.229)
