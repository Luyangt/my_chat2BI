import React from 'react';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import QueryInterface from './QueryInterface';
import './App.css';

function App() {
  return (
    <ConfigProvider locale={zhCN}>
      <div className="App">
        <QueryInterface />
      </div>
    </ConfigProvider>
  );
}

export default App;
