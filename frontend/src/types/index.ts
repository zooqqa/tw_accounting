// Пользователи
export interface User {
  id: number;
  email: string;
  name: string | null;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

// Счета
export interface Account {
  id: number;
  name: string;
  type: 'bank' | 'cash' | 'crypto' | 'investment';
  currency: string;
  balance: number;
  description: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string | null;
}

export interface AccountCreate {
  name: string;
  type: 'bank' | 'cash' | 'crypto' | 'investment';
  currency: string;
  description?: string;
}

// Проекты
export interface Project {
  id: number;
  name: string;
  description: string | null;
  status: 'active' | 'completed' | 'on_hold' | 'cancelled';
  start_date: string | null;
  end_date: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string | null;
}

// Категории
export interface Category {
  id: number;
  name: string;
  type: 'income' | 'expense' | 'transfer';
  description: string | null;
  parent_id: number | null;
  is_active: boolean;
  created_at: string;
  updated_at: string | null;
}

// Контрагенты
export interface Counterparty {
  id: number;
  name: string;
  type: 'customer' | 'supplier' | 'partner' | 'other';
  contact_info: string | null;
  tax_id: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string | null;
}

// Транзакции
export interface Transaction {
  id: number;
  description: string;
  type: 'income' | 'expense' | 'transfer';
  status: 'pending' | 'completed' | 'cancelled' | 'draft';
  amount: number;
  date: string;
  project_id: number | null;
  category_id: number | null;
  counterparty_id: number | null;
  created_at: string;
  updated_at: string | null;
}

export interface TransactionEntry {
  id: number;
  account_id: number;
  account_name: string;
  amount: number;
  direction: 'DEBIT' | 'CREDIT';
  description: string;
}

export interface TransactionCreate {
  amount: number;
  description: string;
  income_account_id?: number;
  expense_account_id?: number;
  bank_account_id?: number;
  from_account_id?: number;
  to_account_id?: number;
  project_id?: number;
  category_id?: number;
  counterparty_id?: number;
  date?: string;
}

// Криптовалюты
export interface CryptoTransaction {
  amount_crypto: number;
  currency: 'TRX' | 'USDT';
  description: string;
  crypto_account_id: number;
  usd_account_id: number;
  tx_hash?: string;
  wallet_from?: string;
  wallet_to?: string;
  fee_crypto?: number;
  project_id?: number;
  category_id?: number;
  counterparty_id?: number;
}

export interface CryptoTransactionDetail {
  transaction_id: number;
  currency: string;
  amount_crypto: number;
  rate_to_usd: number;
  tx_hash: string | null;
  wallet_from: string | null;
  wallet_to: string | null;
  fee: number | null;
  block_number: number | null;
  confirmation_count: number | null;
}

export interface CryptoRates {
  rates: {
    TRX: number;
    USDT: number;
  };
  base_currency: string;
  updated_at: string;
}

// API Response
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
}
