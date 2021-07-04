import React from 'react';
import { TopicItem } from './TopicItem';

export function TopicList({topics, toggleTopic}) {
    return (
        <ul>
            {topics.map((topic) => (
                <TopicItem key={topic.id} topic={topic} toggleTopic={toggleTopic}/>
            ))}
        </ul>
    )
}
