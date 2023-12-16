import Routes from "./AppRoutes"
import React from 'react';
import { Breadcrumb, Divider, Layout, Menu, theme } from 'antd';
import { NavLink } from "react-router-dom";
import { PieChartOutlined } from "@ant-design/icons";
const { Header, Content, Footer } = Layout;
import './App.css'
import api from "./api/api";


const App = () => {

  function getItem(label, key, icon, children) {
    return {
      key,
      icon,
      children,
      label,
    };
  }

  const items = [
    getItem(
      <NavLink to="/flaps">Terror do Backbone</NavLink>,
      "1",
      <PieChartOutlined />
    ), getItem(<NavLink to="/antiguerreiro">Anti Guerreiro</NavLink>,
      "2",
      <PieChartOutlined />)

  ]

  const {
    token: { colorBgContainer },
  } = theme.useToken();


  return (
    <Layout className="layout" style={{
      height: '100vh'
    }}>
      <Header
        style={{
          display: 'flex',
          alignItems: 'center',
          background: colorBgContainer
        }}
      >
        <Menu
          theme="light"
          mode="horizontal"
          items={items}
        />
      </Header>
      <Content
        style={{
          padding: '0 50px',
          overflow: 'auto'
        }}
      >
        <Divider />
        <div
          className="site-layout-content"
          style={{
            background: colorBgContainer
          }}
        >
          <Routes />
        </div>
      </Content>
      <Footer
        style={{
          textAlign: 'center',
        }}
      >
        NOC Altarede © 2023
      </Footer>
    </Layout>

  )
}

export default App