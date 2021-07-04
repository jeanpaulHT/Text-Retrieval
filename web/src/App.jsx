import React, {Fragment, useState, useRef, useEffect} from 'react'
import {v4 as uuidv4} from 'uuid'
import { TodoList } from './components/TodoList'

const KEY = "todoApp.todos";

export function App() {
    const [todos, setTodos] = useState([
        {id: 1, task: "Topic 1", completed: false}
    ]);

    const todoTaskRef = useRef();

    useEffect(() => {
        const storedTodos = JSON.parse(localStorage.getItem(KEY));
        if(storedTodos) {
            setTodos(storedTodos);
        }
    }, []);

    useEffect(() => {
        localStorage.setItem(KEY, JSON.stringify(todos));
    }, [todos]);

    const toggleTodo = (id) => {
        const newTodos = [...todos];
        const todo = newTodos.find((todo) => todo.id === id);
        todo.completed = !todo.completed;
        setTodos(newTodos);
    };

    const handleTodoAdd = () => {
        const task = todoTaskRef.current.value;
        if (task === '') return;

        setTodos((prevTodos) => {
            return [...prevTodos, {id: uuidv4(), task, completed: false}]
        });

        todoTaskRef.current.value = null;
    };

    const handleClearAll = () => {
        const newTodos = todos.filter((todo) => !todo.completed);
        setTodos(newTodos);
    };

    return (
        <Fragment>
            <h1>Buscador de Tweets</h1>
            <h2>Temas:</h2>
            <TodoList todos={todos} toggleTodo={toggleTodo}/>
            <input ref={todoTaskRef} type="text" placeholder="Agregar tema"/>
            <button onClick={handleTodoAdd}>+</button>
            <button onClick={handleClearAll}>🚮</button>
            {/* <div>Te quedan {todos.filter((todo) => !todo.completed).length} tareas por terminar.</div> */}
            <h2>Queries:</h2>
            <input type="text" placeholder="Insertar query"/>
            <button >Buscar</button>
        </Fragment>
    );
}