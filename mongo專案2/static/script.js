document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const todoForm = document.getElementById('todo-form');
    const taskInput = document.getElementById('task-input');
    const todoList = document.getElementById('todo-list');
    const filterMenu = document.getElementById('filter-menu');

    // App State
    let currentFilter = 'active'; // 'active' or 'completed'

    // --- API Calls ---

    async function updateTask(id, data) {
        const response = await fetch(`/api/todos/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        if (!response.ok) console.error('Failed to update task');
        return response.ok;
    }

    async function deleteTodo(id) {
        const response = await fetch(`/api/todos/${id}`, { method: 'DELETE' });
        if (response.ok) {
            fetchTodos();
        } else {
            console.error('Failed to delete task');
        }
    }

    async function addTodo(event) {
        event.preventDefault();
        const task = taskInput.value.trim();
        if (task === '') return;

        const response = await fetch('/api/todos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ task: task }),
        });

        if (response.ok) {
            taskInput.value = '';
            fetchTodos();
        } else {
            console.error('Failed to add task');
        }
    }

    // --- DOM & Event Handling ---

    async function fetchTodos() {
        let url = '/api/todos';
        if (currentFilter === 'active') {
            url += '?completed=false';
        } else if (currentFilter === 'completed') {
            url += '?completed=true';
        }

        const response = await fetch(url);
        const todos = await response.json();
        renderTodos(todos);
    }

    function renderTodos(todos) {
        todoList.innerHTML = '';
        todos.forEach(todo => {
            const li = createTodoElement(todo);
            todoList.appendChild(li);
        });
    }

    function createTodoElement(todo) {
        const li = document.createElement('li');
        li.className = 'todo-item';
        if (todo.completed) {
            li.classList.add('completed');
        }
        li.dataset.id = todo._id;

        li.innerHTML = `
            <div class="task-details">
                <span class="task-text">${todo.task}</span>
                <span class="task-date">${todo.date}</span>
            </div>
            <div class="task-actions">
                <label class="checkbox-container">
                    <input type="checkbox" ${todo.completed ? 'checked' : ''}>
                    <span class="checkmark"></span>
                </label>
                <button class="delete-btn" aria-label="Delete task">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                </button>
            </div>
        `;

        addEventListenersToTodoItem(li, todo);
        return li;
    }

    function addEventListenersToTodoItem(li, todo) {
        const taskDetails = li.querySelector('.task-details');
        const checkbox = li.querySelector('input[type="checkbox"]');
        const deleteBtn = li.querySelector('.delete-btn');

        checkbox.addEventListener('change', async () => {
            const isCompleted = checkbox.checked;
            const success = await updateTask(todo._id, { completed: isCompleted });
            if (success) {
                li.classList.add('removing');
                li.addEventListener('transitionend', () => li.remove());
            }
        });

        deleteBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            deleteTodo(todo._id);
        });

        taskDetails.addEventListener('click', () => {
            if (li.querySelector('.edit-input')) return;
            enableEditMode(li, todo);
        });
    }

    function enableEditMode(li, todo) {
        const taskDetails = li.querySelector('.task-details');
        const taskTextEl = li.querySelector('.task-text');
        const currentText = todo.task;

        taskDetails.style.display = 'none';

        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'edit-input';
        input.value = currentText;
        
        li.insertBefore(input, li.querySelector('.task-actions'));
        input.focus();
        input.select();

        const saveChanges = async () => {
            const newText = input.value.trim();
            input.remove();
            taskDetails.style.display = 'flex';

            if (newText && newText !== currentText) {
                const success = await updateTask(todo._id, { task: newText });
                if (success) {
                    taskTextEl.textContent = newText;
                    todo.task = newText;
                }
            }
        };

        input.addEventListener('blur', saveChanges);
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') input.blur();
            else if (e.key === 'Escape') {
                input.remove();
                taskDetails.style.display = 'flex';
            }
        });
    }

    filterMenu.addEventListener('click', (e) => {
        if (e.target.matches('.filter-btn')) {
            const newFilter = e.target.dataset.filter;
            if (newFilter !== currentFilter) {
                currentFilter = newFilter;
                filterMenu.querySelector('.active').classList.remove('active');
                e.target.classList.add('active');
                todoForm.style.display = (currentFilter === 'active') ? 'flex' : 'none';
                fetchTodos();
            }
        }
    });

    // --- Initial Setup ---
    todoForm.addEventListener('submit', addTodo);
    fetchTodos(); // Initial fetch for 'active' tasks
});