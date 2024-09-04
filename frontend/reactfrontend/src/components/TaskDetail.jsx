import React, { useEffect, useState, useContext } from 'react';
import { useParams } from 'react-router-dom';
import AuthContext from '../context/AuthProvider';
import './TaskDetail.css'; 

const TaskDetail = () => {
    const { taskId } = useParams();
    const { authState } = useContext(AuthContext);
    const [task, setTask] = useState(null);
    const token = authState?.token;

    useEffect(() => {
        const fetchTaskDetail = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:5000/tasks/${taskId}`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                if (response.ok) {
                    const data = await response.json();
                    setTask(data);
                } else {
                    console.error('Failed to fetch task details:', await response.json());
                }
            } catch (error) {
                console.error('Error fetching task details:', error);
            }
        };

        fetchTaskDetail();
    }, [taskId, token]);

    if (!task) return <div>Loading...</div>;

    return (
        <div className="task-detail">
            <h1>{task.title}</h1>
            <p><strong>Description:</strong> {task.description}</p>
            <p><strong>Due Date:</strong> {task.due_date ? new Date(task.due_date).toLocaleDateString() : 'N/A'}</p>
            <p><strong>Completed:</strong> {task.completed ? 'Yes' : 'No'}</p>
        </div>
    );
};

export default TaskDetail;
