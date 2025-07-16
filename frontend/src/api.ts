import axios from 'axios';

// API配置
const API_BASE_URL = 'http://localhost:8000';

// 创建axios实例
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 查询请求类型
export interface QueryRequest {
  question: string;
}

// 查询响应类型
export interface QueryResponse {
  success: boolean;
  question: string;
  sql?: string;
  data?: any[];
  count?: number;
  error?: string;
  execution_time?: number;
}

// 示例查询类型
export interface SampleQuery {
  question: string;
  description: string;
}

// 示例查询响应类型
export interface SampleQueriesResponse {
  sample_queries: SampleQuery[];
}

// API服务类
export class ApiService {
  // 查询API
  static async query(request: QueryRequest): Promise<QueryResponse> {
    const response = await api.post<QueryResponse>('/api/query', request);
    return response.data;
  }

  // 获取示例查询
  static async getSampleQueries(): Promise<SampleQueriesResponse> {
    const response = await api.get<SampleQueriesResponse>('/api/sample-queries');
    return response.data;
  }

  // 健康检查
  static async healthCheck(): Promise<{ message: string; status: string }> {
    const response = await api.get('/');
    return response.data;
  }
}

export default ApiService; 