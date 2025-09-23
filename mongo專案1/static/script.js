// script.js (目前不需要複雜的JS，因為表單提交會重新導向)
// 如果未來需要AJAX提交，可以在這裡添加邏輯

document.addEventListener('DOMContentLoaded', () => {
    // 這裡可以添加一些前端互動邏輯，例如確認刪除等
    const deleteForms = document.querySelectorAll('.delete-form');
    deleteForms.forEach(form => {
        form.addEventListener('submit', (event) => {
            if (!confirm('確定要刪除這個待辦事項嗎？')) {
                event.preventDefault();
            }
        });
    });

    const completeForms = document.querySelectorAll('.complete-form');
    completeForms.forEach(form => {
        form.addEventListener('submit', (event) => {
            // 可以在這裡添加一些完成前的確認，如果需要的話
            // event.preventDefault(); // 如果要阻止預設提交並使用AJAX
        });
    });
});
