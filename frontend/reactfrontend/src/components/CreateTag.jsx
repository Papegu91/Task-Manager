import React, { useState } from 'react';
 
const CreateTag = () => {
    const [name, setName] = useState('');

    const handleCreateTag = async (e) => {
        e.preventDefault();
        const response = await fetch('http://127.0.0.1:5000/tags', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name }),
        });
        if (response.ok) {
            alert('Tag created successfully!');
        }
    };

    return (
        <form onSubmit={handleCreateTag}>
            <input
                type="text"
                placeholder="Tag Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
            />
            <button type="submit">Create Tag</button>
        </form>
    );
};

export default CreateTag;
