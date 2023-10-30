import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch
import os
import imageio
from PIL import Image


class Configuration:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = "Arial"
    matplotlib.rcParams["text.latex.preamble"] = r"\usepackage{cmbright}"
    COLOR_LINE = "#111111"
    COLOR_TEXT = "#111111"


def plot_v_length(v):
    fig, ax = plt.subplots(figsize=(17.5, 7))
    ax.set_aspect("equal", "box")

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

    return fig, ax


def lerp(a, b, t):
    return a + t * (b - a)


frame_dir = "./frames"
os.makedirs(frame_dir, exist_ok=True)

total_frames = 30 * 2.5
values = []

i = 0
max_i = total_frames - 1

while i < total_frames:
    val = 10 * ((i + 1) / total_frames) ** 0.5
    if val > 10:
        val = 10
    values.append(val)

    if val == 10:
        break

    t = i / max_i
    step_size = lerp(1, 0.1, t**2)

    i += step_size

frame_paths = []
for idx, value in enumerate(values):
    fig, ax = plot_v_length(value)
    frame_path = os.path.join(frame_dir, f"frame_{idx:04}.png")
    fig.savefig(frame_path, dpi=300, bbox_inches="tight", pad_inches=0)
    frame_paths.append(frame_path)
    plt.close(fig)

last_image = Image.open(frame_paths[-1])
max_width, max_height = last_image.size

padding_factor = 1.5
padded_width = int(max_width * padding_factor)
padded_height = int(max_height * padding_factor)

centered_frames = []

for frame_path in frame_paths:
    image = Image.open(frame_path)
    width, height = image.size

    new_frame = Image.new("RGB", (padded_width, padded_height), "white")

    x_offset = (padded_width - width) // 2
    y_offset = (padded_height - height) // 2

    new_frame.paste(image, (x_offset, y_offset))
    centered_frames.append(new_frame)

gif_path = "output_centered.gif"
with imageio.get_writer(gif_path, mode="I", duration=1 / 30) as writer:
    for frame in centered_frames:
        writer.append_data(np.array(frame))

print(f"GIF saved at {gif_path}")
