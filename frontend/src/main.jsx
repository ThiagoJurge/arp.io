import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import { BrowserRouter } from "react-router-dom";
import { ConfigProvider, theme } from 'antd';
const { darkAlgorithm } = theme;

ReactDOM.createRoot(document.getElementById('root')).render(

  <BrowserRouter>
    <ConfigProvider
      theme={{
        algorithm: [darkAlgorithm],
        token: {
          "colorPrimary": "red",
          "colorInfo": "red"
        },
      }}
    >
      <App />
    </ConfigProvider>
  </BrowserRouter>
)
