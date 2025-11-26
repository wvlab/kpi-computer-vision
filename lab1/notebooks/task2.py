import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import random
    from lab1 import transform, creation

    return creation, mo, plt, random, transform


@app.cell
def _(mo, play):
    timer = (
        mo.ui.refresh(label="Tick", default_interval="1s")
        if play.value
        else None
    )
    timer
    return (timer,)


@app.cell
def _(mo):
    get_frame, set_frame = mo.state(0)
    get_props, set_props = mo.state(
        {"idx": -1, "pos": (0, 0, 0), "color": "#E74C3C"}
    )
    return get_frame, get_props, set_frame, set_props


@app.cell
def _(get_frame, set_frame, speed, timer):
    # Frame Update Logic
    if timer is not None:
        set_frame(lambda f: f + speed.value)

    current_frame = get_frame()
    return (current_frame,)


@app.cell
def _(current_frame, cycle_len, get_props, random, set_props, spawn_radius):
    c_len = cycle_len.value
    new_cycle_idx = current_frame // c_len

    current_props = get_props()
    active_props = current_props

    if new_cycle_idx > current_props["idx"]:
        limit = spawn_radius.value
        new_pos = (
            random.uniform(-limit, limit),
            random.uniform(-limit, limit),
            random.uniform(-limit, limit),
        )
        new_color = random.choice(
            ["#E74C3C", "#3498DB", "#2ECC71", "#F1C40F", "#9B59B6", "#1ABC9C"]
        )

        new_props = {"idx": new_cycle_idx, "pos": new_pos, "color": new_color}

        set_props(new_props)
        active_props = new_props
    return active_props, c_len, new_cycle_idx


@app.cell
def _(
    active_props,
    alpha,
    base_size,
    beta,
    c_len,
    creation,
    current_frame,
    pyr_height,
    spin_speed,
    transform,
):
    pos_x, pos_y, pos_z = active_props["pos"]
    color = active_props["color"]

    progress = (current_frame % c_len) / c_len
    if progress < 0.2:
        opacity = progress / 0.2
    elif progress > 0.8:
        opacity = (1.0 - progress) / 0.2
    else:
        opacity = 1.0

    points, edges = creation.pyramid(base_size.value, pyr_height.value)

    verts_projected = transform.apply(
        points,
        transform.compose(
            transform.axonometric_projection(alpha.value, beta.value),
            transform.translation_3d(pos_x, pos_y, pos_z),
            transform.rotation_3d_z(current_frame * spin_speed.value),
        ),
    )
    return color, edges, opacity, pos_x, pos_y, pos_z, verts_projected


@app.cell
def _(
    color,
    edges,
    new_cycle_idx,
    opacity,
    plt,
    pos_x,
    pos_y,
    pos_z,
    spawn_radius,
    verts_projected,
):
    fig, ax = plt.subplots(figsize=(6, 6))

    sclimit = spawn_radius.value + 5
    ax.set_xlim(-sclimit, sclimit)
    ax.set_ylim(-sclimit, sclimit)
    ax.set_aspect("equal")
    ax.axis("off")

    for i, j in edges:
        p1 = verts_projected[:, i]
        p2 = verts_projected[:, j]
        ax.plot(
            [p1[0], p2[0]],
            [p1[1], p2[1]],
            color=color,
            alpha=opacity,
            linewidth=2.5,
            solid_capstyle="round",
        )

    ax.set_title(
        f"Cycle: {new_cycle_idx} | Pos: ({pos_x:.1f}, {pos_y:.1f}, {pos_z:.1f})",
        color="gray",
        fontsize=10,
    )

    plt.close(fig)
    fig
    return


@app.cell
def _(mo):
    play = mo.ui.switch(label="▶ Play", value=False)
    speed = mo.ui.slider(1, 10, value=2, label="Speed")

    base_size = mo.ui.slider(1.0, 6.0, value=3.0, label="Base Size")
    pyr_height = mo.ui.slider(1.0, 8.0, value=5.0, label="Height")

    cycle_len = mo.ui.slider(50, 200, value=100, label="Cycle Length (frames)")
    spin_speed = mo.ui.slider(1.0, 10.0, value=4.0, label="Spin Speed")

    alpha = mo.ui.slider(0, 90, value=45, label="Alpha (X-Rot)")
    beta = mo.ui.slider(0, 90, value=35, label="Beta (Y-Rot)")

    spawn_radius = mo.ui.slider(2.0, 15.0, value=8.0, label="Spawn Radius")

    settings = mo.accordion(
        {
            "Geometry": mo.vstack([base_size, pyr_height]),
            "Dynamics": mo.vstack([cycle_len, spin_speed]),
            "Projection": mo.vstack([alpha, beta]),
            "Randomness": mo.vstack([spawn_radius]),
        }
    )

    mo.vstack([mo.hstack([play, speed], justify="center"), settings])
    return (
        alpha,
        base_size,
        beta,
        cycle_len,
        play,
        pyr_height,
        spawn_radius,
        speed,
        spin_speed,
    )


if __name__ == "__main__":
    app.run()
