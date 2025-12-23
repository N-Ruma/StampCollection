const adjust_size_width = (canvas_width, image_aspect_ratio, scale) => {
    const draw_width = canvas_width * scale;
    const draw_height = draw_width / image_aspect_ratio;
    return { draw_width, draw_height };
}

const adjust_size_height = (canvas_height, image_aspect_ratio, scale) => {
    const draw_height = canvas_height * scale;
    const draw_width = draw_height * image_aspect_ratio;
    return { draw_width, draw_height };
}

const calculate_image_size = (image_width, image_height, canvas_width, canvas_height, scale=1.0) => {
    const image_aspect_ratio = image_width / image_height;
    const canvas_aspect_ratio = canvas_width / canvas_height;
    if (image_aspect_ratio < canvas_aspect_ratio) {
        return adjust_size_width(canvas_width, image_aspect_ratio, scale);
    } else {
        return adjust_size_height(canvas_height, image_aspect_ratio, scale);
    }
}

const draw_image = (stamp_id, stamp_url) => {
    const canvas = document.getElementById("canvas_" + stamp_id);
    const ctx = canvas.getContext("2d");

    let image = new Image();
    image.src = stamp_url;

    image.onload = () => {
        const canvas_width = canvas.width;
        const canvas_height = canvas.height;
        const image_width = image.width;
        const image_height = image.height;
        const { draw_width, draw_height } = calculate_image_size(image_width, image_height, canvas_width, canvas_height);

        // blur filter
        ctx.filter = "blur(5px)";

        // draw image
        const x = (canvas_width - draw_width) / 2;
        const y = (canvas_height - draw_height) / 2;
        ctx.drawImage(image, x, y, draw_width, draw_height);

        // get pixel data
        const src = ctx.getImageData(0, 0, canvas_width, canvas_height);
        let pixel = src.data; // [r, g, b, a, r, g, b, a, ...]

        // gray scale
        for (let i = 0; i < pixel.length; i += 4) {
            const color = 0.2126 * pixel[i] + 0.7152 * pixel[i + 1] + 0.0722 * pixel[i + 2];
            pixel[i] = pixel[i + 1] = pixel[i + 2] = color;
        }

        ctx.putImageData(src, 0, 0);
    }
}