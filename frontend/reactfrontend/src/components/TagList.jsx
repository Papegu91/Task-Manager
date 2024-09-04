import React, { useEffect, useState } from 'react';
import './TagList.css';

const TagList = () => {
    const [tags, setTags] = useState([]);

    useEffect(() => {
        const fetchTags = async () => {
            const response = await fetch('http://127.0.0.1:5000/tags');
            const data = await response.json();
            if (response.ok) {
                setTags(data);
            }
        };
        fetchTags();
    }, []);

    return (
        <div>
            <h1>Tags</h1>
            <ul>
                {tags.map((tag) => (
                    <li key={tag.id}>{tag.name}</li>
                ))}
            </ul>
        </div>
    );
};

export default TagList;
