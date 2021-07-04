import React from 'react';

export function TweetItem({tweet}) {
    const{id, tweet} = tweet;

    return (
        <li>
            {tweet}
        </li>
    );
}
