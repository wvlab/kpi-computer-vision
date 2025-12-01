import marimo

__generated_with = "0.18.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    from lab2 import vision

    return cv2, mo, plt, vision


@app.cell
def _():
    from enum import StrEnum

    class ImageSource(StrEnum):
        bing = "assets/kpi_bing.png"
        arcgis = "assets/kpi_arcgis.png"

    return (ImageSource,)


@app.cell
def _(ImageSource, mo):
    image_selector = mo.ui.dropdown(
        options={
            "Map (ArcGIS)": ImageSource.arcgis,
            "Satellite (Bing)": ImageSource.bing,
        },
        value="Map (ArcGIS)",
        label="Select Source Image",
    )

    image_selector
    return (image_selector,)


@app.cell
def _(ImageSource, image_selector):
    image_source = image_selector.value
    if image_source == ImageSource.bing:
        defaults = {
            "h_min": 42,
            "h_max": 90,
            "s_min": 0,
            "s_max": 115,
            "v_min": 40,
            "v_max": 255,
            "blur": 7,
            "morph_op": "close",
            "morph_k": 7,
            "morph_iter": 3,
            "area_min": 1000,
            "area_max": 80000,
        }
    else:
        defaults = {
            "h_min": 5,
            "h_max": 50,
            "s_min": 0,
            "s_max": 60,
            "v_min": 200,
            "v_max": 252,
            "blur": 3,
            "morph_op": "close",
            "morph_k": 5,
            "morph_iter": 2,
            "area_min": 250,
            "area_max": 20000,
        }
    return defaults, image_source


@app.cell
def _(defaults, mo):
    blur_input = mo.ui.number(
        start=1,
        stop=31,
        step=2,
        value=defaults["blur"],
        label="Blur Kernel (Odd)",
    )

    h_min = mo.ui.number(
        start=0, stop=179, value=defaults["h_min"], label="H Min"
    )
    h_max = mo.ui.number(
        start=0, stop=179, value=defaults["h_max"], label="H Max"
    )

    s_min = mo.ui.number(
        start=0, stop=255, value=defaults["s_min"], label="S Min"
    )
    s_max = mo.ui.number(
        start=0, stop=255, value=defaults["s_max"], label="S Max"
    )
    v_min = mo.ui.number(
        start=0, stop=255, value=defaults["v_min"], label="V Min"
    )
    v_max = mo.ui.number(
        start=0, stop=255, value=defaults["v_max"], label="V Max"
    )

    morph_type = mo.ui.dropdown(
        {"close": "Close (Fill Holes/Text)", "open": "Open (Remove Noise)"},
        value=defaults["morph_op"],
        label="Operation",
    )
    morph_k = mo.ui.number(
        start=1, stop=31, step=1, value=defaults["morph_k"], label="Kernel Size"
    )
    morph_iter = mo.ui.number(
        start=0, stop=10, value=defaults["morph_iter"], label="Iterations"
    )

    area_min = mo.ui.number(
        start=0,
        stop=10000,
        step=10,
        value=defaults["area_min"],
        label="Min Area",
    )
    area_max = mo.ui.number(
        start=0,
        stop=100000,
        step=100,
        value=defaults["area_max"],
        label="Max Area",
    )

    mo.vstack(
        [
            blur_input,
            mo.hstack([h_min, h_max], justify="start"),
            mo.hstack([s_min, s_max], justify="start"),
            mo.hstack([v_min, v_max], justify="start"),
            mo.hstack([morph_type, morph_k, morph_iter], justify="start"),
            mo.hstack([area_min, area_max], justify="start"),
        ]
    )
    return (
        area_max,
        area_min,
        blur_input,
        h_max,
        h_min,
        morph_iter,
        morph_k,
        morph_type,
        s_max,
        s_min,
        v_max,
        v_min,
    )


@app.cell
def _(
    area_max,
    area_min,
    blur_input,
    cv2,
    h_max,
    h_min,
    image_source,
    morph_iter,
    morph_k,
    morph_type,
    plt,
    s_max,
    s_min,
    v_max,
    v_min,
    vision,
):
    try:
        original = vision.load_image(image_source)

        blurred = vision.apply_blur(original, blur_input.value)

        mask = vision.segment_color(
            blurred,
            h_min.value,
            h_max.value,
            s_min.value,
            s_max.value,
            v_min.value,
            v_max.value,
        )

        processed = vision.morphological_ops(
            mask, morph_type.value, morph_k.value, morph_iter.value
        )

        count, contours = vision.find_buildings(
            processed, area_min.value, area_max.value
        )

        result_img = original.copy()
        cv2.drawContours(result_img, contours, -1, (255, 0, 0), 2)

        for i, cnt in enumerate(contours):
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.putText(
                    result_img,
                    str(i + 1),
                    (cX - 10, cY),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 0, 255),
                    2,
                )

        fig, axes = plt.subplots(1, 3, figsize=(20, 8))

        axes[0].imshow(original)
        axes[0].set_title("Original")
        axes[0].axis("off")

        axes[1].imshow(processed, cmap="gray")
        axes[1].set_title("Binary Mask (Processed)")
        axes[1].axis("off")

        axes[2].imshow(result_img)
        axes[2].set_title(f"Result: {count} Buildings")
        axes[2].axis("off")

        plt.tight_layout()

    except Exception as e:
        fig = None
        print(f"Error: {e}")

    fig
    return (count,)


@app.cell
def _(count, mo):
    mo.stat(value=str(count), label="Total Buildings", bordered=True)
    return


if __name__ == "__main__":
    app.run()
