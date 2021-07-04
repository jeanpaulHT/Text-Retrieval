import React, {Fragment, useState, useRef, useEffect} from 'react'
import {v4 as uuidv4} from 'uuid'
import { TopicList } from './components/TopicList'

const KEY = "topicApp.topics";

export function App() {
    const [topics, setTopics] = useState([
        {id: 1, task: "covid", selected: false}
    ]);

    const topicTaskRef = useRef();

    // preserve topics
    useEffect(() => {
        const storedTopics = JSON.parse(localStorage.getItem(KEY));
        if(storedTopics) {
            setTopics(storedTopics);
        }
    }, []);

    useEffect(() => {
        localStorage.setItem(KEY, JSON.stringify(topics));
    }, [topics]);


    // topic functions
    const toggleTopic = (id) => {
        const newTopics = [...topics];
        const topic = newTopics.find((topic) => topic.id === id);
        topic.selected = !topic.selected;
        setTopics(newTopics);
    };

    const handleTopicAdd = () => {
        const task = topicTaskRef.current.value;
        if (task === '') return;

        setTopics((prevTopics) => {
            return [...prevTopics, {id: uuidv4(), task, selected: false}]
        });

        topicTaskRef.current.value = null;
    };

    const handleClearAll = () => {
        const newTopics = topics.filter((topic) => !topic.selected);
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
            {/* <div>{topics.filter((topic) => !topic.selected).length} temas seleccionados.</div> */}
            <h2>Queries:</h2>
            <input type="text" placeholder="Insertar query"/>
            <button >Buscar</button>
        </Fragment>
    );
}