import React, { useContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthContext from '../context/AuthProvider';
import './TaskList.css'; 

const TaskList = () => {
    const { authState } = useContext(AuthContext);
    const [tasks, setTasks] = useState([]);
    const token = authState?.token;
    const navigate = useNavigate();

    useEffect(() => {
        const fetchTasks = async () => {
            console.log(token);
            try {
                const response = await fetch('http://127.0.0.1:5000/tasks', {
                    headers: { Authorization: `Bearer ${token}` },
                });
                if (response.ok) {
                    const data = await response.json();
                    setTasks(data);
                } else {
                    console.error('Failed to fetch tasks:', await response.json());
                }
            } catch (error) {
                console.error('Error fetching tasks:', error);
            }
        };
        fetchTasks();
    }, [token]);

    const handleTaskClick = (taskId) => {
        navigate(`/tasks/${taskId}`);
    };

    return (
        <div className="task-list">
            <h1>Tasks</h1>
            <ul>
                {tasks.map((task) => (
                    <li key={task.id} onClick={() => handleTaskClick(task.id)} className="task-item">
                        <h2>{task.title}</h2>
                        <p>{task.description}</p>
                        <p>Due Date: {task.due_date ? new Date(task.due_date).toLocaleDateString() : 'N/A'}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default TaskList;
