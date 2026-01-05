function draw_image(id, imageUrl) {
  const canvas = document.getElementById("canvas_" + id);
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  const img = new Image();
  img.src = imageUrl;

  img.onload = function () {
    canvas.width = 150;
    canvas.height = 150;

    // UNKNOWN 表現（グレースケール + ぼかし）
    ctx.filter = "grayscale(100%) blur(3px)";
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
  };
}
