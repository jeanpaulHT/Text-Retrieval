import React from 'react';

export function TopicItem({topic, toggleTopic}) {
    const{id, task, completed} = topic;

    const handleTopicClick = () => {
        toggleTopic(id);
    }

    return (
        <li>
            <input type="checkbox" onChange={handleTopicClick}/>
            {task}
        </li>
    );
}
