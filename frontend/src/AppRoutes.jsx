import React from 'react'
import { Route, Routes } from "react-router-dom";
import Flaps from './pages/Flaps';
import AntiGuerreiro from './pages/AntiGuerreiro';

const AppRoutes = () => {
    return (
        <Routes>
            <Route path="/" element={'bom dia'} />
            <Route path="/flaps" element={<Flaps />} />
            <Route path="/antiguerreiro" element={<AntiGuerreiro />} />
            <Route path="*" element={<h1>NotFoundPage</h1>} />
        </Routes>
    )
}

export default AppRoutes