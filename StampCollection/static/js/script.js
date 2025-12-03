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