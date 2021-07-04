import React from 'react';
import { TweetItem } from './TweetItem';

export function TweetList({tweets}) {
    return (
        <ul>
            {tweets.map((tweet) => (
                <TweetItem key={tweet.id} tweet={tweet}/>
            ))}
        </ul>
    )
}
