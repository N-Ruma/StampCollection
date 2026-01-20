let current_sort = Number(
    new URLSearchParams(window.location.search).get("s") ?? 0
);
// 0: 追加順
// 1: 昇順(名前)
// 2: 降順(名前)
// 3: 獲得済み
// 4: 未獲得

const toggle_sort = () => {
    switch (current_sort) {
        case 0:
            current_sort = 1;
            break;
        case 1:
            current_sort = 2;
            break;
        case 2:
            current_sort = 3;
            break;
        case 3:
            current_sort = 4;
            break;
        case 4:
            current_sort = 0;
            break;
    }
};

// ボタン表示用
const sortLabels = [
    "追加順",
    "名前 昇順",
    "名前 降順",
    "獲得済み",
    "未獲得",
];

document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("sort-button");

    btn.textContent = sortLabels[current_sort];

    btn.addEventListener("click", () => {
        toggle_sort();
        location.href = `?s=${current_sort}`;
    });
});