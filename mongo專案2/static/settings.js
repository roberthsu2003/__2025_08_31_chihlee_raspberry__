document.addEventListener('DOMContentLoaded', () => {
    const clearCompletedBtn = document.getElementById('clear-completed-btn');
    const clearAllBtn = document.getElementById('clear-all-btn');

    if (clearCompletedBtn) {
        clearCompletedBtn.addEventListener('click', async () => {
            if (confirm('您確定要清除所有已完成的任務嗎？')) {
                const response = await fetch('/api/todos/completed', { method: 'DELETE' });
                if (response.ok) {
                    alert('已完成的任務已清除');
                } else {
                    alert('清除失敗');
                }
            }
        });
    }

    if (clearAllBtn) {
        clearAllBtn.addEventListener('click', async () => {
            if (confirm('您確定要清除所有的任務嗎？此操作無法復原。')) {
                const response = await fetch('/api/todos/all', { method: 'DELETE' });
                if (response.ok) {
                    alert('所有任務已清除');
                } else {
                    alert('清除失敗');
                }
            }
        });
    }
});
