import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './context/AuthProvider'; 

import Navbar from './components/Navbar';
import Register from './components/Register';
import Login from './components/Login';
import TaskList from './components/TaskList';
import CreateTask from './components/CreateTask';
import TaskDetail from './components/TaskDetail';
import TagList from './components/TagList';
import CreateTag from './components/CreateTag';

function App() {
    return (
        <AuthProvider>
            <Router>
                <Navbar /> 
                <Routes>
                    <Route path="/register" element={<Register />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/tasks/new" element={<CreateTask />} />
                    <Route path="/tasks/:taskId" element={<TaskDetail />} />
                    <Route path="/tasks" element={<TaskList />} />
                    <Route path="/tags/new" element={<CreateTag />} />
                    <Route path="/tags" element={<TagList />} />
                </Routes>
            </Router>
        </AuthProvider>
    );
}

export default App;
