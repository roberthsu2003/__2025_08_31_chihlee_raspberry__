document.addEventListener('DOMContentLoaded', () => {
    const todoInput = document.getElementById('todo-input');
    const addBtn = document.getElementById('add-btn');
    const todoList = document.getElementById('todo-list');

    // 渲染待辦事項列表
    const renderTodos = (todos) => {
        todoList.innerHTML = '';
        todos.forEach(todo => {
            const li = document.createElement('li');
            li.className = `todo-item ${todo.completed ? 'completed' : ''}`;
            li.dataset.id = todo.id;

            const title = document.createElement('span');
            title.className = 'title';
            title.textContent = todo.title;
            title.addEventListener('click', () => toggleComplete(todo.id, !todo.completed));

            const controls = document.createElement('div');
            controls.className = 'controls';

            const editBtn = document.createElement('button');
            editBtn.className = 'edit-btn';
            editBtn.textContent = '編輯';
            editBtn.addEventListener('click', () => toggleEditMode(li, todo));

            const deleteBtn = document.createElement('button');
            deleteBtn.className = 'delete-btn';
            deleteBtn.innerHTML = '&times;';
            deleteBtn.addEventListener('click', () => deleteTodo(todo.id));

            controls.appendChild(editBtn);
            controls.appendChild(deleteBtn);
            li.appendChild(title);
            li.appendChild(controls);
            todoList.appendChild(li);
        });
    };

    // 取得所有待辦事項
    const fetchTodos = async () => {
        try {
            const response = await fetch('/api/todos');
            const todos = await response.json();
            renderTodos(todos);
        } catch (error) {
            console.error('Error fetching todos:', error);
        }
    };

    // 新增待辦事項
    const addTodo = async () => {
        const title = todoInput.value.trim();
        if (title === '') return;

        try {
            const response = await fetch('/api/todos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ title: title, completed: false }),
            });
            if (response.ok) {
                todoInput.value = '';
                fetchTodos();
            }
        } catch (error) {
            console.error('Error adding todo:', error);
        }
    };

    // 切換完成狀態
    const toggleComplete = async (id, completed) => {
        try {
            await fetch(`/api/todos/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ completed: completed }),
            });
            fetchTodos();
        } catch (error) {
            console.error('Error updating todo:', error);
        }
    };

    // 刪除待辦事項
    const deleteTodo = async (id) => {
        try {
            await fetch(`/api/todos/${id}`, {
                method: 'DELETE',
            });
            fetchTodos();
        } catch (error) {
            console.error('Error deleting todo:', error);
        }
    };

    // 更新標題
    const updateTitle = async (id, newTitle) => {
        try {
            await fetch(`/api/todos/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ title: newTitle }),
            });
            fetchTodos();
        } catch (error) {
            console.error('Error updating title:', error);
        }
    };

    // 切換編輯模式
    const toggleEditMode = (li, todo) => {
        const titleSpan = li.querySelector('.title');
        const editBtn = li.querySelector('.edit-btn');
        const isEditing = li.classList.contains('editing');

        if (isEditing) {
            const input = li.querySelector('.edit-input');
            updateTitle(todo.id, input.value);
            // fetchTodos() 會自動重繪，所以不用手動切換回來
        } else {
            li.classList.add('editing');
            const currentTitle = titleSpan.textContent;
            const input = document.createElement('input');
            input.type = 'text';
            input.className = 'edit-input';
            input.value = currentTitle;
            li.replaceChild(input, titleSpan);
            input.focus();
            editBtn.textContent = '儲存';
        }
    };

    // 事件監聽
    addBtn.addEventListener('click', addTodo);
    todoInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addTodo();
        }
    });

    // 初始載入
    fetchTodos();
});
