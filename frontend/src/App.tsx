import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import Layout from '@/components/Layout';
import Login from '@/pages/Login';
import Dashboard from '@/pages/Dashboard';

// Компонент для защищенных роутов
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />;
}

// Временные заглушки для страниц
function Accounts() {
  return (
    <div className="text-center py-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Счета</h2>
      <p className="text-gray-500">Страница счетов в разработке</p>
    </div>
  );
}

function Transactions() {
  return (
    <div className="text-center py-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Транзакции</h2>
      <p className="text-gray-500">Страница транзакций в разработке</p>
    </div>
  );
}

function Crypto() {
  return (
    <div className="text-center py-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Криптовалюты</h2>
      <p className="text-gray-500">Страница криптовалют в разработке</p>
    </div>
  );
}

function Projects() {
  return (
    <div className="text-center py-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Проекты</h2>
      <p className="text-gray-500">Страница проектов в разработке</p>
    </div>
  );
}

function Categories() {
  return (
    <div className="text-center py-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Категории</h2>
      <p className="text-gray-500">Страница категорий в разработке</p>
    </div>
  );
}

function Counterparties() {
  return (
    <div className="text-center py-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Контрагенты</h2>
      <p className="text-gray-500">Страница контрагентов в разработке</p>
    </div>
  );
}

function Reports() {
  return (
    <div className="text-center py-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Отчеты</h2>
      <p className="text-gray-500">Страница отчетов в разработке</p>
    </div>
  );
}

function Settings() {
  return (
    <div className="text-center py-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Настройки</h2>
      <p className="text-gray-500">Страница настроек в разработке</p>
    </div>
  );
}

function App() {
  return (
    <Routes>
      {/* Публичные роуты */}
      <Route path="/login" element={<Login />} />
      
      {/* Защищенные роуты */}
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="accounts" element={<Accounts />} />
        <Route path="transactions" element={<Transactions />} />
        <Route path="crypto" element={<Crypto />} />
        <Route path="projects" element={<Projects />} />
        <Route path="categories" element={<Categories />} />
        <Route path="counterparties" element={<Counterparties />} />
        <Route path="reports" element={<Reports />} />
        <Route path="settings" element={<Settings />} />
      </Route>

      {/* Обработка несуществующих роутов */}
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}

export default App;
