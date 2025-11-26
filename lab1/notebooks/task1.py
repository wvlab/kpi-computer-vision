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

    return creation, mo, np, plt, random, transform


@app.cell
def _(mo):
    mo.md("""
    Варіант 14

    Реалізувати операції: обертання – переміщення – масштабування. 3.
    операцію реалізувати циклічно, траєкторію зміни положення цієї операції
    скрити.

    Обрати самостійно: бібліотеку, розмір графічного вікна, розмір фігури,
    параметри реалізації операцій, кольорову гамму усіх графічних об’єктів.
    Всі операції перетворень мають здійснюватись у межах графічного вікна.

    Фігура: Шестикутник
    """)
    return


@app.cell
def _(mo, play):
    timer = (
        mo.ui.refresh(label="Tick", default_interval="100ms")
        if play.value
        else None
    )
    timer
    return (timer,)


@app.cell
def _(mo):
    get_t, set_t = mo.state(0.0)
    get_color, set_color = mo.state("#884EA0")
    return get_color, get_t, set_color, set_t


@app.cell
def _(get_color, get_t, rand_color, random, set_color, set_t, speed_t, timer):
    if timer is not None:
        prev_t = get_t()
        new_t = prev_t + speed_t.value

        if (new_t % 360) < (prev_t % 360) and rand_color.value:
            new_c = random.choice(
                [
                    "#E74C3C",
                    "#8E44AD",
                    "#3498DB",
                    "#16A085",
                    "#F39C12",
                    "#2C3E50",
                ]
            )
            set_color(new_c)

        set_t(new_t % 360)

    current_t = get_t()
    current_color = get_color()
    return current_color, current_t


@app.cell
def _(
    creation,
    current_t,
    hex_radius,
    jitter,
    np,
    orbit_radius,
    random,
    rot_mult,
    scale_mult,
    transform,
):
    r_hex = hex_radius.value
    r_orbit = orbit_radius.value

    angle_rot = current_t * rot_mult.value

    tx = r_orbit * np.cos(np.radians(current_t))
    ty = r_orbit * np.sin(np.radians(current_t))

    if jitter.value:
        tx += random.uniform(-0.5, 0.5)
        ty += random.uniform(-0.5, 0.5)

    scale = 1.0 + 0.5 * np.sin(np.radians(current_t * scale_mult.value))

    # v' = T_orbit @ R_spin @ S_pulse @ v
    # 1. Scale object locally
    # 2. Rotate object locally (Spin)
    # 3. Translate object to orbit position
    tr = transform.compose(
        transform.translation_2d(tx, ty),
        transform.rotation_2d(angle_rot),
        transform.scaling_2d(scale, scale),
    )

    shape = transform.apply(creation.hexagon(r_hex), tr)

    return scale, shape


@app.cell
def _(current_color, current_t, plt, scale, shape):
    fig, ax = plt.subplots(figsize=(6, 6))
    window_limit = 12

    ax.set_xlim(-window_limit, window_limit)
    ax.set_ylim(-window_limit, window_limit)
    ax.set_aspect("equal")
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)

    ax.plot(
        shape[0],
        shape[1],
        color=current_color,
        linewidth=3,
        marker="o",
        markersize=4,
    )
    ax.fill(shape[0], shape[1], color=current_color, alpha=0.3)

    ax.set_title(f"t={current_t:.0f}° | Scale={scale:.2f}")

    plt.close(fig)
    fig
    return


@app.cell
def _(mo):
    play = mo.ui.switch(label="▶ Play", value=False)
    speed_t = mo.ui.slider(1, 10, value=2, label="Time Step")
    hex_radius = mo.ui.slider(0.5, 5.0, value=2.0, label="Hex Radius")
    orbit_radius = mo.ui.slider(0.0, 10.0, value=6.0, label="Orbit Radius")

    rot_mult = mo.ui.slider(0.0, 10.0, value=2.0, label="Spin Speed")
    scale_mult = mo.ui.slider(0.0, 10.0, value=4.0, label="Pulse Speed")

    rand_color = mo.ui.switch(label="Random Color Cycle", value=True)
    jitter = mo.ui.switch(label="Add Noise (Jitter)", value=False)

    settings = mo.accordion(
        {
            "Geometry & Motion": mo.vstack(
                [hex_radius, orbit_radius, rot_mult, scale_mult]
            ),
            "Randomness": mo.vstack([rand_color, jitter]),
        }
    )

    mo.vstack([mo.hstack([play, speed_t], justify="center"), settings])
    return (
        hex_radius,
        jitter,
        orbit_radius,
        play,
        rand_color,
        rot_mult,
        scale_mult,
        speed_t,
    )


if __name__ == "__main__":
    app.run()
