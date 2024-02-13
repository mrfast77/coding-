window.addEventListener('load', () => {
    let todos = JSON.parse(localStorage.getItem('todos')) || [];
    const form = document.querySelector("#task-form");

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const todo = {
            content: e.target.elements.content.value
        }

        todos.push(todo);

        localStorage.setItem('todos', JSON.stringify(todos));

        e.target.reset();

        DisplayTodos()
    })

    DisplayTodos()

})
     
function DisplayTodos () {    
    const list = document.querySelector("#tasks");
    list.innerHTML = "";

    todos.forEach(todo => {
        const todoItem = document.createElement('div');
        todoItem.classList.add('todo-item');

        const taskInputElement = document.createElement("input");
        const taskContentElement = document.createElement("div");
        const taskActionsElement = document.createElement("div");
        const taskEditElement = document.createElement("button");
        const taskDeleteElement = document.createElement("button");

        taskContentElement.classList.add("content");
        taskInputElement.classList.add("text");
        taskInputElement.type = "text";
        taskInputElement.value = task;
        taskInputElement.setAttribute("readonly", "readonly");
        taskActionsElement.classList.add("actions");
        taskEditElement.classList.add("edit");
        taskEditElement.innerHTML = "Edit"
        taskDeleteElement.classList.add("delete");
        taskDeleteElement.innerHTML = "Delete"

        todoItem.appendChild(taskContentElement);
        todoItem.appendChild(taskActionsElement);
        taskContentElement.appendChild(taskInputElement);
        taskActionsElement.appendChild(taskEditElement);
        taskActionsElement.appendChild(taskDeleteElement);

        list.appendChild(todoItem);

        // Edit tasks
        taskEditElement.addEventListener('click', () => {
            if (taskEditElement.innerText.toLowerCase() == "edit") {
                taskInputElement.removeAttribute("readonly");
                taskInputElement.focus();
                taskEditElement.innerText = "Save";
            } else {
                taskInputElement.setAttribute("readonly", "readonly");
                taskEditElement.innerText = "Edit";
                localStorage.setItem('todos', JSON.stringify(todos));
                DisplayTodos()
            }
        })

        // Delete tasks
        taskDeleteElement.addEventListener('click', () => {
            listElement.removeChild(taskElement);
        })
    })

}
