import React, {Fragment, useState, useRef, useEffect} from 'react'
import {v4 as uuidv4} from 'uuid'
import { TopicList } from './components/TopicList'

const KEY = "topicApp.topics";

export function App() {
    const [topics, setTopics] = useState([
        {id: 1, task: "Topic 1", completed: false}
    ]);

    const topicTaskRef = useRef();

    useEffect(() => {
        const storedTopics = JSON.parse(localStorage.getItem(KEY));
        if(storedTopics) {
            setTopics(storedTopics);
        }
    }, []);

    useEffect(() => {
        localStorage.setItem(KEY, JSON.stringify(topics));
    }, [topics]);

    const toggleTopic = (id) => {
        const newTopics = [...topics];
        const topic = newTopics.find((topic) => topic.id === id);
        topic.completed = !topic.completed;
        setTopics(newTopics);
    };

    const handleTopicAdd = () => {
        const task = topicTaskRef.current.value;
        if (task === '') return;

        setTopics((prevTopics) => {
            return [...prevTopics, {id: uuidv4(), task, completed: false}]
        });

        topicTaskRef.current.value = null;
    };

    const handleClearAll = () => {
        const newTopics = topics.filter((topic) => !topic.completed);
        setTopics(newTopics);
    };

    return (
        <Fragment>
            <h1>Buscador de Tweets</h1>
            <h2>Temas:</h2>
            <TopicList topics={topics} toggleTopic={toggleTopic}/>
            <input ref={topicTaskRef} type="text" placeholder="Agregar tema"/>
            <button onClick={handleTopicAdd}>+</button>
            <button onClick={handleClearAll}>🚮</button>
            {/* <div>{topics.filter((topic) => !topic.completed).length} temas seleccionados.</div> */}
            <h2>Queries:</h2>
            <input type="text" placeholder="Insertar query"/>
            <button >Buscar</button>
        </Fragment>
    );
}