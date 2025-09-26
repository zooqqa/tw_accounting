import React, { useState } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard,
  Wallet,
  ArrowUpDown,
  TrendingUp,
  Users,
  FolderOpen,
  Tag,
  Settings,
  LogOut,
  Menu,
  X,
  Bitcoin,
  DollarSign,
} from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { cn } from '@/utils';

const navigation = [
  { name: 'Главная', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Счета', href: '/accounts', icon: Wallet },
  { name: 'Транзакции', href: '/transactions', icon: ArrowUpDown },
  { name: 'Криптовалюты', href: '/crypto', icon: Bitcoin },
  { name: 'Проекты', href: '/projects', icon: FolderOpen },
  { name: 'Категории', href: '/categories', icon: Tag },
  { name: 'Контрагенты', href: '/counterparties', icon: Users },
  { name: 'Отчеты', href: '/reports', icon: TrendingUp },
  { name: 'Настройки', href: '/settings', icon: Settings },
];

interface LayoutProps {
  children?: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="h-screen flex bg-gray-50">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-gray-600 bg-opacity-75 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div
        className={cn(
          'fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0',
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-between h-16 px-6 border-b border-gray-200">
            <div className="flex items-center space-x-2">
              <DollarSign className="h-8 w-8 text-primary-600" />
              <span className="text-xl font-bold text-gray-900">TW Accounting</span>
            </div>
            <button
              type="button"
              className="lg:hidden"
              onClick={() => setSidebarOpen(false)}
            >
              <X className="h-6 w-6 text-gray-400" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-1 sidebar-scrollbar overflow-y-auto">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={cn(
                    'group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors',
                    isActive
                      ? 'bg-primary-100 text-primary-700'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  )}
                  onClick={() => setSidebarOpen(false)}
                >
                  <item.icon
                    className={cn(
                      'mr-3 flex-shrink-0 h-5 w-5',
                      isActive ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500'
                    )}
                  />
                  {item.name}
                </Link>
              );
            })}
          </nav>

          {/* User info */}
          <div className="flex-shrink-0 p-4 border-t border-gray-200">
            <div className="flex items-center justify-between">
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {user?.name || user?.email}
                </p>
                <p className="text-xs text-gray-500">
                  {user?.is_superuser ? 'Администратор' : 'Пользователь'}
                </p>
              </div>
              <button
                type="button"
                onClick={handleLogout}
                className="ml-3 p-2 text-gray-400 hover:text-gray-500 transition-colors"
                title="Выйти"
              >
                <LogOut className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col lg:pl-0">
        {/* Top bar */}
        <div className="flex-shrink-0 h-16 bg-white shadow-sm border-b border-gray-200 flex items-center px-6">
          <button
            type="button"
            className="lg:hidden mr-4"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu className="h-6 w-6 text-gray-500" />
          </button>
          
          <div className="flex-1">
            <h1 className="text-xl font-semibold text-gray-900">
              {navigation.find(item => item.href === location.pathname)?.name || 'TW Accounting'}
            </h1>
          </div>
        </div>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto">
          <div className="py-6">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
              {children || <Outlet />}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
