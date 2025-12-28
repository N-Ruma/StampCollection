let current_sort = 0;
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
        default:
            break;
    }
};