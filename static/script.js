document.addEventListener("DOMContentLoaded", loadTasks);

// Busca todas as tarefas no banco de dados via API GET
async function loadTasks() {
    try {
        const response = await fetch('/api/tasks');
        const tasks = await response.json();
        
        const taskList = document.getElementById("taskList");
        taskList.innerHTML = "";

        if (tasks.length === 0) {
            taskList.innerHTML = `<p style="text-align:center; color:#95a5a6;">Nenhuma tarefa salva no banco de dados.</p>`;
            return;
        }

        tasks.forEach(task => {
            renderTask(task);
        });
    } catch (error) {
        console.error("Erro ao carregar dados do banco:", error);
    }
}

// Salva uma nova tarefa no banco via API POST
async function addTask() {
    const input = document.getElementById("taskInput");
    const taskText = input.value.trim();

    if (taskText === "") {
        alert("Digite algo para salvar no banco!");
        return;
    }

    try {
        const response = await fetch('/api/tasks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ task: taskText })
        });

        if (response.ok) {
            input.value = "";
            loadTasks(); // Atualiza a lista com o registro recém-criado
        }
    } catch (error) {
        console.error("Erro ao gravar no banco:", error);
    }
}

// Renderiza a linha na tela associando o ID do Banco
function renderTask(task) {
    const taskList = document.getElementById("taskList");
    const li = document.createElement("li");

    li.innerHTML = `
        <span>${task.descricao}</span>
        <button class="delete-btn" onclick="deleteTask(${task.id})">Excluir</button>
    `;

    taskList.appendChild(li);
}

// Deleta do banco de dados usando o ID como parâmetro
async function deleteTask(id) {
    try {
        const response = await fetch(`/api/tasks/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadTasks(); // Recarrega a lista sem o item removido
        }
    } catch (error) {
        console.error("Erro ao remover do banco:", error);
    }
}