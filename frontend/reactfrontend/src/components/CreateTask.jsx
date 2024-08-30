import React, { useContext, useState } from 'react';
import AuthContext from '../context/AuthProvider';

const CreateTask = () => {
    const { authState } = useContext(AuthContext);
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [dueDate, setDueDate] = useState('');
    const token = authState?.token;

    const handleCreateTask = async (e) => {
        e.preventDefault();
        const response = await fetch('http://127.0.0.1:5000/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ title, description, due_date: dueDate }),
        });
        if (response.ok) {
            alert('Task created successfully!');
        }
    };

    return (
        <form onSubmit={handleCreateTask}>
            <input
                type="text"
                placeholder="Title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
            />
            <input
                type="text"
                placeholder="Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
            />
            <input
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
            />
            <button type="submit">Create Task</button>
        </form>
    );
};

export default CreateTask;
