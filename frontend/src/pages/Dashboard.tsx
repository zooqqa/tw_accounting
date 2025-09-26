import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { 
  Wallet, 
  TrendingUp, 
  TrendingDown, 
  ArrowUpDown,
  DollarSign,
  Bitcoin,
  Eye,
  Plus
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { accountsApi, transactionsApi, cryptoApi } from '@/services/api';
import { formatCurrency, formatNumber, formatDate } from '@/utils';
import type { Account, Transaction } from '@/types';

interface StatsCardProps {
  title: string;
  value: string;
  icon: React.ComponentType<{ className?: string }>;
  trend?: {
    value: number;
    isPositive: boolean;
  };
  color: string;
}

function StatsCard({ title, value, icon: Icon, trend, color }: StatsCardProps) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center">
        <div className={`p-3 rounded-lg ${color}`}>
          <Icon className="h-6 w-6 text-white" />
        </div>
        <div className="ml-4 flex-1">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-semibold text-gray-900">{value}</p>
          {trend && (
            <div className="flex items-center mt-1">
              {trend.isPositive ? (
                <TrendingUp className="h-4 w-4 text-green-500" />
              ) : (
                <TrendingDown className="h-4 w-4 text-red-500" />
              )}
              <span className={`text-sm ml-1 ${trend.isPositive ? 'text-green-600' : 'text-red-600'}`}>
                {trend.value > 0 ? '+' : ''}{trend.value}%
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function AccountCard({ account }: { account: Account }) {
  return (
    <div className="bg-white rounded-lg shadow p-4">
      <div className="flex items-center justify-between">
        <div>
          <h4 className="font-medium text-gray-900">{account.name}</h4>
          <p className="text-sm text-gray-500">{account.type} • {account.currency}</p>
        </div>
        <div className="text-right">
          <p className="text-lg font-semibold text-gray-900">
            {formatCurrency(account.balance, account.currency)}
          </p>
          <Link
            to={`/accounts/${account.id}`}
            className="text-sm text-primary-600 hover:text-primary-500 flex items-center"
          >
            <Eye className="h-4 w-4 mr-1" />
            Подробнее
          </Link>
        </div>
      </div>
    </div>
  );
}

function TransactionRow({ transaction }: { transaction: Transaction }) {
  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'income':
        return <TrendingUp className="h-4 w-4 text-green-500" />;
      case 'expense':
        return <TrendingDown className="h-4 w-4 text-red-500" />;
      case 'transfer':
        return <ArrowUpDown className="h-4 w-4 text-blue-500" />;
      default:
        return <DollarSign className="h-4 w-4 text-gray-500" />;
    }
  };

  const getAmountColor = (type: string) => {
    switch (type) {
      case 'income':
        return 'text-green-600';
      case 'expense':
        return 'text-red-600';
      default:
        return 'text-gray-900';
    }
  };

  return (
    <tr className="hover:bg-gray-50">
      <td className="px-6 py-4 whitespace-nowrap">
        <div className="flex items-center">
          {getTypeIcon(transaction.type)}
          <div className="ml-3">
            <p className="text-sm font-medium text-gray-900">{transaction.description}</p>
            <p className="text-xs text-gray-500">{formatDate(transaction.date)}</p>
          </div>
        </div>
      </td>
      <td className="px-6 py-4 whitespace-nowrap">
        <span className="px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-800">
          {transaction.type === 'income' ? 'Доход' : transaction.type === 'expense' ? 'Расход' : 'Перевод'}
        </span>
      </td>
      <td className={`px-6 py-4 whitespace-nowrap text-sm font-medium ${getAmountColor(transaction.type)}`}>
        {transaction.type === 'expense' ? '-' : ''}{formatCurrency(transaction.amount)}
      </td>
      <td className="px-6 py-4 whitespace-nowrap">
        <span className={`px-2 py-1 text-xs font-medium rounded-full ${
          transaction.status === 'completed' ? 'bg-green-100 text-green-800' :
          transaction.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
          'bg-gray-100 text-gray-800'
        }`}>
          {transaction.status === 'completed' ? 'Завершено' : 
           transaction.status === 'pending' ? 'Ожидание' : 'Черновик'}
        </span>
      </td>
    </tr>
  );
}

export default function Dashboard() {
  const { data: accounts = [] } = useQuery({
    queryKey: ['accounts'],
    queryFn: accountsApi.getAll,
  });

  const { data: transactions = [] } = useQuery({
    queryKey: ['transactions', 'recent'],
    queryFn: () => transactionsApi.getAll(),
  });

  const { data: cryptoRates } = useQuery({
    queryKey: ['crypto-rates'],
    queryFn: cryptoApi.getRates,
    refetchInterval: 5 * 60 * 1000, // Обновляем каждые 5 минут
  });

  // Подсчет статистики
  const totalBalance = accounts.reduce((sum, account) => sum + account.balance, 0);
  const recentTransactions = transactions.slice(0, 5);
  
  const monthlyIncome = transactions
    .filter(t => t.type === 'income' && new Date(t.date) > new Date(Date.now() - 30 * 24 * 60 * 60 * 1000))
    .reduce((sum, t) => sum + t.amount, 0);
    
  const monthlyExpenses = transactions
    .filter(t => t.type === 'expense' && new Date(t.date) > new Date(Date.now() - 30 * 24 * 60 * 60 * 1000))
    .reduce((sum, t) => sum + t.amount, 0);

  const cryptoAccounts = accounts.filter(account => account.type === 'crypto');

  return (
    <div className="space-y-6">
      {/* Заголовок */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Главная панель</h1>
        <div className="flex space-x-3">
          <Link
            to="/transactions/create"
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700"
          >
            <Plus className="h-4 w-4 mr-2" />
            Новая транзакция
          </Link>
        </div>
      </div>

      {/* Статистические карты */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Общий баланс"
          value={formatCurrency(totalBalance)}
          icon={Wallet}
          color="bg-blue-500"
        />
        <StatsCard
          title="Доходы за месяц"
          value={formatCurrency(monthlyIncome)}
          icon={TrendingUp}
          color="bg-green-500"
        />
        <StatsCard
          title="Расходы за месяц"
          value={formatCurrency(monthlyExpenses)}
          icon={TrendingDown}
          color="bg-red-500"
        />
        <StatsCard
          title="Количество счетов"
          value={accounts.length.toString()}
          icon={DollarSign}
          color="bg-purple-500"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Счета */}
        <div className="lg:col-span-2">
          <div className="bg-white shadow rounded-lg">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-medium text-gray-900">Счета</h3>
                <Link
                  to="/accounts"
                  className="text-sm text-primary-600 hover:text-primary-500"
                >
                  Все счета
                </Link>
              </div>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {accounts.slice(0, 5).map((account) => (
                  <AccountCard key={account.id} account={account} />
                ))}
                {accounts.length === 0 && (
                  <div className="text-center py-8">
                    <Wallet className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500">Нет счетов</p>
                    <Link
                      to="/accounts/create"
                      className="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-primary-600 bg-primary-100 hover:bg-primary-200"
                    >
                      Создать счет
                    </Link>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Криптовалюты */}
        <div>
          <div className="bg-white shadow rounded-lg">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-medium text-gray-900">Криптовалюты</h3>
                <Link
                  to="/crypto"
                  className="text-sm text-primary-600 hover:text-primary-500"
                >
                  Подробнее
                </Link>
              </div>
            </div>
            <div className="p-6">
              {cryptoRates && (
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <Bitcoin className="h-5 w-5 text-orange-500 mr-2" />
                      <span className="text-sm font-medium">TRX</span>
                    </div>
                    <span className="text-sm font-semibold">
                      ${formatNumber(cryptoRates.rates.TRX, 6)}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <DollarSign className="h-5 w-5 text-green-500 mr-2" />
                      <span className="text-sm font-medium">USDT</span>
                    </div>
                    <span className="text-sm font-semibold">
                      ${formatNumber(cryptoRates.rates.USDT, 3)}
                    </span>
                  </div>
                </div>
              )}
              
              {cryptoAccounts.length > 0 && (
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <h4 className="text-sm font-medium text-gray-900 mb-2">Крипто-счета</h4>
                  <div className="space-y-2">
                    {cryptoAccounts.map((account) => (
                      <div key={account.id} className="flex justify-between text-sm">
                        <span className="text-gray-600">{account.name}</span>
                        <span className="font-medium">{formatCurrency(account.balance)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Последние транзакции */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-medium text-gray-900">Последние транзакции</h3>
            <Link
              to="/transactions"
              className="text-sm text-primary-600 hover:text-primary-500"
            >
              Все транзакции
            </Link>
          </div>
        </div>
        <div className="overflow-hidden">
          {recentTransactions.length > 0 ? (
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Описание
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Тип
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Сумма
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Статус
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {recentTransactions.map((transaction) => (
                  <TransactionRow key={transaction.id} transaction={transaction} />
                ))}
              </tbody>
            </table>
          ) : (
            <div className="text-center py-8">
              <ArrowUpDown className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">Нет транзакций</p>
              <Link
                to="/transactions/create"
                className="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-primary-600 bg-primary-100 hover:bg-primary-200"
              >
                Создать транзакцию
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
