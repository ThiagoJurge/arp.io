import React from 'react'
import { Route, Routes } from "react-router-dom";
import Flaps from './pages/Flaps';

const AppRoutes = () => {
    return (
        <Routes>
            <Route path="/" element={'bom dia'} />
            <Route path="/flaps" element={<Flaps />} />
            {/* <Route path="/antiguerreiro" element={<Antiguerreiro />} /> */}
        </Routes>
    )
}

export default AppRoutes