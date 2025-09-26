import axios from 'axios';
import type {
  User,
  LoginRequest,
  AuthResponse,
  Account,
  AccountCreate,
  Project,
  Category,
  Counterparty,
  Transaction,
  TransactionEntry,
  TransactionCreate,
  CryptoTransaction,
  CryptoTransactionDetail,
  CryptoRates,
} from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';

// Создаем экземпляр axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Интерцептор для добавления токена авторизации
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Интерцептор для обработки ошибок
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  login: async (credentials: LoginRequest): Promise<AuthResponse> => {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    
    const response = await api.post('/api/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
    return response.data;
  },

  register: async (userData: { email: string; password: string; name?: string }): Promise<User> => {
    const response = await api.post('/api/auth/register', userData);
    return response.data;
  },

  getProfile: async (): Promise<User> => {
    const response = await api.get('/api/auth/me');
    return response.data;
  },

  updateProfile: async (userData: Partial<User>): Promise<User> => {
    const response = await api.patch('/api/auth/me', userData);
    return response.data;
  },
};

// Accounts API
export const accountsApi = {
  getAll: async (): Promise<Account[]> => {
    const response = await api.get('/api/accounts/');
    return response.data;
  },

  getById: async (id: number): Promise<Account> => {
    const response = await api.get(`/api/accounts/${id}`);
    return response.data;
  },

  create: async (accountData: AccountCreate): Promise<Account> => {
    const response = await api.post('/api/accounts/', accountData);
    return response.data;
  },

  update: async (id: number, accountData: Partial<AccountCreate>): Promise<Account> => {
    const response = await api.patch(`/api/accounts/${id}`, accountData);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/api/accounts/${id}`);
  },

  getBalance: async (id: number): Promise<{ account_id: number; balance: number }> => {
    const response = await api.get(`/api/transactions/accounts/${id}/balance`);
    return response.data;
  },
};

// Projects API
export const projectsApi = {
  getAll: async (): Promise<Project[]> => {
    const response = await api.get('/api/projects/');
    return response.data;
  },

  create: async (projectData: Omit<Project, 'id' | 'created_at' | 'updated_at'>): Promise<Project> => {
    const response = await api.post('/api/projects/', projectData);
    return response.data;
  },

  update: async (id: number, projectData: Partial<Project>): Promise<Project> => {
    const response = await api.patch(`/api/projects/${id}`, projectData);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/api/projects/${id}`);
  },
};

// Categories API
export const categoriesApi = {
  getAll: async (): Promise<Category[]> => {
    const response = await api.get('/api/categories/');
    return response.data;
  },

  create: async (categoryData: Omit<Category, 'id' | 'created_at' | 'updated_at'>): Promise<Category> => {
    const response = await api.post('/api/categories/', categoryData);
    return response.data;
  },

  update: async (id: number, categoryData: Partial<Category>): Promise<Category> => {
    const response = await api.patch(`/api/categories/${id}`, categoryData);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/api/categories/${id}`);
  },
};

// Counterparties API
export const counterpartiesApi = {
  getAll: async (): Promise<Counterparty[]> => {
    const response = await api.get('/api/counterparties/');
    return response.data;
  },

  create: async (counterpartyData: Omit<Counterparty, 'id' | 'created_at' | 'updated_at'>): Promise<Counterparty> => {
    const response = await api.post('/api/counterparties/', counterpartyData);
    return response.data;
  },

  update: async (id: number, counterpartyData: Partial<Counterparty>): Promise<Counterparty> => {
    const response = await api.patch(`/api/counterparties/${id}`, counterpartyData);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/api/counterparties/${id}`);
  },
};

// Transactions API
export const transactionsApi = {
  getAll: async (params?: { type?: string; project_id?: number; category_id?: number }): Promise<Transaction[]> => {
    const response = await api.get('/api/transactions/', { params });
    return response.data;
  },

  getById: async (id: number): Promise<Transaction> => {
    const response = await api.get(`/api/transactions/${id}`);
    return response.data;
  },

  getEntries: async (id: number): Promise<TransactionEntry[]> => {
    const response = await api.get(`/api/transactions/${id}/entries`);
    return response.data;
  },

  createIncome: async (transactionData: TransactionCreate): Promise<Transaction> => {
    const response = await api.post('/api/transactions/income', transactionData);
    return response.data;
  },

  createExpense: async (transactionData: TransactionCreate): Promise<Transaction> => {
    const response = await api.post('/api/transactions/expense', transactionData);
    return response.data;
  },

  createTransfer: async (transactionData: TransactionCreate): Promise<Transaction> => {
    const response = await api.post('/api/transactions/transfer', transactionData);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/api/transactions/${id}`);
  },
};

// Crypto API
export const cryptoApi = {
  getRates: async (): Promise<CryptoRates> => {
    const response = await api.get('/api/crypto/rates');
    return response.data;
  },

  getSupportedCurrencies: async (): Promise<{ currencies: any[] }> => {
    const response = await api.get('/api/crypto/supported-currencies');
    return response.data;
  },

  createIncome: async (cryptoData: CryptoTransaction): Promise<Transaction> => {
    const response = await api.post('/api/crypto/income', cryptoData);
    return response.data;
  },

  createExpense: async (cryptoData: CryptoTransaction): Promise<Transaction> => {
    const response = await api.post('/api/crypto/expense', cryptoData);
    return response.data;
  },

  getTransactionDetails: async (id: number): Promise<CryptoTransactionDetail> => {
    const response = await api.get(`/api/crypto/transactions/${id}/details`);
    return response.data;
  },

  validateWallet: async (address: string, network = 'tron'): Promise<{ valid: boolean; error?: string }> => {
    const response = await api.get(`/api/crypto/wallet-validation/${address}?network=${network}`);
    return response.data;
  },

  validateTronTransaction: async (txHash: string): Promise<{ valid: boolean; transaction_info?: any }> => {
    const response = await api.post('/api/crypto/validate-tron', { tx_hash: txHash });
    return response.data;
  },
};

export default api;
