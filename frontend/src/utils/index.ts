import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(amount: number, currency = 'USD'): string {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
}

export function formatNumber(value: number, decimals = 2): string {
  return new Intl.NumberFormat('ru-RU', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
}

export function formatDate(date: string | Date): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return new Intl.DateTimeFormat('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  }).format(d);
}

export function formatDateTime(date: string | Date): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return new Intl.DateTimeFormat('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(d);
}

export function getTransactionTypeLabel(type: string): string {
  const labels: Record<string, string> = {
    income: 'Доход',
    expense: 'Расход',
    transfer: 'Перевод',
  };
  return labels[type] || type;
}

export function getTransactionStatusLabel(status: string): string {
  const labels: Record<string, string> = {
    pending: 'Ожидание',
    completed: 'Завершено',
    cancelled: 'Отменено',
    draft: 'Черновик',
  };
  return labels[status] || status;
}

export function getAccountTypeLabel(type: string): string {
  const labels: Record<string, string> = {
    bank: 'Банковский',
    cash: 'Наличные',
    crypto: 'Криптовалютный',
    investment: 'Инвестиционный',
  };
  return labels[type] || type;
}

export function getCategoryTypeLabel(type: string): string {
  const labels: Record<string, string> = {
    income: 'Доходы',
    expense: 'Расходы',
    transfer: 'Переводы',
  };
  return labels[type] || type;
}

export function getCounterpartyTypeLabel(type: string): string {
  const labels: Record<string, string> = {
    customer: 'Клиент',
    supplier: 'Поставщик',
    partner: 'Партнер',
    other: 'Прочие',
  };
  return labels[type] || type;
}

export function getProjectStatusLabel(status: string): string {
  const labels: Record<string, string> = {
    active: 'Активный',
    completed: 'Завершен',
    on_hold: 'Приостановлен',
    cancelled: 'Отменен',
  };
  return labels[status] || status;
}

export function truncateAddress(address: string, startChars = 6, endChars = 4): string {
  if (address.length <= startChars + endChars) {
    return address;
  }
  return `${address.slice(0, startChars)}...${address.slice(-endChars)}`;
}

export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

export function validateTronAddress(address: string): boolean {
  return address.length === 34 && address.startsWith('T');
}
